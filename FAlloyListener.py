# Generated from FAlloy.g4 by ANTLR 4.7.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .FAlloyParser import FAlloyParser
else:
    from FAlloyParser import FAlloyParser

# This class defines a complete listener for a parse tree produced by FAlloyParser.
class FAlloyListener(ParseTreeListener):

    # Enter a parse tree produced by FAlloyParser#specification.
    def enterSpecification(self, ctx:FAlloyParser.SpecificationContext):
        pass

    # Exit a parse tree produced by FAlloyParser#specification.
    def exitSpecification(self, ctx:FAlloyParser.SpecificationContext):
        pass


    # Enter a parse tree produced by FAlloyParser#module.
    def enterModule(self, ctx:FAlloyParser.ModuleContext):
        pass

    # Exit a parse tree produced by FAlloyParser#module.
    def exitModule(self, ctx:FAlloyParser.ModuleContext):
        pass


    # Enter a parse tree produced by FAlloyParser#open.
    def enterOpen(self, ctx:FAlloyParser.OpenContext):
        pass

    # Exit a parse tree produced by FAlloyParser#open.
    def exitOpen(self, ctx:FAlloyParser.OpenContext):
        pass


    # Enter a parse tree produced by FAlloyParser#paragraph.
    def enterParagraph(self, ctx:FAlloyParser.ParagraphContext):
        pass

    # Exit a parse tree produced by FAlloyParser#paragraph.
    def exitParagraph(self, ctx:FAlloyParser.ParagraphContext):
        pass


    # Enter a parse tree produced by FAlloyParser#factDecl.
    def enterFactDecl(self, ctx:FAlloyParser.FactDeclContext):
        pass

    # Exit a parse tree produced by FAlloyParser#factDecl.
    def exitFactDecl(self, ctx:FAlloyParser.FactDeclContext):
        pass


    # Enter a parse tree produced by FAlloyParser#assertDecl.
    def enterAssertDecl(self, ctx:FAlloyParser.AssertDeclContext):
        pass

    # Exit a parse tree produced by FAlloyParser#assertDecl.
    def exitAssertDecl(self, ctx:FAlloyParser.AssertDeclContext):
        pass


    # Enter a parse tree produced by FAlloyParser#funDecl.
    def enterFunDecl(self, ctx:FAlloyParser.FunDeclContext):
        pass

    # Exit a parse tree produced by FAlloyParser#funDecl.
    def exitFunDecl(self, ctx:FAlloyParser.FunDeclContext):
        pass


    # Enter a parse tree produced by FAlloyParser#cmdDecl.
    def enterCmdDecl(self, ctx:FAlloyParser.CmdDeclContext):
        pass

    # Exit a parse tree produced by FAlloyParser#cmdDecl.
    def exitCmdDecl(self, ctx:FAlloyParser.CmdDeclContext):
        pass


    # Enter a parse tree produced by FAlloyParser#scope.
    def enterScope(self, ctx:FAlloyParser.ScopeContext):
        pass

    # Exit a parse tree produced by FAlloyParser#scope.
    def exitScope(self, ctx:FAlloyParser.ScopeContext):
        pass


    # Enter a parse tree produced by FAlloyParser#typescope.
    def enterTypescope(self, ctx:FAlloyParser.TypescopeContext):
        pass

    # Exit a parse tree produced by FAlloyParser#typescope.
    def exitTypescope(self, ctx:FAlloyParser.TypescopeContext):
        pass


    # Enter a parse tree produced by FAlloyParser#sigDecl.
    def enterSigDecl(self, ctx:FAlloyParser.SigDeclContext):
        pass

    # Exit a parse tree produced by FAlloyParser#sigDecl.
    def exitSigDecl(self, ctx:FAlloyParser.SigDeclContext):
        pass


    # Enter a parse tree produced by FAlloyParser#enumDecl.
    def enterEnumDecl(self, ctx:FAlloyParser.EnumDeclContext):
        pass

    # Exit a parse tree produced by FAlloyParser#enumDecl.
    def exitEnumDecl(self, ctx:FAlloyParser.EnumDeclContext):
        pass


    # Enter a parse tree produced by FAlloyParser#sigQual.
    def enterSigQual(self, ctx:FAlloyParser.SigQualContext):
        pass

    # Exit a parse tree produced by FAlloyParser#sigQual.
    def exitSigQual(self, ctx:FAlloyParser.SigQualContext):
        pass


    # Enter a parse tree produced by FAlloyParser#sigExt.
    def enterSigExt(self, ctx:FAlloyParser.SigExtContext):
        pass

    # Exit a parse tree produced by FAlloyParser#sigExt.
    def exitSigExt(self, ctx:FAlloyParser.SigExtContext):
        pass


    # Enter a parse tree produced by FAlloyParser#rootExpr.
    def enterRootExpr(self, ctx:FAlloyParser.RootExprContext):
        pass

    # Exit a parse tree produced by FAlloyParser#rootExpr.
    def exitRootExpr(self, ctx:FAlloyParser.RootExprContext):
        pass


    # Enter a parse tree produced by FAlloyParser#letOrDeclExpr.
    def enterLetOrDeclExpr(self, ctx:FAlloyParser.LetOrDeclExprContext):
        pass

    # Exit a parse tree produced by FAlloyParser#letOrDeclExpr.
    def exitLetOrDeclExpr(self, ctx:FAlloyParser.LetOrDeclExprContext):
        pass


    # Enter a parse tree produced by FAlloyParser#quant.
    def enterQuant(self, ctx:FAlloyParser.QuantContext):
        pass

    # Exit a parse tree produced by FAlloyParser#quant.
    def exitQuant(self, ctx:FAlloyParser.QuantContext):
        pass


    # Enter a parse tree produced by FAlloyParser#lExpr.
    def enterLExpr(self, ctx:FAlloyParser.LExprContext):
        pass

    # Exit a parse tree produced by FAlloyParser#lExpr.
    def exitLExpr(self, ctx:FAlloyParser.LExprContext):
        pass


    # Enter a parse tree produced by FAlloyParser#lOpt.
    def enterLOpt(self, ctx:FAlloyParser.LOptContext):
        pass

    # Exit a parse tree produced by FAlloyParser#lOpt.
    def exitLOpt(self, ctx:FAlloyParser.LOptContext):
        pass


    # Enter a parse tree produced by FAlloyParser#lCExpr.
    def enterLCExpr(self, ctx:FAlloyParser.LCExprContext):
        pass

    # Exit a parse tree produced by FAlloyParser#lCExpr.
    def exitLCExpr(self, ctx:FAlloyParser.LCExprContext):
        pass


    # Enter a parse tree produced by FAlloyParser#cOp.
    def enterCOp(self, ctx:FAlloyParser.COpContext):
        pass

    # Exit a parse tree produced by FAlloyParser#cOp.
    def exitCOp(self, ctx:FAlloyParser.COpContext):
        pass


    # Enter a parse tree produced by FAlloyParser#unHighOp.
    def enterUnHighOp(self, ctx:FAlloyParser.UnHighOpContext):
        pass

    # Exit a parse tree produced by FAlloyParser#unHighOp.
    def exitUnHighOp(self, ctx:FAlloyParser.UnHighOpContext):
        pass


    # Enter a parse tree produced by FAlloyParser#binLogicExpr.
    def enterBinLogicExpr(self, ctx:FAlloyParser.BinLogicExprContext):
        pass

    # Exit a parse tree produced by FAlloyParser#binLogicExpr.
    def exitBinLogicExpr(self, ctx:FAlloyParser.BinLogicExprContext):
        pass


    # Enter a parse tree produced by FAlloyParser#otherBinOp.
    def enterOtherBinOp(self, ctx:FAlloyParser.OtherBinOpContext):
        pass

    # Exit a parse tree produced by FAlloyParser#otherBinOp.
    def exitOtherBinOp(self, ctx:FAlloyParser.OtherBinOpContext):
        pass


    # Enter a parse tree produced by FAlloyParser#fuzzyCompareOp.
    def enterFuzzyCompareOp(self, ctx:FAlloyParser.FuzzyCompareOpContext):
        pass

    # Exit a parse tree produced by FAlloyParser#fuzzyCompareOp.
    def exitFuzzyCompareOp(self, ctx:FAlloyParser.FuzzyCompareOpContext):
        pass


    # Enter a parse tree produced by FAlloyParser#fuzzyUnOp.
    def enterFuzzyUnOp(self, ctx:FAlloyParser.FuzzyUnOpContext):
        pass

    # Exit a parse tree produced by FAlloyParser#fuzzyUnOp.
    def exitFuzzyUnOp(self, ctx:FAlloyParser.FuzzyUnOpContext):
        pass


    # Enter a parse tree produced by FAlloyParser#arrowExpr.
    def enterArrowExpr(self, ctx:FAlloyParser.ArrowExprContext):
        pass

    # Exit a parse tree produced by FAlloyParser#arrowExpr.
    def exitArrowExpr(self, ctx:FAlloyParser.ArrowExprContext):
        pass


    # Enter a parse tree produced by FAlloyParser#joinExpr.
    def enterJoinExpr(self, ctx:FAlloyParser.JoinExprContext):
        pass

    # Exit a parse tree produced by FAlloyParser#joinExpr.
    def exitJoinExpr(self, ctx:FAlloyParser.JoinExprContext):
        pass


    # Enter a parse tree produced by FAlloyParser#expr.
    def enterExpr(self, ctx:FAlloyParser.ExprContext):
        pass

    # Exit a parse tree produced by FAlloyParser#expr.
    def exitExpr(self, ctx:FAlloyParser.ExprContext):
        pass


    # Enter a parse tree produced by FAlloyParser#unLowOp.
    def enterUnLowOp(self, ctx:FAlloyParser.UnLowOpContext):
        pass

    # Exit a parse tree produced by FAlloyParser#unLowOp.
    def exitUnLowOp(self, ctx:FAlloyParser.UnLowOpContext):
        pass


    # Enter a parse tree produced by FAlloyParser#declOrFuzzyDecl.
    def enterDeclOrFuzzyDecl(self, ctx:FAlloyParser.DeclOrFuzzyDeclContext):
        pass

    # Exit a parse tree produced by FAlloyParser#declOrFuzzyDecl.
    def exitDeclOrFuzzyDecl(self, ctx:FAlloyParser.DeclOrFuzzyDeclContext):
        pass


    # Enter a parse tree produced by FAlloyParser#decl.
    def enterDecl(self, ctx:FAlloyParser.DeclContext):
        pass

    # Exit a parse tree produced by FAlloyParser#decl.
    def exitDecl(self, ctx:FAlloyParser.DeclContext):
        pass


    # Enter a parse tree produced by FAlloyParser#fuzzyDecl.
    def enterFuzzyDecl(self, ctx:FAlloyParser.FuzzyDeclContext):
        pass

    # Exit a parse tree produced by FAlloyParser#fuzzyDecl.
    def exitFuzzyDecl(self, ctx:FAlloyParser.FuzzyDeclContext):
        pass


    # Enter a parse tree produced by FAlloyParser#letDecl.
    def enterLetDecl(self, ctx:FAlloyParser.LetDeclContext):
        pass

    # Exit a parse tree produced by FAlloyParser#letDecl.
    def exitLetDecl(self, ctx:FAlloyParser.LetDeclContext):
        pass


    # Enter a parse tree produced by FAlloyParser#binOp.
    def enterBinOp(self, ctx:FAlloyParser.BinOpContext):
        pass

    # Exit a parse tree produced by FAlloyParser#binOp.
    def exitBinOp(self, ctx:FAlloyParser.BinOpContext):
        pass


    # Enter a parse tree produced by FAlloyParser#arrowOp.
    def enterArrowOp(self, ctx:FAlloyParser.ArrowOpContext):
        pass

    # Exit a parse tree produced by FAlloyParser#arrowOp.
    def exitArrowOp(self, ctx:FAlloyParser.ArrowOpContext):
        pass


    # Enter a parse tree produced by FAlloyParser#block.
    def enterBlock(self, ctx:FAlloyParser.BlockContext):
        pass

    # Exit a parse tree produced by FAlloyParser#block.
    def exitBlock(self, ctx:FAlloyParser.BlockContext):
        pass


    # Enter a parse tree produced by FAlloyParser#blockOrBar.
    def enterBlockOrBar(self, ctx:FAlloyParser.BlockOrBarContext):
        pass

    # Exit a parse tree produced by FAlloyParser#blockOrBar.
    def exitBlockOrBar(self, ctx:FAlloyParser.BlockOrBarContext):
        pass


    # Enter a parse tree produced by FAlloyParser#name.
    def enterName(self, ctx:FAlloyParser.NameContext):
        pass

    # Exit a parse tree produced by FAlloyParser#name.
    def exitName(self, ctx:FAlloyParser.NameContext):
        pass


    # Enter a parse tree produced by FAlloyParser#ref.
    def enterRef(self, ctx:FAlloyParser.RefContext):
        pass

    # Exit a parse tree produced by FAlloyParser#ref.
    def exitRef(self, ctx:FAlloyParser.RefContext):
        pass


