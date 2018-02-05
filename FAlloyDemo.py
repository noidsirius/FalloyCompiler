
from antlr4 import *
from antlr4.tree.Tree import TerminalNodeImpl

from FAlloyUtils import fuzzy_relations

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
    def exitSpecification(self, ctx: FAlloyParser.SpecificationContext):
        print("")

    def exitModule(self, ctx: FAlloyParser.ModuleContext):
        print("")

    def exitOpen(self, ctx:FAlloyParser.OpenContext):
        print("")

    def exitParagraph(self, ctx:FAlloyParser.ParagraphContext):
        print("")

    def enterFuzzyDecl(self, ctx: FAlloyParser.FuzzyDeclContext):
        for child in ctx.children:
            if isinstance(child, TerminalNodeImpl) and child.symbol.text == ':':
                break
            if isinstance(child, FAlloyParser.NameContext):
                fuzzy_relations.append(child.children[0].symbol.text)

    def exitFuzzyDecl(self, ctx: FAlloyParser.FuzzyDeclContext):
        print("-> one FuzzyValue")

    # def enterExpr(self, ctx: FAlloyParser.ExprContext):
    #     if len(ctx.children) == 3 and isinstance(ctx.children[1], FAlloyParser.FuzzyCompareOpContext):
    #         ctx.children[2].FUZZY_EQUAL_SECOND = True
    #         print("fuzzyEQUAL[", end="")
    #     if ctx.FUZZY_EQUAL_SECOND:
    #         print(", ", end="")
    #
    # # Exit a parse tree produced by FAlloyParser#expr.
    # def exitExpr(self, ctx: FAlloyParser.ExprContext):
    #     if ctx.FUZZY_EQUAL_SECOND:
    #         print("] ", end="")
    #     pass

    def visitTerminal(self, node: TerminalNode):
        if isinstance(node.parentCtx, FAlloyParser.FuzzyDeclContext):
            if node.symbol.text == 'fuzzy':
                return
        # if isinstance(node.parentCtx, FAlloyParser.FuzzyCompareOpContext):
        #     return
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
    walker.walk(printer, tree)
    print(fuzzy_relations)
if __name__ == '__main__':
    main()
