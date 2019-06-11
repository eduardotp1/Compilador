
from symbolTable import SymbolTable

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
            if x[0]=="TRUE" or x[0]:
                x1=True
            if x[0]=="FALSE" or not x[0]:
                x1=False
            
            if y[0]=="TRUE" or y[0]:
                y1=True
            if y[0]=="FALSE" or not y[0]:
                y1=False
            
            if self.value == 'and':
                if x1 and y1:
                    return ["TRUE", "BOOLEAN"]
                else:
                    return ["FALSE", "BOOLEAN"]
            if self.value == 'or':
                if x1 or y1:
                    return ["TRUE", "BOOLEAN"]
                else:
                    return ["FALSE", "BOOLEAN"]
            if self.value=="=":
                if x1 == y1:
                    return ["TRUE", "BOOLEAN"]
                else:
                    return ["FALSE", "BOOLEAN"]

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
            if self.value == 'NOT':
                if (self.children[0].Evaluate(table)[0]=="FALSE"):
                    return ["TRUE", "BOOLEAN"]
                else:
                    return ["FALSE", "BOOLEAN"]
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
        x=self.children[0].value
        y=self.children[1].Evaluate(table)
        if table.table[x][1]==y[1]:
            table.set_value(x, y[0])
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

class SubDec(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self,  table):
        if self.value in table.table:
            raise Exception("The variable is already declared")
        table.set_type(self.value,"SUB")
        table.set_value(self.value,self)
        

class FuncDec(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, table):
        if self.value in table.table:
            raise Exception("The variable is already declared")
        table.set_type(self.value,"FUNC")
        table.set_value(self.value,self)

class Call(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, table):
        no=table.get_value2(self.value)
        dec=no[0] #no func ou sub
        tipo=no[1] #tipo do no, func ou sub
        new_table=SymbolTable(table)
        init=0
        if tipo=="INTEGER":
            num=new_table.get_value(self.value)[0]/2
            return [num,"INTEGER"]
        if tipo=="FUNC":
            new_table.table[self.value] =  [None, dec.children[0].Evaluate(table)]
            init=1
        j=0
        for i in range(init, len(dec.children)-1):
            dec.children[i].Evaluate(new_table)
            argument=self.children[i-init].Evaluate(table)
            argument_value=argument[0]
            argument_type=argument[1]
            parameter_type=dec.children[i].children[1].Evaluate(table)  #new_table.get_value(argument_type)
            if argument_type!=parameter_type:
                raise Exception("tipos errados")
            new_table.set_value(dec.children[i].children[0].value,argument_value)
            j+=1
        if (j) != len(self.children):
            raise Exception("quantidade de argumentos distintos")
        dec.children[-1].Evaluate(new_table)
        if tipo=="FUNC":
            return new_table.get_value(self.value)