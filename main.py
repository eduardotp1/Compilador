from parser import Parser
from node import Node
from symbolTable import SymbolTable
from writer import *
import sys


if len(sys.argv) == 1:
    raise Exception("didn't pass the filename")
file = sys.argv[1]

f = open(file, "r")
code=f.read()
tree=Parser.run(code)
table=SymbolTable()
tree.Evaluate(table)
Writer.file()