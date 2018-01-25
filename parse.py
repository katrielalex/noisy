#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from noisyLexer import noisyLexer
from noisyParser import noisyParser
from noisyListener import noisyListener

import antlr4
import click
import collections
import logging


CHECKERS = []


def checker(cls):
    CHECKERS.append(cls)
    return cls


@checker
class SpecPrinter(noisyListener):
    def exitSpec(self, ctx):
        name = ctx.name().subname().getText()
        lines = ctx.line()
        print(f'Spec {name}: {len(lines)} lines')
        for i, line in enumerate(lines):
            # import ipdb; ipdb.set_trace()
            for token in line.token():
                print(f'\t line {i}: {token.getText().strip()}')


@checker
class EphemeralsSentAtMostOnce(noisyListener):
    def exitSpec(self, ctx):
        seen = collections.defaultdict(collections.Counter)
        for line in ctx.line():
            direction = line.direction().getText()
            for token in line.token():
                key = token.key()
                if key is not None:
                    seen[direction].update(key.getText())
        print(seen)


def parse(f):
    lexer = noisyLexer(antlr4.FileStream(f))
    parser = noisyParser(antlr4.CommonTokenStream(lexer))
    tree = parser.spec()

    walker = antlr4.ParseTreeWalker()
    for checker in CHECKERS:
        logging.info(f'Running checker {checker.__name__}')
        walker.walk(checker(), tree)

    return tree


@click.command()
@click.argument('filename')
def main(filename):
    logging.basicConfig(level=logging.INFO)

    parse(filename)


if __name__ == '__main__':
    main()
