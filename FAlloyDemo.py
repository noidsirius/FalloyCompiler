
from antlr4 import *
from FAlloyLexer import FAlloyLexer
from FAlloyListener import FAlloyListener
from FAlloyParser import FAlloyParser
import sys

class FAlloyPrintListener(FAlloyListener):
    def enterHi(self, ctx):
        print("FAlloy: %s" % ctx.ID())

def main():
    fin = open("../f_test_3.als", "r")
    lexer = FAlloyLexer(InputStream(fin.read()))
    stream = CommonTokenStream(lexer)
    parser = FAlloyParser(stream)
    tree = parser.specification()
    printer = FAlloyPrintListener()
    walker = ParseTreeWalker()
    walker.walk(printer, tree)

if __name__ == '__main__':
    main()
