from parser import Parser
from node import Node
from symbolTable import SymbolTable
import sys


if len(sys.argv) == 1:
    raise Exception("didn't pass the filename")
file = sys.argv[1]

f = open(file, "r")
code=f.read()
tree=Parser.run(code)
table=SymbolTable(None)
tree.Evaluate(table)