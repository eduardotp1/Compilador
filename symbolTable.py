class SymbolTable:
    def __init__(self):
        self.table={}

    def get_value(self,variavel):
        if variavel in self.table.keys():
            return self.table[variavel]
        else:
            raise Exception("Variable doesn't exist")

    def set_value(self, variavel, value):
        self.table[variavel]=value