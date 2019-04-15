class Node:
        def Evaluate(self,table):
            pass
class BinOp(Node):
    def __init__ (self, value,children):
        self.value=value
        self.children=children
    def Evaluate(self,table):
        if self.value=="+":
            return(self.children[0].Evaluate(table)+self.children[1].Evaluate(table))
        if self.value=="-":
            return(self.children[0].Evaluate(table)-self.children[1].Evaluate(table))
        if self.value=="*":
            return(self.children[0].Evaluate(table)*self.children[1].Evaluate(table))
        if self.value=="/":
            return(self.children[0].Evaluate(table)//self.children[1].Evaluate(table))
        if self.value=="<":
            if ((self.children[0].Evaluate(table)<self.children[1].Evaluate(table))):
                return True
            else:
                return False
        if self.value==">":
            if ((self.children[0].Evaluate(table)>self.children[1].Evaluate(table))):
                return True
            else:
                return False
        if self.value=="=":
            if ((self.children[0].Evaluate(table)==self.children[1].Evaluate(table))):
                return True
            else:
                return False

class UnOp(Node):
    def __init__ (self, value,children):
        self.value=value
        self.children=children
    def Evaluate(self,table):
        if self.value=="+":
            return(+self.children[0].Evaluate(table))
        if self.value=="-":
            return(-self.children[0].Evaluate(table))


class IntVal(Node):
    def __init__ (self, value,children):
        self.value=value
        self.children=children
    def Evaluate(self,table):
        return(self.value)

class NoOp(Node):
    def __init__ (self, value,children):
        self.value=value
        self.children=children

class IdentifierNode(Node):
    def __init__ (self, value,children):
        self.value=value
        self.children=children

    def Evaluate(self,table):
        return (table.get_value(self.value))

class AssigmentOp(Node):
    def __init__ (self, value,children):
        self.value=value
        self.children=children
    def Evaluate(self,table):
        table.set_value(self.children[0].value, self.children[1].Evaluate(table))

class PrintNode(Node):
    def __init__ (self, value,children):
        self.value=value
        self.children=children
    def Evaluate(self,table):
        print(self.children[0].Evaluate(table))

class StatementsNode(Node):
    def __init__ (self, value,children):
        self.value=value
        self.children=children
    def Evaluate(self,table):
        for i in self.children:
            i.Evaluate(table)

class WhileNode(Node):
    def __init__ (self, value,children):
        self.value=value
        self.children=children
    def Evaluate(self,table):
        while self.children[0].Evaluate(table):
            self.children[1].Evaluate(table)

class IfNode(Node):
    def __init__ (self, value,children):
        self.value=value
        self.children=children
    def Evaluate(self,table):
        if self.children[0].Evaluate(table):
            self.children[1].Evaluate(table)
        else:
            if len(self.children) == 3:
                self.children[2].Evaluate(table)

class InputNode(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, table):
        return int(input())