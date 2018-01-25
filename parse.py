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


@checker
class SpecPrinter(noisyListener):
    def exitSpec(self, ctx):
        name = ctx.name().subname().getText()
        predistributed = ctx.predistributed()
        if predistributed is not None:
            logging.debug(f'Spec {name}: predistributed keys are around')
        lines = ctx.body().line()
        logging.debug(f'Spec {name}: {len(lines)} lines')
        for i, line in enumerate(lines):
            # import ipdb; ipdb.set_trace()
            for token in line.token():
                logging.debug(f'\t line {i}: {token.getText().strip()}')


@checker
class KeysSentAtMostOnce(noisyListener):
    @staticmethod
    def all_lines(ctx):
        predistributed = ctx.predistributed()
        if predistributed is not None:
            yield from predistributed.line()
        yield from ctx.body().line()

    def exitSpec(self, ctx):
        name = ctx.name().subname().getText()
        seen = collections.defaultdict(collections.Counter)
        for line in self.all_lines(ctx):
            direction = line.direction().getText()
            for token in line.token():
                key = token.key()
                if key is not None:
                    seen[direction].update(key.getText())

        for direction, counts in seen.items():
            for key, count in counts.items():
                assert count == 1, f'Key {key} sent {count} times as A {direction} B in spec {name}'


@checker
class PredistributedStaticsAreArguments(noisyListener):
    def exitSpec(self, ctx):
        args = ctx.name().args()
        predistributed = ctx.predistributed()
        directions = '<- ->'.split()
        if predistributed is None:
            return

        # prekeys = the set of keys that were transmitted before '...'
        prekeys = {d: set() for d in directions}
        for line in predistributed.line():
            prekeys[line.direction().getText()].update(
                {token.key().getText() for token in line.token()},
            )

        # if no 's' keys were sent then we're all good
        if not any('s' in prekeys[d] for d in directions):
            return

        # argkeys = the set of keys in the argument list
        argkeys = {d: set() for d in directions}
        for arg in args.arg():
            # getTokens(RESPONDER) is a non-empty list if arg matched a RESPONDER token
            # i.e. arg contained an 'r' such as re or rs as opposed to just r or s
            direction = '<-' if arg.getTokens(
                noisyParser.RESPONDER,
            ) else '->'
            argkeys[direction].add(arg.key().getText())

        for d in directions:
            if 's' in prekeys[d]:
                assert 's' in argkeys[d], \
                    f"Key 's' was sent in the predistribution phase but not registered as an argument."


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
