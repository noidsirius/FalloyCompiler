
from antlr4 import *
from antlr4.tree.Tree import TerminalNodeImpl

from FAlloyUtils import fuzzy_relations, adjective_mapper, phase

from FAlloyLexer import FAlloyLexer
from FAlloyListener import FAlloyListener
from FAlloyParser import FAlloyParser


# def exprContainsFuzzyRelation(expr_node):
#     if isinstance(expr_node.children[0], FAlloyParser.NameContext):
#         return expr_node.children[0].children[0].symbol.text in fuzzy_relations
#     if isinstance(expr_node.children[0], FAlloyParser.ExprContext):
#         return exprContainsFuzzyRelation(expr_node.children[0])
#     return False

class FAlloyPrintListener(FAlloyListener):
    def enterEveryRule(self, ctx:ParserRuleContext):
        if phase == 2:
            if hasattr(ctx, "SKIP_PRINT"):
                for child in ctx.children:
                    child.SKIP_PRINT = True


    def exitSpecification(self, ctx: FAlloyParser.SpecificationContext):
        if phase == 3:
            print("")

    def exitModule(self, ctx: FAlloyParser.ModuleContext):
        if phase == 3:
            print("")

    def exitOpen(self, ctx:FAlloyParser.OpenContext):
        if phase == 3:
            print("")

    def exitParagraph(self, ctx:FAlloyParser.ParagraphContext):
        if phase == 3:
            print("")

    def enterFuzzyDecl(self, ctx: FAlloyParser.FuzzyDeclContext):
        if phase == 1:
            for child in ctx.children:
                if isinstance(child, TerminalNodeImpl) and child.symbol.text == ':':
                    break
                if isinstance(child, FAlloyParser.NameContext):
                    fuzzy_relations.append(child.children[0].symbol.text)

    def exitFuzzyDecl(self, ctx: FAlloyParser.FuzzyDeclContext):
        if phase == 3:
            print("-> one FuzzyValue")

    def enterBinLogicExpr(self, ctx: FAlloyParser.BinLogicExprContext):
        if phase == 1:
            if len(ctx.children) == 3 and isinstance(ctx.children[1], FAlloyParser.FuzzyCompareOpContext):
                ctx.children[2].FUZZY_EQUAL_SECOND = True
                ctx.children[1].SKIP_PRINT = True
                ctx.FUZZY_EXPR = True
                if len(ctx.children[1].children) > 1:
                    ctx.FUZZY_ADJECTIVE = ctx.children[1].children[1].children[0].symbol.text

                else:
                    ctx.HAS_FUZZY_VALUE = True
        if phase == 3:
            if len(ctx.children) == 3 and isinstance(ctx.children[1], FAlloyParser.FuzzyCompareOpContext):
                print("fuzzyEQUAL[", end="")
            if hasattr(ctx, 'FUZZY_EQUAL_SECOND'):
                print(", ", end="")

    def exitBinLogicExpr(self, ctx: FAlloyParser.BinLogicExprContext):
        if phase == 3:
            if hasattr(ctx, 'FUZZY_EXPR'):
                print("] ", end="")
                if hasattr(ctx, 'FUZZY_ADJECTIVE'):
                    print('in %s' % adjective_mapper[getattr(ctx, 'FUZZY_ADJECTIVE')], end="")

    def enterLExpr(self, ctx:FAlloyParser.LExprContext):
        if phase == 3:
            if hasattr(ctx, 'SHOULD_FUZZIFY'):
                print('(', end='')
            if hasattr(ctx, 'IFF'):
                print('fuzzyIFONLYIF[ ', end='')
            if hasattr(ctx, 'IMPLIES'):
                print('fuzzyIF[ ', end='')
            if hasattr(ctx, 'AND'):
                print('fuzzyAND[ ', end='')
            if hasattr(ctx, 'OR'):
                print('fuzzyOR[ ', end='')
            if hasattr(ctx, 'IFELSE'):
                print('fuzzyIFELSE[ ', end='')
            if hasattr(ctx, 'ADD_COMMA'):
                print(', ', end='')

    def exitLExpr(self, ctx:FAlloyParser.LExprContext):
        if phase == 1:
            if isinstance(ctx.children[0], FAlloyParser.LCExprContext):
                if hasattr(ctx.children[0], "HAS_FUZZY_VALUE"):
                    ctx.HAS_FUZZY_VALUE = True
            if len(ctx.children) == 3:
                if hasattr(ctx.children[0], "HAS_FUZZY_VALUE") or hasattr(ctx.children[2], "HAS_FUZZY_VALUE"):
                    ctx.HAS_FUZZY_VALUE = True
                    if not hasattr(ctx.children[0], "HAS_FUZZY_VALUE"):
                        ctx.children[0].SHOULD_FUZZIFY = True
                    if not hasattr(ctx.children[2], "HAS_FUZZY_VALUE"):
                        ctx.children[2].SHOULD_FUZZIFY = True
                    ctx.children[2].ADD_COMMA = True
                    ctx.children[1].SKIP_PRINT = True
                    lopt_text = ctx.children[1].children[0].symbol.text
                    if lopt_text == 'iff' or lopt_text == '<=>':
                        ctx.IFF = True
                    if lopt_text == 'implies' or lopt_text == '=>':
                        ctx.IMPLIES = True
                    if lopt_text == 'and' or lopt_text == '&&':
                        ctx.AND = True
                    if lopt_text == 'or' or lopt_text == '||':
                        ctx.OR = True

            if len(ctx.children) == 5:
                if hasattr(ctx.children[0], "HAS_FUZZY_VALUE") or hasattr(ctx.children[2],
                                                                          "HAS_FUZZY_VALUE") or hasattr(ctx.children[4],
                                                                                                        "HAS_FUZZY_VALUE"):
                    ctx.HAS_FUZZY_VALUE = True
                    if not hasattr(ctx.children[0], "HAS_FUZZY_VALUE"):
                        ctx.children[0].SHOULD_FUZZIFY = True
                    if not hasattr(ctx.children[2], "HAS_FUZZY_VALUE"):
                        ctx.children[2].SHOULD_FUZZIFY = True
                    if not hasattr(ctx.children[4], "HAS_FUZZY_VALUE"):
                        ctx.children[4].SHOULD_FUZZIFY = True
                    ctx.children[2].ADD_COMMA = True
                    ctx.children[4].ADD_COMMA = True
                    ctx.children[1].SKIP_PRINT = True
                    ctx.children[3].SKIP_PRINT = True
                    ctx.IFELSE = True

        if phase == 3:
            if hasattr(ctx, 'IFF') or hasattr(ctx, 'IMPLIES') or hasattr(ctx, 'AND') or hasattr(ctx, 'OR') or \
                    hasattr(ctx, 'IFELSE'):
                print('] ', end='')
            if hasattr(ctx, 'SHOULD_FUZZIFY'):
                print("=> fuzzyTrue else fuzzyFalse)", end="")

    def enterLCExpr(self, ctx:FAlloyParser.LCExprContext):
        pass

    # Exit a parse tree produced by FAlloyParser#lCExpr.
    def exitLCExpr(self, ctx:FAlloyParser.LCExprContext):
        if phase == 1:
            if isinstance(ctx.children[0], FAlloyParser.BinLogicExprContext):
                if hasattr(ctx.children[0], "HAS_FUZZY_VALUE"):
                    ctx.HAS_FUZZY_VALUE = True
            # if len(ctx.children) == 3:
            #     if hasattr(ctx.children[0], "HAS_FUZZY_VALUE") or hasattr(ctx.children[2], "HAS_FUZZY_VALUE"):
            #         ctx.HAS_FUZZY_VALUE = True
            #         if not hasattr(ctx.children[0], "HAS_FUZZY_VALUE"):
            #             ctx.children[0].SHOULD_FUZZIFY = True
            #         if not hasattr(ctx.children[2], "HAS_FUZZY_VALUE"):
            #             ctx.children[2].SHOULD_FUZZIFY = True
            #         ctx.children[2].ADD_COMMA = True
            #         lopt_text = ctx.children[1].children[0].symbol.text
            #         ctx.children[1].SKIP_PRINT = True
            #         if lopt_text == 'iff' or lopt_text == '<=>':
            #             ctx.IFF = True
            #         if lopt_text == 'implies' or lopt_text == '=>':
            #             ctx.IMPLIES = True
            #         if lopt_text == 'and' or lopt_text == '&&':
            #             ctx.AND = True
            #         if lopt_text == 'or' or lopt_text == '||':
            #             ctx.OR = True
            #
            # if len(ctx.children) == 5:
            #     if hasattr(ctx.children[0], "HAS_FUZZY_VALUE") or hasattr(ctx.children[2],
            #                                                               "HAS_FUZZY_VALUE") or hasattr(ctx.children[4],
            #                                                                                             "HAS_FUZZY_VALUE"):
            #         ctx.HAS_FUZZY_VALUE = True
            #         if not hasattr(ctx.children[0], "HAS_FUZZY_VALUE"):
            #             ctx.children[0].SHOULD_FUZZIFY = True
            #         if not hasattr(ctx.children[2], "HAS_FUZZY_VALUE"):
            #             ctx.children[2].SHOULD_FUZZIFY = True
            #         if not hasattr(ctx.children[4], "HAS_FUZZY_VALUE"):
            #             ctx.children[4].SHOULD_FUZZIFY = True
            #         ctx.children[2].ADD_COMMA = True
            #         ctx.children[4].ADD_COMMA = True
            #         ctx.children[1].SKIP_PRINT = True
            #         ctx.children[3].SKIP_PRINT = True
            #         ctx.IFELSE = True

    def visitTerminal(self, node: TerminalNode):
        if phase == 3:
            if hasattr(node, "SKIP_PRINT"):
                return
            if isinstance(node.parentCtx, FAlloyParser.FuzzyDeclContext):
                if node.symbol.text == 'fuzzy':
                    return
            print(node.symbol.text, end=" ")


def main():
    #fin = open("../f_test_3.als", "r")
    fin = open("f_test_3.als", "r")
    lexer = FAlloyLexer(InputStream(fin.read()))
    stream = CommonTokenStream(lexer)
    parser = FAlloyParser(stream)
    tree = parser.specification()
    printer = FAlloyPrintListener()
    walker = ParseTreeWalker()
    global phase
    phase = 1
    walker.walk(printer, tree)
    phase = 2
    walker.walk(printer, tree)
    phase = 3
    walker.walk(printer, tree)
    # print(fuzzy_relations)
if __name__ == '__main__':
    main()
