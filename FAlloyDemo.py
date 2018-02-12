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
    v = STR_result
    return STR_result


def is_fuzzy_relation(parser_node):
    return hasattr(parser_node, "IS_FUZZY_REL") or to_string(parser_node).strip().split(' ')[-1] in fuzzy_relations


class FAlloyPrintListener(FAlloyListener):
    def enterEveryRule(self, ctx: ParserRuleContext):
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

    def exitOpen(self, ctx: FAlloyParser.OpenContext):
        if phase == 3:
            print("")

    def exitParagraph(self, ctx: FAlloyParser.ParagraphContext):
        if phase == 3:
            print("")

    def exitLetOrDeclExpr(self, ctx: FAlloyParser.LetOrDeclExprContext):
        if not isinstance(ctx.children[0], FAlloyParser.LExprContext):
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

    def enterLExpr(self, ctx: FAlloyParser.LExprContext):
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

    def exitLExpr(self, ctx: FAlloyParser.LExprContext):
        if phase == 1:
            if isinstance(ctx.children[0], FAlloyParser.LCExprContext):
                if is_fuzzy_relation(ctx.children[0]):
                    ctx.IS_FUZZY_REL = True
            if len(ctx.children) == 3:
                if isinstance(ctx.children[0], FAlloyParser.LExprContext):
                    if is_fuzzy_relation(ctx.children[0]) or is_fuzzy_relation(ctx.children[2]):
                        ctx.IS_FUZZY_REL = True
                        if not is_fuzzy_relation(ctx.children[0]):
                            ctx.children[0].SHOULD_FUZZIFY = True
                        if not is_fuzzy_relation(ctx.children[2]):
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
                else:
                    if is_fuzzy_relation(ctx.children[1]):
                        ctx.IS_FUZZY_REL = True

            if len(ctx.children) == 5:
                if is_fuzzy_relation(ctx.children[0]) or is_fuzzy_relation(ctx.children[2]) or is_fuzzy_relation(
                        ctx.children[4]):
                    ctx.IS_FUZZY_REL = True
                    if not is_fuzzy_relation(ctx.children[0]):
                        ctx.children[0].SHOULD_FUZZIFY = True
                    if not is_fuzzy_relation(ctx.children[2]):
                        ctx.children[2].SHOULD_FUZZIFY = True
                    if not is_fuzzy_relation(ctx.children[4]):
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

    def enterLCExpr(self, ctx: FAlloyParser.LCExprContext):
        if phase == 3:
            if hasattr(ctx, 'NOT'):
                print("fuzzyNOT[", end='')
            if hasattr(ctx, 'IN'):
                print("fuzzyIN[", end="")
            if hasattr(ctx, 'ADD_COMMA'):
                print(", ", end="")

    # Exit a parse tree produced by FAlloyParser#lCExpr.
    def exitLCExpr(self, ctx: FAlloyParser.LCExprContext):
        if phase == 1:
            if isinstance(ctx.children[0], FAlloyParser.JoinExprContext):
                if is_fuzzy_relation(ctx.children[0]):
                    ctx.IS_FUZZY_REL = True
            if isinstance(ctx.children[0], FAlloyParser.BinLogicExprContext):
                if is_fuzzy_relation(ctx.children[0]):
                    ctx.IS_FUZZY_REL = True
            if isinstance(ctx.children[0], FAlloyParser.UnHighOpContext):
                if is_fuzzy_relation(ctx.children[1]):
                    ctx.IS_FUZZY_REL = True
                    un_high_op_text = ctx.children[0].children[0].symbol.text
                    if un_high_op_text == '!' or un_high_op_text == 'not':
                        ctx.children[0].SKIP_PRINT = True
                        ctx.NOT = True
            if isinstance(ctx.children[0], FAlloyParser.LCExprContext):
                if is_fuzzy_relation(ctx.children[0]) or is_fuzzy_relation(ctx.children[-1]):
                    cop_text = ctx.children[-2].children[0].symbol.text
                    if cop_text == 'in':
                        ctx.IN = True
                        ctx.IS_FUZZY_REL = True
                        ctx.children[-2].SKIP_PRINT = True
                        ctx.children[-1].ADD_COMMA = True
                        if len(ctx.children) == 4:
                            ctx.NOT = True
                            ctx.children[1].SKIP_PRINT = True

        if phase == 3:
            if hasattr(ctx, 'IN'):
                print("] ", end="")
            if hasattr(ctx, 'NOT'):
                print("] ", end='')

    def enterBinLogicExpr(self, ctx: FAlloyParser.BinLogicExprContext):
        if phase == 3:
            if hasattr(ctx, 'PLUSPLUS'):
                print("fuzzyPLUSPLUS[", end="")
            if hasattr(ctx, 'EQUAL'):
                print("fuzzyEQUAL[", end="")
            if hasattr(ctx, 'ADD_COMMA'):
                print(", ", end="")

    def exitBinLogicExpr(self, ctx: FAlloyParser.BinLogicExprContext):
        if phase == 1:
            if len(ctx.children) == 3 and isinstance(ctx.children[1], FAlloyParser.FuzzyCompareOpContext):
                ctx.children[2].ADD_COMMA = True
                ctx.children[1].SKIP_PRINT = True
                ctx.EQUAL = True
                if len(ctx.children[1].children) > 1:
                    ctx.FUZZY_ADJECTIVE = ctx.children[1].children[1].children[0].symbol.text
                else:
                    ctx.IS_FUZZY_REL = True
            elif len(ctx.children) == 3 and isinstance(ctx.children[1], FAlloyParser.OtherBinOpContext):
                if to_string(ctx.children[1]).strip().split(' ')[-1] == '++' and is_fuzzy_relation(
                        ctx.children[0]) and is_fuzzy_relation(ctx.children[2]):
                    ctx.PLUSPLUS = True
                    ctx.children[1].SKIP_PRINT = True
                    ctx.children[2].ADD_COMMA = True
            else:
                for child in ctx.children:
                    if is_fuzzy_relation(child):
                        ctx.IS_FUZZY_REL = True
                        break
        if phase == 3:
            if hasattr(ctx, 'PLUSPLUS'):
                print("] ", end="")
            if hasattr(ctx, 'EQUAL'):
                print("] ", end="")
                if hasattr(ctx, 'FUZZY_ADJECTIVE'):
                    print('in %s ' % adjective_mapper[getattr(ctx, 'FUZZY_ADJECTIVE')], end="")

    def exitArrowExpr(self, ctx: FAlloyParser.ArrowExprContext):
        if phase == 1:
            if isinstance(ctx.children[0], FAlloyParser.JoinExprContext):
                if is_fuzzy_relation(ctx.children[0]):
                    ctx.IS_FUZZY_REL = True

    def enterJoinExpr(self, ctx: FAlloyParser.JoinExprContext):
        if phase == 1:
            if len(ctx.children) == 3 and isinstance(ctx.children[0], FAlloyParser.JoinExprContext):
                if is_fuzzy_relation(ctx.children[0]) or is_fuzzy_relation(ctx.children[2]):
                    ctx.children[1].SKIP_PRINT = True
                    ctx.children[2].ADD_COMMA = True
                    ctx.FUZZY_JOIN = True
                    ctx.IS_FUZZY_REL = True
        if phase == 3:
            if hasattr(ctx, "FUZZY_JOIN"):
                print("fuzzyDotJoin[", end='')
            if hasattr(ctx, 'ADD_COMMA'):
                print(", ", end="")

    def exitJoinExpr(self, ctx: FAlloyParser.JoinExprContext):
        if phase == 1:
            if is_fuzzy_relation(ctx.children[0]):
                ctx.IS_FUZZY_REL = True
            if len(ctx.children) == 3 and is_fuzzy_relation(ctx.children[2]):
                ctx.IS_FUZZY_REL = True
        if phase == 3:
            if hasattr(ctx, "FUZZY_JOIN"):
                print("] ", end='')

    def enterExpr(self, ctx: FAlloyParser.ExprContext):
        if phase == 1:
            if to_string(ctx.children[0]).startswith('fuzzy'):
                ctx.IS_FUZZY_REL = True
        if phase == 3:
            if hasattr(ctx, "TRANSPOSE"):
                print("fuzzyTranspose[", end='')
            if hasattr(ctx, "TRANSITIVE"):
                print("fuzzyTransitive[", end='')

    def exitExpr(self, ctx: FAlloyParser.ExprContext):
        if phase == 1:
            if isinstance(ctx.children[0], FAlloyParser.UnLowOpContext):
                if is_fuzzy_relation(ctx.children[1]):
                    ctx.children[0].SKIP_PRINT = True
                    if ctx.children[0].children[0].symbol.text == '~':
                        ctx.TRANSPOSE = True
                    if ctx.children[0].children[0].symbol.text == '^':
                        ctx.TRANSITIVE = True
                    ctx.IS_FUZZY_REL = True
            for child in ctx.children:
                if is_fuzzy_relation(child):
                    ctx.IS_FUZZY_REL = True
                    break
        if phase == 3:
            if hasattr(ctx, "TRANSPOSE"):
                print("] ", end='')
            if hasattr(ctx, "TRANSITIVE"):
                print("] ", end='')

    def enterName(self, ctx: FAlloyParser.NameContext):
        if phase == 1:
            if is_fuzzy_relation(ctx):
                ctx.IS_FUZZY_REL = True

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
        print("fuzzyMAXSUM [%s]" % relation)
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
