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
    logging.basicConfig(level=logging.DEBUG)

    for f in filenames:
        logging.info(f'Reading {f}')
        parse(f)


if __name__ == '__main__':
    main()
