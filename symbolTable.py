class SymbolTable:
    def __init__(self):
        self.table={}
        self.index=0

    def get_value(self,variavel):
        if variavel in self.table.keys():
            if self.table[variavel][0]==None:
                raise Exception("Variable doesn't have value")
            return self.table[variavel]
        else:
            raise Exception("Variable doesn't exist")

    def set_value(self, variavel, value):
        self.table[variavel][0]=value[0]

    def set_type(self, variavel,tipo):
        if variavel in self.table:
            raise Exception("Variavel ja existe")
        else:
            self.index += 4
            self.table[variavel]=[None,tipo,self.index]