class Node:
        def Evaluate(self,table):
            pass
class BinOp(Node):
    def __init__ (self, value,children):
        self.value=value
        self.children=children
    def Evaluate(self,table):
        x=self.children[0].Evaluate(table)
        y=self.children[1].Evaluate(table)
        if x[1]==y[1]=="INTEGER":
            if self.value=="+":
                return [(x[0]+y[0]),"INTEGER"]
            if self.value=="-":
                return [(x[0]-y[0]),"INTEGER"]
            if self.value=="*":
                return [(x[0]*y[0]),"INTEGER"]
            if self.value=="/":
                return [(x[0]//y[0]),"INTEGER"]
            if self.value=="<":
                if ((x[0]<y[0])):
                    return [True,"BOOLEAN"]
                else:
                    return [False,"BOOLEAN"]
            if self.value==">":
                if ((x[0]>y[0])):
                    return [True,"BOOLEAN"]
                else:
                    return [False,"BOOLEAN"]
            if self.value=="=":
                if ((x[0]==y[0])):
                    return [True,"BOOLEAN"]
                else:
                    return [False,"BOOLEAN"]

            if x[1]==y[1]=="BOOLEAN":
                if self.value == 'and':
                    return [x[0] and y[0], "BOOLEAN"]
                if self.value == 'or':
                    return [x[0] or y[0], "BOOLEAN"]

            raise Exception("Can't operate with two different types")

class UnOp(Node):
    def __init__ (self, value,children):
        self.value=value
        self.children=children
    def Evaluate(self,table):
        if self.children[0].Evaluate(table)[1] == "INTEGER":
            if self.value=="+":
                return [(+self.children[0].Evaluate(table)[0]),"INTEGER"]
            if self.value=="-":
                return [(-self.children[0].Evaluate(table)[0]),"INTEGER"]

        if self.children[0].Evaluate(table)[1] == "BOOLEAN":
            if self.value == 'not':
                return [not (self.children[0].Evaluate(table)[0]), "BOOLEAN"]
        raise Exception("Type is not correct")

class IntVal(Node):
    def __init__ (self, value,children):
        self.value=value
        self.children=children
    def Evaluate(self,table):
        return [self.value, "INTEGER"]

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
        if self.children[0].value not in table.table:
            raise Exception("The variable is not declared")
        if table.table[self.children[0].value][1]==self.children[1].Evaluate(table)[1]:
            table.set_value(self.children[0].value, self.children[1].Evaluate(table))
        else:
            raise Exception("The type of the value is not the type of the variable")

class TypeNode(Node):
    def __init__ (self, value,children):
        self.value=value
        self.children=children
    def Evaluate(self,table):
        return self.value

class PrintNode(Node):
    def __init__ (self, value,children):
        self.value=value
        self.children=children
    def Evaluate(self,table):
        print(self.children[0].Evaluate(table)[0])

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
        if self.children[0].Evaluate(table)[1]!="BOOLEAN":
            raise Exception("Type must be boolean")
        while self.children[0].Evaluate(table)[0]:
            self.children[1].Evaluate(table)

class IfNode(Node):
    def __init__ (self, value,children):
        self.value=value
        self.children=children
    def Evaluate(self,table):
        if self.children[0].Evaluate(table)[1]!="BOOLEAN":
            raise Exception("Type must be boolean")
        if self.children[0].Evaluate(table)[0]:
            self.children[1].Evaluate(table)
        else:
            if len(self.children) == 3:
                self.children[2].Evaluate(table)

class InputNode(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, table):
        return [int(input()), "INTEGER"]

class VarDec(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self,  table):
        table.set_type(self.children[0].value, self.children[1].value)

class BooleanVal(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self,  table):
        return [self.value, "BOOLEAN"]