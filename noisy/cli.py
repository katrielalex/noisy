#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .checkers import CHECKERS
from .noisyLexer import noisyLexer
from .noisyParser import noisyParser

import antlr4
import click
import logging


def parse(f):
    lexer = noisyLexer(antlr4.FileStream(f))
    parser = noisyParser(antlr4.CommonTokenStream(lexer))
    parser._errHandler = antlr4.error.ErrorStrategy.BailErrorStrategy()
    tree = parser.spec()

    walker = antlr4.ParseTreeWalker()
    for checker in CHECKERS:
        logging.debug(f'Running checker {checker.__name__}')
        try:
            walker.walk(checker(), tree)
        except AssertionError as e:
            logging.exception(e)
            continue


@click.command()
@click.argument('filenames', nargs=-1)
def main(filenames):
    logging.basicConfig(level=logging.INFO)

    for f in filenames:
        logging.info(f'Reading {f}')
        parse(f)


if __name__ == '__main__':
    main()
