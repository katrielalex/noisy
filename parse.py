#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from noisyLexer import noisyLexer
from noisyParser import noisyParser
from noisyListener import noisyListener

import antlr4
import click
import collections
import itertools
import logging


CHECKERS = []


def checker(cls):
    CHECKERS.append(cls)
    return cls


def all_keys_with_directions(ctx):
    predistributed = ctx.predistributed()
    if predistributed is not None:
        for line in predistributed.preline():
            for key in line.key():
                yield line.direction().getText(), key.getText()
    for line in ctx.body().bodyline():
        for token in line.token():
            if token.key() is not None:
                yield line.direction().getText(), token.key().getText()


def all_argkeys(args):
    # argkeys = the set of keys in the argument list
    argkeys = {d: set() for d in '<- ->'.split()}
    if args is not None and args.arg() is not None:
        for arg in args.arg():
            # getTokens(RESPONDER) is a non-empty list if arg matched a RESPONDER token
            # i.e. arg contained an 'r' such as re or rs as opposed to just r or s
            direction = '<-' if arg.getTokens(
                noisyParser.RESPONDER,
            ) else '->'
            argkeys[direction].add(arg.key().getText())
    return argkeys


@checker
class SpecPrinter(noisyListener):
    def exitSpec(self, ctx):
        name = ctx.name().subname().getText()
        predistributed = ctx.predistributed()
        if predistributed is not None:
            logging.debug(f'Spec {name}: predistributed keys are around')
        lines = ctx.body().bodyline()
        logging.debug(f'Spec {name}: {len(lines)} lines')
        for i, line in enumerate(lines):
            # import ipdb; ipdb.set_trace()
            for token in line.token():
                logging.debug(f'\t line {i}: {token.getText().strip()}')


@checker
class KeysSentAtMostOnce(noisyListener):
    def exitSpec(self, ctx):
        name = ctx.name().subname().getText()
        seen = collections.defaultdict(collections.Counter)
        for direction, key in all_keys_with_directions(ctx):
            seen[direction].update(key)

        for direction, counts in seen.items():
            for key, count in counts.items():
                assert count == 1, f'Key {key} sent {count} times as A {direction} B in spec {name}'


@checker
class PredistributedKeysAreArguments(noisyListener):
    def exitSpec(self, ctx):
        predistributed = ctx.predistributed()
        directions = '<- ->'.split()
        if predistributed is None:
            return

        # prekeys = the set of keys that were transmitted before '...'
        prekeys = {d: set() for d in directions}
        for line in predistributed.preline():
            prekeys[line.direction().getText()].update(
                {key.getText() for key in line.key()},
            )

        # argkeys = the set of keys registered in arguments
        argkeys = all_argkeys(ctx.name().args())

        for d in directions:
            for key in prekeys[d]:
                assert key in argkeys[d], \
                    f'Key {key} was sent in the predistribution phase but not registered as an argument.'


@checker
class AllStaticsAreArguments(noisyListener):
    def exitSpec(self, ctx):
        statics = {d: k for d, k in all_keys_with_directions(ctx) if k == 's'}
        argkeys = all_argkeys(ctx.name().args())

        for d in statics:
            assert 's' in argkeys[d], \
                f'Static key was sent {d:} but not registered as an argument.'


# TODO(katriel) check that the handshake messages alternate direction starting with ->
# UNLESS there is a pre-message <- containing e, in which case the handshake messages should
# alternate direction starting with <-

# TODO(katriel) check that all ephemeral keys are used before sending anything else

@checker
class EphemeralsAreAlwaysUsed(noisyListener):
    def exitSpec(self, ctx):
        directions = '-> <-'.split()
        danger_remote_public_keys = {d: set() for d in directions}
        for line in ctx.body().bodyline():
            direction = line.direction().getText()
            for token in line.token():
                operation = token.operation()
                if operation is None:
                    assert not danger_remote_public_keys[direction], \
                        "You're sending a key but you haven't used an ephemeral " \
                        f'with {danger_remote_public_keys[direction]} yet!'
                    continue
                operation = operation.getText()
                local_key = operation[directions.index(direction)]
                remote_key = operation[1 - directions.index(direction)]
                if local_key == 'e' and remote_key in danger_remote_public_keys[direction]:
                    danger_remote_public_keys[direction].remove(remote_key)
                if local_key != 'e':
                    danger_remote_public_keys[direction].add(remote_key)


def parse(f):
    lexer = noisyLexer(antlr4.FileStream(f))
    parser = noisyParser(antlr4.CommonTokenStream(lexer))
    parser._errHandler = antlr4.error.ErrorStrategy.BailErrorStrategy()
    tree = parser.spec()

    walker = antlr4.ParseTreeWalker()
    for checker in CHECKERS:
        logging.info(f'Running checker {checker.__name__}')
        walker.walk(checker(), tree)

    return tree


@click.command()
@click.argument('filenames', nargs=-1)
def main(filenames):
    logging.basicConfig(level=logging.INFO)

    for f in filenames:
        logging.info(f'Reading {f}')
        try:
            parse(f)
        except AssertionError as e:
            logging.exception(e)
            continue


if __name__ == '__main__':
    main()
