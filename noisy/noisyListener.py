# -*- coding: utf-8 -*-
# Generated from noisy.g4 by ANTLR 4.7.1
from antlr4 import *
if __name__ is not None and '.' in __name__:
    from .noisyParser import noisyParser
else:
    from noisyParser import noisyParser

# This class defines a complete listener for a parse tree produced by noisyParser.


class noisyListener(ParseTreeListener):

    # Enter a parse tree produced by noisyParser#spec.
    def enterSpec(self, ctx: noisyParser.SpecContext):
        pass

    # Exit a parse tree produced by noisyParser#spec.
    def exitSpec(self, ctx: noisyParser.SpecContext):
        pass

    # Enter a parse tree produced by noisyParser#name.
    def enterName(self, ctx: noisyParser.NameContext):
        pass

    # Exit a parse tree produced by noisyParser#name.
    def exitName(self, ctx: noisyParser.NameContext):
        pass

    # Enter a parse tree produced by noisyParser#subname.
    def enterSubname(self, ctx: noisyParser.SubnameContext):
        pass

    # Exit a parse tree produced by noisyParser#subname.
    def exitSubname(self, ctx: noisyParser.SubnameContext):
        pass

    # Enter a parse tree produced by noisyParser#args.
    def enterArgs(self, ctx: noisyParser.ArgsContext):
        pass

    # Exit a parse tree produced by noisyParser#args.
    def exitArgs(self, ctx: noisyParser.ArgsContext):
        pass

    # Enter a parse tree produced by noisyParser#arg.
    def enterArg(self, ctx: noisyParser.ArgContext):
        pass

    # Exit a parse tree produced by noisyParser#arg.
    def exitArg(self, ctx: noisyParser.ArgContext):
        pass

    # Enter a parse tree produced by noisyParser#predistributed.
    def enterPredistributed(self, ctx: noisyParser.PredistributedContext):
        pass

    # Exit a parse tree produced by noisyParser#predistributed.
    def exitPredistributed(self, ctx: noisyParser.PredistributedContext):
        pass

    # Enter a parse tree produced by noisyParser#preline.
    def enterPreline(self, ctx: noisyParser.PrelineContext):
        pass

    # Exit a parse tree produced by noisyParser#preline.
    def exitPreline(self, ctx: noisyParser.PrelineContext):
        pass

    # Enter a parse tree produced by noisyParser#body.
    def enterBody(self, ctx: noisyParser.BodyContext):
        pass

    # Exit a parse tree produced by noisyParser#body.
    def exitBody(self, ctx: noisyParser.BodyContext):
        pass

    # Enter a parse tree produced by noisyParser#bodyline.
    def enterBodyline(self, ctx: noisyParser.BodylineContext):
        pass

    # Exit a parse tree produced by noisyParser#bodyline.
    def exitBodyline(self, ctx: noisyParser.BodylineContext):
        pass

    # Enter a parse tree produced by noisyParser#token.
    def enterToken(self, ctx: noisyParser.TokenContext):
        pass

    # Exit a parse tree produced by noisyParser#token.
    def exitToken(self, ctx: noisyParser.TokenContext):
        pass

    # Enter a parse tree produced by noisyParser#key.
    def enterKey(self, ctx: noisyParser.KeyContext):
        pass

    # Exit a parse tree produced by noisyParser#key.
    def exitKey(self, ctx: noisyParser.KeyContext):
        pass

    # Enter a parse tree produced by noisyParser#operation.
    def enterOperation(self, ctx: noisyParser.OperationContext):
        pass

    # Exit a parse tree produced by noisyParser#operation.
    def exitOperation(self, ctx: noisyParser.OperationContext):
        pass

    # Enter a parse tree produced by noisyParser#direction.
    def enterDirection(self, ctx: noisyParser.DirectionContext):
        pass

    # Exit a parse tree produced by noisyParser#direction.
    def exitDirection(self, ctx: noisyParser.DirectionContext):
        pass
