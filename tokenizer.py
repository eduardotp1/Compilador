# from token import Token

class Token:
    def __init__ (self, type,value):
        self.type=type
        self.value=value
    

class Tokenizer:
    def __init__(self, origin):
        self.origin=origin
        self.position=0
        self.actual=None
        self.reserved=["BEGIN","PRINT","END","IF","WHILE","ELSE","THEN","WEND","INPUT","DIM","AS","SUB","INTEGER","BOOLEAN","TRUE", "FALSE", "CALL", "FUNCTION","AND","OR","NOT"]

    def selectNext(self):
        if self.position==len(self.origin):
            self.actual=Token('EOF',"")
            return self.actual

        while self.origin[self.position]==(" "):
            self.position+=1
            if self.position==len(self.origin):
                self.actual=Token('EOF',"")
                return self.actual
        
        if self.origin[self.position]=="(":
            self.actual=Token('OPEN_PAR',"(")
            self.position+=1
            return self.actual
        
        if self.origin[self.position]==")":
            self.actual=Token('CLOSE_PAR',")")
            self.position+=1
            return self.actual

        if self.origin[self.position]=="+":
            self.actual=Token('PLUS',"+")
            self.position+=1
            return self.actual

        if self.origin[self.position]=="-":
            self.actual=Token('MINUS',"-")
            self.position+=1
            return self.actual
        if self.origin[self.position]=="/":
            self.actual=Token('DIV',"")
            self.position+=1
            return self.actual
        if self.origin[self.position]=="*":
            self.actual=Token('MULT',"*")
            self.position+=1
            return self.actual
        if self.origin[self.position]=="'":
            self.actual=Token('COM',"'")
            self.position+=1
            return self.actual 
        if self.origin[self.position]=="=":
            self.actual=Token('EQUAL',"=")
            self.position+=1
            return self.actual 

        if self.origin[self.position]=="<":
            self.actual=Token('SMALLER',"<")
            self.position+=1
            return self.actual 

        if self.origin[self.position]==">":
            self.actual=Token('BIGGER',">")
            self.position+=1
            return self.actual 

        if self.origin[self.position]=="\n":
            self.actual=Token('BREAK',"\n")
            self.position+=1
            return self.actual 

        if self.origin[self.position]==",":
            self.actual=Token('COMMA',",")
            self.position+=1
            return self.actual 


        num=""
        while self.position<len(self.origin) and self.origin[self.position].isdigit():
            num=num+self.origin[self.position]
            self.position+=1
        if num!="":

            self.actual=Token('INT',int(num))
            return self.actual
        
        identifier=""
        while  self.position<len(self.origin)-2:
            if self.origin[self.position].isalpha():
                identifier=identifier+self.origin[self.position]
                self.position+=1
                if self.position<len(self.origin)-1 and self.origin[self.position] == "_" or self.origin[self.position].isdigit() or self.origin[self.position].isalpha():
                    identifier=identifier+self.origin[self.position]
                    self.position+=1
                else:
                    break
            else:
                break
        identifier=identifier.upper()
        if identifier in self.reserved:
            self.actual=Token(identifier,identifier)
            return self.actual
        else:
            self.actual=Token('IDENTIFIER',identifier)
        return self.actual