from token import Token
from tokenizer import Tokenizer
from prePro import PrePro

class Parser:
    def parseExpression():
        res=Parser.parseTerm()
        t=Parser.tokens.actual
        while t.type=='PLUS' or t.type=='MINUS':
            if t.type=='PLUS':
                t=Parser.tokens.selectNext()
                res+=Parser.parseTerm()
            elif t.type=='MINUS':
                t=Parser.tokens.selectNext()
                res-=Parser.parseTerm()
        return res

    def parseTerm(): 
        res_term=0
        if Parser.tokens.actual.type== 'INT':
            res_term+=Parser.tokens.actual.value
            t=Parser.tokens.selectNext()
            while t.type=='MULT' or t.type=='DIV':
                if t.type=='DIV':
                    t=Parser.tokens.selectNext()
                    if t.type=='INT':
                        res_term//=t.value
                    else:
                        raise Exception('It must have an integer')
                elif t.type=='MULT':
                    t=Parser.tokens.selectNext()
                    if t.type=='INT':
                        res_term*=t.value
                    else:
                        raise Exception('It must have an integer')
                t=Parser.tokens.selectNext()
        else:
            raise Exception('It must be an integer')
        return res_term


    def run(code):
        code=PrePro.filter(code)
        Parser.tokens=Tokenizer(code)
        t=Parser.tokens.selectNext()
        return (Parser.parseExpression())
