from parser import Parser
from node import Node

f = open("operacoes.vbs", "r")
code=f.read()
tree=Parser.run(code)
print(tree.Evaluate())