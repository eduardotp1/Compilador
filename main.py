from parser import Parser
from node import Node
from symbolTable import SymbolTable

f = open("operacoes.vbs", "r")
code=f.read()
tree=Parser.run(code)
table=SymbolTable()
tree.Evaluate(table)