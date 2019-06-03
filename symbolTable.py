class SymbolTable:
    def __init__(self,ancestor):
        self.table={}
        self.ancestor = ancestor

    def get_value(self,variavel):
        if variavel in self.table.keys():
            if self.table[variavel][0]==None:
                raise Exception("{0} doesn't have value".format(variavel))
            return self.table[variavel]
        else:
            if self.ancestor != None:
                value = self.ancestor.get_value(variavel)
                return value
            else:
                raise Exception("{0} doesn't exist".format(variavel))
        

    def get_value2(self,variavel):
        if variavel in self.table.keys():
            if self.table[variavel][0]==None:
                if self.ancestor != None:
                    value = self.ancestor.get_value2(variavel)
                    return value
                else:
                    raise Exception("{0} doesn't exist".format(variavel))
            return self.table[variavel]
        else:
            if self.ancestor != None:
                value = self.ancestor.get_value2(variavel)
                return value
            else:
                raise Exception("{0} doesn't exist".format(variavel))

    def set_value(self, variavel, value):
        self.table[variavel][0]=value

    def set_type(self, variavel,tipo):
        self.table[variavel]=[None,tipo]