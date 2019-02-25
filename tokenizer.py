from token import Token
class Tokenizer:
    def __init__(self, origin):
        self.origin=origin
        self.position=0
        self.actual=None

    def selectNext(self):
        if self.position==len(self.origin):
            self.actual=Token('EOF',"")
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
        num=""
        while  self.position<len(self.origin) and self.origin[self.position].isdigit():
            num=num+self.origin[self.position]
            self.position+=1
        self.actual=Token('INT',int(num))
        return self.actual