import sys

from antlr4 import *
from antlr4.tree.Tree import TerminalNodeImpl

from FAlloyUtils import fuzzy_relations, adjective_mapper, phase

from FAlloyLexer import FAlloyLexer
from FAlloyListener import FAlloyListener
from FAlloyParser import FAlloyParser

STR_result = ""


class StringListener(FAlloyListener):
    def visitTerminal(self, node: TerminalNode):
        global STR_result
        STR_result += node.symbol.text + ' '


def to_string(parser_node):
    global STR_result
    STR_result = ""
    printer = StringListener()
    walker = ParseTreeWalker()
    walker.walk(printer, parser_node)
    return STR_result



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
                ctx.children[2].ADD_COMMA = True
                ctx.children[1].SKIP_PRINT = True
                ctx.EQUAL = True
                if len(ctx.children[1].children) > 1:
                    ctx.FUZZY_ADJECTIVE = ctx.children[1].children[1].children[0].symbol.text
                else:
                    ctx.HAS_FUZZY_VALUE = True
        if phase == 3:
            if hasattr(ctx, 'EQUAL'):
                print("fuzzyEQUAL[", end="")
            if hasattr(ctx, 'ADD_COMMA'):
                print(", ", end="")

    def exitBinLogicExpr(self, ctx: FAlloyParser.BinLogicExprContext):
        if phase == 3:
            if hasattr(ctx, 'EQUAL'):
                print("] ", end="")
                if hasattr(ctx, 'FUZZY_ADJECTIVE'):
                    print('in %s' % adjective_mapper[getattr(ctx, 'FUZZY_ADJECTIVE')], end="")

    def enterLExpr(self, ctx:FAlloyParser.LExprContext):
        if phase == 3:
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
                print("=> fuzzyTrue else fuzzyFalse", end="")

    def enterLCExpr(self, ctx:FAlloyParser.LCExprContext):
        if phase == 3:
            if hasattr(ctx, 'NOT'):
                print("fuzzyNOT[", end='')
            if hasattr(ctx, 'EQUAL'):
                print("fuzzyEQUAL[", end="")
            if hasattr(ctx, 'ADD_COMMA'):
                print(", ", end="")

    # Exit a parse tree produced by FAlloyParser#lCExpr.
    def exitLCExpr(self, ctx:FAlloyParser.LCExprContext):
        if phase == 1:
            if isinstance(ctx.children[0], FAlloyParser.BinLogicExprContext):
                if hasattr(ctx.children[0], "HAS_FUZZY_VALUE"):
                    ctx.HAS_FUZZY_VALUE = True
            if isinstance(ctx.children[0], FAlloyParser.UnHighOpContext):
                if hasattr(ctx.children[1], "HAS_FUZZY_VALUE"):
                    ctx.HAS_FUZZY_VALUE = True
                    un_high_op_text = ctx.children[0].children[0].symbol.text
                    if un_high_op_text == '!' or un_high_op_text == 'not':
                        ctx.children[0].SKIP_PRINT = True
                        ctx.NOT = True
            if isinstance(ctx.children[0], FAlloyParser.LCExprContext):
                if hasattr(ctx.children[0], "HAS_FUZZY_VALUE") or hasattr(ctx.children[-1], "HAS_FUZZY_VALUE"):
                    ctx.HAS_FUZZY_VALUE = True
                    if not hasattr(ctx.children[0], "HAS_FUZZY_VALUE"):
                        ctx.children[0].SHOULD_FUZZIFY = True
                    if not hasattr(ctx.children[-1], "HAS_FUZZY_VALUE"):
                        ctx.children[-1].SHOULD_FUZZIFY = True
                else:
                    cop_text = ctx.children[-2].children[0].symbol.text
                    s1 = to_string(ctx.children[0])
                    s2 = s1.strip()
                    s3 = s2.split(' ')
                    lcexpr_first = to_string(ctx.children[0]).strip().split(' ')[-1]
                    if lcexpr_first in fuzzy_relations and cop_text == '=':
                        ctx.HAS_FUZZY_VALUE = True
                        ctx.EQUAL = True
                        ctx.children[-1].ADD_COMMA = True
                        ctx.children[1].SKIP_PRINT = True
                        if len(ctx.children) == 4:
                            ctx.NOT = True
                            ctx.children[2].SKIP_PRINT = True


        if phase == 3:
            if hasattr(ctx, 'EQUAL'):
                print("] ", end="")
            if hasattr(ctx, 'NOT'):
                print("] ", end='')

    def visitTerminal(self, node: TerminalNode):
        if phase == 3:
            if hasattr(node, "SKIP_PRINT"):
                return
            if isinstance(node.parentCtx, FAlloyParser.FuzzyDeclContext):
                if node.symbol.text == 'fuzzy':
                    return
            print(node.symbol.text, end=" ")


def print_fuzzy_constarints():
    print("fact {")
    for relation in fuzzy_relations:
        print("fuzzyMAXSUM [%s, univ]" % relation)
    print("}")


def main():
    if len(sys.argv) > 1:
        input_file_name = sys.argv[1]
        fin = open(input_file_name, "r")
    else:
        fin = open("alaki.txt", "r")
    lexer = FAlloyLexer(InputStream(fin.read()))
    stream = CommonTokenStream(lexer)
    parser = FAlloyParser(stream)
    tree = parser.specification()
    # print(to_string(tree))
    printer = FAlloyPrintListener()
    walker = ParseTreeWalker()
    global phase
    phase = 1
    walker.walk(printer, tree)
    phase = 2
    walker.walk(printer, tree)
    phase = 3
    walker.walk(printer, tree)
    print_fuzzy_constarints()
if __name__ == '__main__':
    main()
