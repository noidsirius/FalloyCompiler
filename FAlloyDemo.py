import sys

from antlr4 import *
from antlr4.tree.Tree import TerminalNodeImpl

from FAlloyUtils import fuzzy_relations, modifier_mapper, phase,\
    fuzzy_lone_relations, fuzzy_one_relations, fuzzy_set_relations, fuzzy_some_relations, predicates_nodes, predicates_names, \
    run_pred_names

from FAlloyLexer import FAlloyLexer
from FAlloyListener import FAlloyListener
from FAlloyParser import FAlloyParser

STR_result = ""


class StringListener(FAlloyListener):
    def enterEveryRule(self, ctx:ParserRuleContext):
        if hasattr(ctx, "SKIP_PRINT"):
            for child in ctx.children:
                child.SKIP_PRINT = True
    def visitTerminal(self, node: TerminalNode):
        if hasattr(node, "SKIP_PRINT"):
            return
        global STR_result
        STR_result += node.symbol.text + ' '


def to_string(parser_node):
    global STR_result
    STR_result = ""
    printer = StringListener()
    walker = ParseTreeWalker()
    walker.walk(printer, parser_node)
    return STR_result


class CallPredListener(FAlloyListener):
    def enterEveryRule(self, ctx:ParserRuleContext):
        if hasattr(ctx, "SKIP_PRINT"):
            for child in ctx.children:
                child.SKIP_PRINT = True

    def enterDecl(self, ctx:FAlloyParser.DeclContext):
        for child in ctx.children:
            if isinstance(child, TerminalNode):
                if child.symbol.text in ['private', 'disj']:
                    child.SKIP_PRINT = True
        ctx.children[-1].SKIP_PRINT = True
        ctx.children[-2].SKIP_PRINT = True

    def visitTerminal(self, node: TerminalNode):
        if hasattr(node, "SKIP_PRINT"):
            return
        global STR_result
        STR_result += node.symbol.text + ' '


def str_call_pred(parser_node):
    global STR_result
    STR_result = ""
    for child in parser_node.children:
        child.SKIP_PRINT = True
        if child.symbol.text == 'pred':
            break
    parser_node.children[-1].SKIP_PRINT = True
    printer = CallPredListener()
    walker = ParseTreeWalker()
    walker.walk(printer, parser_node)
    for child in parser_node.children:
        delattr(child,'SKIP_PRINT')
        if child.symbol.text == 'pred':
            break
    return STR_result


def str_fuzzify():
    return " => FV_10 else FV_00"

def is_fuzzy_fun(parser_node):
    name = to_string(parser_node).strip()
    return name.startswith('fuzzy') or name in predicates_names


def is_fuzzy_relation(parser_node):
    return hasattr(parser_node, "IS_FUZZY_REL") or to_string(parser_node).strip().split(' ')[-1] in fuzzy_relations


class FAlloyPrintListener(FAlloyListener):
    def enterEveryRule(self, ctx: ParserRuleContext):
        if phase == 1:
            ctx.BEFORE_TEXT = ""
            ctx.AFTER_TEXT = ""
        if phase == 3:
            if hasattr(ctx, "BEFORE_TEXT"):
                print(ctx.BEFORE_TEXT, end="")
            if hasattr(ctx, "SKIP_PRINT"):
                for child in ctx.children:
                    child.SKIP_PRINT = True

    def exitEveryRule(self, ctx: ParserRuleContext):
        if phase == 3:
            if hasattr(ctx, "AFTER_TEXT"):
                print(ctx.AFTER_TEXT, end="")

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

    def enterLetOrDeclExpr(self, ctx:FAlloyParser.LetOrDeclExprContext):
        if phase == 3:
            pass

    def exitLetOrDeclExpr(self, ctx: FAlloyParser.LetOrDeclExprContext):
        if phase == 2:
            if isinstance(ctx.children[0], FAlloyParser.QuantContext):
                ctx.BEFORE_TEXT = '(('
                ctx.AFTER_TEXT = ') %s)' % str_fuzzify()
        if phase == 3:
            if not isinstance(ctx.children[0], FAlloyParser.LExprContext):
                print("")

    def exitFuzzyDecl(self, ctx: FAlloyParser.FuzzyDeclContext):
        if phase == 1:
            line_frs = []
            for child in ctx.children:
                if isinstance(child, TerminalNodeImpl) and child.symbol.text == ':':
                    break
                if isinstance(child, FAlloyParser.NameContext):
                    line_frs.append(child.children[0].symbol.text)

            if isinstance(ctx.children[-1].children[0].children[0].children[0].children[0],
                          FAlloyParser.UnHighOpContext):
                ctx.children[-1].children[0].children[0].children[0].children[0].children[0].SKIP_PRINT = True
                multiplicity_str = ctx.children[-1].children[0].children[0].children[0].children[0].children[
                    0].symbol.text
                if multiplicity_str == 'one':
                    for fr in line_frs:
                        fuzzy_one_relations.append(fr)
                if multiplicity_str == 'some':
                    for fr in line_frs:
                        fuzzy_some_relations.append(fr)
                if multiplicity_str == 'set':
                    for fr in line_frs:
                        fuzzy_set_relations.append(fr)
                if multiplicity_str == 'lone':
                    for fr in line_frs:
                        fuzzy_lone_relations.append(fr)
            else:
                for fr in line_frs:
                    fuzzy_one_relations.append(fr)
            for fr in line_frs:
                fuzzy_relations.append(fr)
        if phase == 3:
            print("-> one FuzzyValue")

    def exitLExpr(self, ctx: FAlloyParser.LExprContext):
        if phase == 2:
            if isinstance(ctx.children[0], FAlloyParser.LCExprContext):
                if is_fuzzy_relation(ctx.children[0]):
                    ctx.IS_FUZZY_REL = True
            if len(ctx.children) == 3:
                if isinstance(ctx.children[0], FAlloyParser.LExprContext):
                    if is_fuzzy_relation(ctx.children[0]) or is_fuzzy_relation(ctx.children[2]):
                        ctx.IS_FUZZY_REL = True
                        if not is_fuzzy_relation(ctx.children[0]):
                            ctx.children[0].AFTER_TEXT += str_fuzzify()
                        if not is_fuzzy_relation(ctx.children[2]):
                            ctx.children[2].AFTER_TEXT += str_fuzzify()
                        ctx.children[2].BEFORE_TEXT = ','
                        ctx.children[1].SKIP_PRINT = True
                        lopt_text = ctx.children[1].children[0].symbol.text
                        ctx.AFTER_TEXT = ']'
                        if lopt_text == 'iff' or lopt_text == '<=>':
                            ctx.BEFORE_TEXT = 'fuzzyIFONLYIF['
                        if lopt_text == 'implies' or lopt_text == '=>':
                            ctx.BEFORE_TEXT = 'fuzzyIF['
                        if lopt_text == 'and' or lopt_text == '&&':
                            ctx.BEFORE_TEXT = 'fuzzyAND['
                        if lopt_text == 'or' or lopt_text == '||':
                            ctx.BEFORE_TEXT = 'fuzzyOR['
                else:
                    if is_fuzzy_relation(ctx.children[1]):
                        ctx.IS_FUZZY_REL = True

            if len(ctx.children) == 5:
                if is_fuzzy_relation(ctx.children[0]) or is_fuzzy_relation(ctx.children[2]) or is_fuzzy_relation(
                        ctx.children[4]):
                    ctx.IS_FUZZY_REL = True
                    if not is_fuzzy_relation(ctx.children[0]):
                        ctx.children[0].AFTER_TEXT += str_fuzzify()
                    if not is_fuzzy_relation(ctx.children[2]):
                        ctx.children[2].AFTER_TEXT += str_fuzzify()
                    if not is_fuzzy_relation(ctx.children[4]):
                        ctx.children[4].AFTER_TEXT += str_fuzzify()
                    ctx.children[2].BEFORE_TEXT = ','
                    ctx.children[4].BEFORE_TEXT = ','
                    ctx.children[1].SKIP_PRINT = True
                    ctx.children[3].SKIP_PRINT = True
                    ctx.BEFORE_TEXT = 'fuzzyIFELSE['
                    ctx.AFTER_TEXT = ']'

    # Exit a parse tree produced by FAlloyParser#lCExpr.
    def exitLCExpr(self, ctx: FAlloyParser.LCExprContext):
        if phase == 2:
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
                        ctx.BEFORE_TEXT += 'fuzzyNOT['
                        ctx.AFTER_TEXT += ']'
            if isinstance(ctx.children[0], FAlloyParser.LCExprContext):
                if is_fuzzy_relation(ctx.children[0]) or is_fuzzy_relation(ctx.children[-1]):
                    cop_text = ctx.children[-2].children[0].symbol.text
                    if cop_text == 'in':
                        if len(ctx.children) == 4:
                            ctx.BEFORE_TEXT += 'fuzzyNOT['
                            ctx.AFTER_TEXT += ']'
                            ctx.children[1].SKIP_PRINT = True
                        ctx.IN = True
                        ctx.BEFORE_TEXT += 'fuzzyIN['
                        ctx.AFTER_TEXT += ']'
                        ctx.IS_FUZZY_REL = True
                        ctx.children[-2].SKIP_PRINT = True
                        ctx.children[-1].BEFORE_TEXT = ','

    def exitBinLogicExpr(self, ctx: FAlloyParser.BinLogicExprContext):
        if phase == 2:
            if len(ctx.children) == 3 and isinstance(ctx.children[1], FAlloyParser.FuzzyCompareOpContext):
                ctx.children[2].BEFORE_TEXT = ','
                ctx.children[1].SKIP_PRINT = True
                ctx.EQUAL = True
                ctx.BEFORE_TEXT = "fuzzyEQUAL [" + ctx.BEFORE_TEXT
                ctx.AFTER_TEXT = "]"
                ctx.IS_FUZZY_REL = True
                if len(ctx.children[1].children) > 1:
                    ctx.BEFORE_TEXT = '%s [' % modifier_mapper[ctx.children[1].children[1].children[0].symbol.text] + ctx.BEFORE_TEXT
                    ctx.AFTER_TEXT += ']'
            elif len(ctx.children) == 3 and isinstance(ctx.children[1], FAlloyParser.OtherBinOpContext):
                if is_fuzzy_relation(ctx.children[0]) or is_fuzzy_relation(ctx.children[2]):
                    if to_string(ctx.children[1]).strip().split(' ')[-1] == '++':
                        ctx.BEFORE_TEXT = 'fuzzyPLUSPLUS[' + ctx.BEFORE_TEXT
                        ctx.AFTER_TEXT += ']'
                        ctx.children[2].BEFORE_TEXT = ','
                        ctx.children[1].SKIP_PRINT = True
                    elif to_string(ctx.children[1]).strip().split(' ')[-1] == '+':
                        ctx.BEFORE_TEXT = 'fuzzyPLUS[' + ctx.BEFORE_TEXT
                        ctx.AFTER_TEXT += ']'
                        ctx.children[2].BEFORE_TEXT = ','
                        ctx.children[1].SKIP_PRINT = True
                    elif to_string(ctx.children[1]).strip().split(' ')[-1] == '-':
                        ctx.BEFORE_TEXT = 'fuzzySUB[' + ctx.BEFORE_TEXT
                        ctx.AFTER_TEXT += ']'
                        ctx.children[2].BEFORE_TEXT = ','
                        ctx.children[1].SKIP_PRINT = True
                    elif to_string(ctx.children[1]).strip().split(' ')[-1] == '&':
                        ctx.BEFORE_TEXT = 'fuzzyINTERSECTION[' + ctx.BEFORE_TEXT
                        ctx.AFTER_TEXT += ']'
                        ctx.children[2].BEFORE_TEXT = ','
                        ctx.children[1].SKIP_PRINT = True
            else:
                for child in ctx.children:
                    if is_fuzzy_relation(child):
                        ctx.IS_FUZZY_REL = True
                        break

    def exitArrowExpr(self, ctx: FAlloyParser.ArrowExprContext):
        if phase == 2:
            if isinstance(ctx.children[0], FAlloyParser.JoinExprContext):
                if is_fuzzy_relation(ctx.children[0]):
                    ctx.IS_FUZZY_REL = True

    def exitJoinExpr(self, ctx: FAlloyParser.JoinExprContext):
        if phase == 2:
            if is_fuzzy_relation(ctx.children[0]):
                ctx.IS_FUZZY_REL = True
            if isinstance(ctx.children[0], FAlloyParser.JoinExprContext) and ctx.children[1].symbol.text == '[':
                if is_fuzzy_fun(ctx.children[0]):
                    ctx.IS_FUZZY_REL = True
            if len(ctx.children) == 3 and is_fuzzy_relation(ctx.children[2]):
                ctx.IS_FUZZY_REL = True
            if len(ctx.children) == 3 and isinstance(ctx.children[0], FAlloyParser.JoinExprContext):
                if is_fuzzy_relation(ctx.children[0]) or is_fuzzy_relation(ctx.children[2]):
                    ctx.children[1].SKIP_PRINT = True
                    ctx.children[2].BEFORE_TEXT = ','
                    ctx.BEFORE_TEXT = "fuzzyDotJoin[" + ctx.BEFORE_TEXT
                    ctx.AFTER_TEXT += ']'
                    ctx.IS_FUZZY_REL = True

    def exitExpr(self, ctx: FAlloyParser.ExprContext):
        if phase == 2:
            if to_string(ctx.children[0]).startswith('fuzzy'):
                ctx.IS_FUZZY_REL = True
            if isinstance(ctx.children[0], FAlloyParser.UnLowOpContext):
                if is_fuzzy_relation(ctx.children[1]):
                    ctx.children[0].SKIP_PRINT = True
                    if ctx.children[0].children[0].symbol.text == '~':
                        ctx.BEFORE_TEXT = "fuzzyTranspose[" + ctx.BEFORE_TEXT
                        ctx.AFTER_TEXT += "]"
                    if ctx.children[0].children[0].symbol.text == '^':
                        ctx.BEFORE_TEXT = "fuzzyTransitive[" + ctx.BEFORE_TEXT
                        ctx.AFTER_TEXT += "]"
                    ctx.IS_FUZZY_REL = True
            for child in ctx.children:
                if is_fuzzy_relation(child):
                    ctx.IS_FUZZY_REL = True
                    break

    def exitName(self, ctx: FAlloyParser.NameContext):
        if phase == 2:
            if is_fuzzy_relation(ctx):
                ctx.IS_FUZZY_REL = True

    def exitPredDecl(self, ctx:FAlloyParser.PredDeclContext):
        if phase == 2:
            predicates_nodes.append(ctx)
            for child in ctx.children:
                if isinstance(child, FAlloyParser.NameContext):
                    predicates_names.append(to_string(child).strip())
                    break
            if ctx.children[0].symbol.text == 'pred':
                ctx.children[0].ALTERED_TEXT = 'fun'
            elif ctx.children[1].symbol.text == 'pred':
                ctx.children[1].ALTERED_TEXT = 'fun'
            ctx.children[-1].BEFORE_TEXT = ': FuzzyValue'

    # def enterFactDecl(self, ctx:FAlloyParser.FactDeclContext):
    #     if phase == 2:
    #         for

    def exitCmdDecl(self, ctx:FAlloyParser.CmdDeclContext):
        if phase == 2:
            for child in ctx.children:
                if isinstance(child, FAlloyParser.NameContext):
                    child.BEFORE_TEXT = "RUN_"
                    run_pred_names.append(to_string(child).strip())
                    break

    def enterBlock(self, ctx:FAlloyParser.BlockContext):
        if phase == 3:
            if not isinstance(ctx.parentCtx.parentCtx, FAlloyParser.ParagraphContext) or isinstance(ctx.parentCtx, FAlloyParser.PredDeclContext):
                if len(ctx.children) > 3:
                    ctx.children[1].BEFORE_TEXT = 'fuzzyAND[' * (len(ctx.children) - 3)
                    for child in ctx.children[2:-1]:
                        child.BEFORE_TEXT = ','
                        child.AFTER_TEXT = ']'
                    # ctx.children[0].SKIP_PRINT = True
                    # ctx.children[-1].SKIP_PRINT = True


    def visitTerminal(self, node: TerminalNode):
        if phase == 3:
            if hasattr(node, "SKIP_PRINT"):
                return
            if isinstance(node.parentCtx, FAlloyParser.FuzzyDeclContext):
                if node.symbol.text == 'fuzzy':
                    return
            if hasattr(node, "ALTERED_TEXT"):
                print(node.ALTERED_TEXT, end=" ")
            else:
                print(node.symbol.text, end=" ")


def print_fuzzy_constarints():
    print("fact {")
    for relation in fuzzy_one_relations:
        print("fuzzyMAXSUM [%s]" % relation)
    for relation in fuzzy_some_relations:
        print("fuzzyAtLeastSUM [%s]" % relation)
    for relation in fuzzy_lone_relations:
        print("fuzzyAtMostSUM [%s]" % relation)
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
    for pred_node in predicates_nodes:
        pred_node.children[-1].SKIP_PRINT = True
        print(to_string(pred_node))
        print("{\n%s in AlmostTrue\n}" % str_call_pred(pred_node))
        for child in pred_node.children:
            if isinstance(child, FAlloyParser.NameContext):
                name = to_string(child).strip()
                if name in run_pred_names:
                    print(to_string(pred_node).replace(name, "RUN_"+name))
                    print("{\n%s in KB.PredTrue\n}" % str_call_pred(pred_node))
        delattr(pred_node.children[-1], "SKIP_PRINT")

    print_fuzzy_constarints()
    print("fact{\n KB.FactTrue = FV_10// + FV_08 + FV_05 + FV_02 + FV_00\n KB.PredTrue = FV_10\n}")


if __name__ == '__main__':
    main()
