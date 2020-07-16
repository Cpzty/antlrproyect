import sys
from antlr4 import *
from antlr4.tree.Tree import TerminalNodeImpl
from antlr4.tree.Trees import Trees

from lark.tree import pydot__tree_to_png

sys.path.insert(0, "D:/Documents/ultimo semestre/compiladores 2.0/antler project/gen")

from DecafLexer import DecafLexer
from DecafListener import DecafListener
from DecafParser import DecafParser



def parse(argv):
    if len(sys.argv) > 1:
        input = FileStream(argv[1]) #read the first argument as a filestream
        lexer = DecafLexer(input) #call your lexer
        stream = CommonTokenStream(lexer)
        parser = DecafParser(stream)
        tree = parser.program() #start from the parser rule, however should be changed to your entry rule for your specific grammar
        #pydot__tree_to_png(tree, "./tree.png")
        traverse(tree, parser.ruleNames)
        f = open('treegen.txt', 'w')
        f.write((Trees.toStringTree(tree, None, parser)))

        f.close()
        printer = DecafListener()
        walker = ParseTreeWalker()
        walker.walk(printer, tree)
        #print(walker)
    else:
        print('Error : Expected a valid file')

def traverse(tree, rule_names, indent = 0):

    if tree.getText() == "<EOF>":
        return
    elif isinstance(tree, TerminalNodeImpl):
        #print("{0}TOKEN='{1}'".format("  " * indent, tree.getText()))
        pass
    else:
        print("{0}{1}".format("  " * indent, rule_names[tree.getRuleIndex()]))
        for child in tree.children:
            traverse(child, rule_names, indent + 1)

parse(sys.argv)