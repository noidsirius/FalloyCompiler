
from antlr4 import *
from FAlloyLexer import FAlloyLexer
from FAlloyListener import FAlloyListener
from FAlloyParser import FAlloyParser
import sys

class FAlloyPrintListener(FAlloyListener):
    def exitSpecification(self, ctx: FAlloyParser.SpecificationContext):
        print("")

    def exitModule(self, ctx: FAlloyParser.ModuleContext):
        print("")

    def exitOpen(self, ctx:FAlloyParser.OpenContext):
        print("")

    def exitParagraph(self, ctx:FAlloyParser.ParagraphContext):
        print("")

    def visitTerminal(self, node: TerminalNode):
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

if __name__ == '__main__':
    main()
