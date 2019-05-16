from writer import *
class Node:
    i=-1
    def Evaluate(self,table):
        pass
    @staticmethod
    def newId():
        Node.i+=1
        return Node.i

class BinOp(Node):
    def __init__ (self, value,children):
        self.value=value
        self.children=children
        self.id=Node.newId()
    def Evaluate(self,table):
        x=self.children[0].Evaluate(table)
        Writer.Write("PUSH EBX\n")
        y=self.children[1].Evaluate(table)
        Writer.Write("POP EAX\n")
        if x[1]==y[1]=="INTEGER":
            if self.value=="+":
                Writer.Write("ADD EAX, EBX\n")
                Writer.Write("MOV EBX, EAX\n")
                return [(x[0]+y[0]),"INTEGER"]
            if self.value=="-":
                Writer.Write("SUB EAX, EBX\n")
                Writer.Write("MOV EBX, EAX\n")
                return [(x[0]-y[0]),"INTEGER"]
            if self.value=="*":
                Writer.Write("IMUL EAX, EBX\n")
                Writer.Write("MOV EBX, EAX\n")
                return [(x[0]*y[0]),"INTEGER"]
            if self.value=="/":
                Writer.Write("IDIV EAX, EBX\n")
                Writer.Write("MOV EBX, EAX\n")
                return [(x[0]//y[0]),"INTEGER"]
            if self.value=="<":
                Writer.Write("CMP EAX, EBX\n")
                Writer.Write("CALL binop_jl\n")
                if ((x[0]<y[0])):
                    return [True,"BOOLEAN"]
                else:
                    return [False,"BOOLEAN"]
            if self.value==">":
                Writer.Write("CMP EAX, EBX\n")
                Writer.Write("CALL BINOP_JG\n")
                if ((x[0]>y[0])):
                    return [True,"BOOLEAN"]
                else:
                    return [False,"BOOLEAN"]
            if self.value=="=":
                Writer.Write("CMP EAX, EBX\n")
                Writer.Write("CALL binop_je\n")
                if ((x[0]==y[0])):
                    return [True,"BOOLEAN"]
                else:
                    return [False,"BOOLEAN"]

            if x[1]==y[1]=="BOOLEAN":
                if self.value == 'and':
                    Writer.Write("AND EAX, EBX\n")
                    Writer.Write("MOV EBX, EAX\n")
                    return [x[0] and y[0], "BOOLEAN"]
                if self.value == 'or':
                    Writer.Write("OR EAX, EBX\n")
                    Writer.Write("MOV EBX, EAX\n")
                    return [x[0] or y[0], "BOOLEAN"]

            raise Exception("Can't operate with two different types")

class UnOp(Node):
    def __init__ (self, value,children):
        self.value=value
        self.children=children
        self.id=Node.newId()
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
        self.id=Node.newId()
    def Evaluate(self,table):
        Writer.Write("MOV EBX,{0}\n".format(self.value))
        return [self.value, "INTEGER"]

class NoOp(Node):
    def __init__ (self, value,children):
        self.value=value
        self.children=children
        self.id=Node.newId()

class IdentifierNode(Node):
    def __init__ (self, value,children):
        self.value=value
        self.children=children
        self.id=Node.newId()

    def Evaluate(self,table):
        Writer.Write("MOV EBX, [EBP - {0}]\n".format(table.get_value(self.value)[2]))
        return (table.get_value(self.value))

class AssignmentOp(Node):
    def __init__ (self, value,children):
        self.value=value
        self.children=children
        self.id=Node.newId()
    def Evaluate(self,table):
        if self.children[0].value not in table.table:
            raise Exception("The variable is not declared")
        valor=self.children[1].Evaluate(table)
        if table.table[self.children[0].value][1]==valor[1]:
            table.set_value(self.children[0].value, valor)
            Writer.Write("MOV [EBP - {0}], EBX ; {1} = {2}\n".format(table.get_value(self.children[0].value)[2],self.children[0].value, valor[0]))
            

        else:
            raise Exception("The type of the value is not the type of the variable")

class TypeNode(Node):
    def __init__ (self, value,children):
        self.value=value
        self.children=children
        self.id=Node.newId()
    def Evaluate(self,table):
        return self.value

class PrintNode(Node):
    def __init__ (self, value,children):
        self.value=value
        self.children=children
        self.id=Node.newId()
    def Evaluate(self,table):
        print(self.children[0].Evaluate(table)[0])
        Writer.Write("PUSH EBX\n")
        Writer.Write("CALL print\n")
        Writer.Write("POP EBX\n")

class StatementsNode(Node):
    def __init__ (self, value,children):
        self.value=value
        self.children=children
        self.id=Node.newId()
    def Evaluate(self,table):
        for i in self.children:
            i.Evaluate(table)

class WhileNode(Node):
    def __init__ (self, value,children):
        self.value=value
        self.children=children
        self.id=Node.newId()
    def Evaluate(self,table):
        Writer.Write("LOOP_{0}:\n".format(self.id))
        if self.children[0].Evaluate(table)[1]!="BOOLEAN":
            raise Exception("Type must be boolean")
        Writer.Write("CMP EBX, False\n")
        Writer.Write("JE EXIT_{0}\n".format(self.id))
        # while self.children[0].Evaluate(table)[0]:
        self.children[1].Evaluate(table)
        Writer.Write("JMP LOOP_{0}\n".format(self.id))
        Writer.Write("EXIT_{0}:\n".format(self.id))

class IfNode(Node):
    def __init__ (self, value,children):
        self.value=value
        self.children=children
        self.id=Node.newId()
    def Evaluate(self,table):
        if self.children[0].Evaluate(table)[1]!="BOOLEAN":
            raise Exception("Type must be boolean")
        Writer.Write("CMP EBX, False\n")
        Writer.Write("JE ELSE_{0}\n".format(self.id))
        # if self.children[0].Evaluate(table)[0]:
        self.children[1].Evaluate(table)
        Writer.Write("ELSE_{0}:\n".format(self.id))
        # else:
        if len(self.children) == 3:
            self.children[2].Evaluate(table)

class InputNode(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id=Node.newId()

    def Evaluate(self, table):
        return [int(input()), "INTEGER"]

class VarDec(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id=Node.newId()

    def Evaluate(self,  table):
        table.set_type(self.children[0].value, self.children[1].value)
        Writer.Write("PUSH DWORD 0\n")

class BooleanVal(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id=Node.newId()

    def Evaluate(self,  table):
        b=0
        if self.value:
            b=1
        Writer.Write("MOV EBX,{0}\n".format(b))        
        return [self.value, "BOOLEAN"]

    