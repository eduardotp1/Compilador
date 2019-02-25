from token import Token
from tokenizer import Tokenizer

class Parser:
    def parseExpression():
        res=0
        t=Parser.tokens.selectNext()
        if t.type== 'INT':
            res=t.value
            t=Parser.tokens.selectNext()
            while t.type=='PLUS' or t.type=='MINUS' or t.type=='MULT' or t.type=='DIV' :
                if t.type=='PLUS':
                    t=Parser.tokens.selectNext()
                    if t.type=='INT':
                        res+=t.value
                    else:
                        raise Exception('It must be an integer')
                if t.type=='MINUS':
                    t=Parser.tokens.selectNext()
                    if t.type=='INT':
                        res-=t.value
                    else:
                        raise Exception('It must be an integer')
                if t.type=='DIV':
                    t=Parser.tokens.selectNext()
                    if t.type=='INT':
                        res/=t.value
                    else:
                        raise Exception('It must be an integer')
                if t.type=='MULT':
                    t=Parser.tokens.selectNext()
                    if t.type=='INT':
                        res*=t.value
                    else:
                        raise Exception('It must be an integer')
                t=Parser.tokens.selectNext()
        else:
            raise Exception('Error')
        return res
        
    
    def run(code):
        Parser.tokens=Tokenizer(code)
        print(Parser.parseExpression())
