from parser import Parser
from node import Node

code=input()
tree=Parser.run(code)
print(tree.Evaluate())