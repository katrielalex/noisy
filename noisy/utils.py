# -*- coding: utf-8 -*-
from .noisyParser import noisyParser


class TokenType:
    KEY = 0
    OP = 1


def all_things_with_directions(ctx):
    predistributed = ctx.predistributed()
    if predistributed is not None:
        for line in predistributed.preline():
            for key in line.key():
                yield (TokenType.KEY, (line.direction().getText(), key.getText()))
    for line in ctx.body().bodyline():
        for token in line.token():
            if token.key() is not None:
                yield (TokenType.KEY, (line.direction().getText(), token.key().getText()))
            else:
                yield (TokenType.OP, (line.direction().getText(), token.operation().getText()))


def all_keys_with_directions(ctx):
    for type, thing in all_things_with_directions(ctx):
        if type == TokenType.KEY:
            yield thing


def all_ops_with_directions(ctx):
    for type, thing in all_things_with_directions(ctx):
        if type == TokenType.OP:
            yield thing


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
