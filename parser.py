from token import Token
from tokenizer import Tokenizer
from prePro import PrePro

class Parser:
    def parseExpression():
        res=Parser.parseTerm()
        while Parser.tokens.actual.type=='PLUS' or Parser.tokens.actual.type=='MINUS':
            if Parser.tokens.actual.type=='PLUS':
                t=Parser.tokens.selectNext()
                res+=Parser.parseTerm()
            elif Parser.tokens.actual.type=='MINUS':
                t=Parser.tokens.selectNext()
                res-=Parser.parseTerm()
        return res

    def parseTerm():
        res=Parser.parseFactor()
        while Parser.tokens.actual.type=='MULT' or Parser.tokens.actual.type=='DIV':
            if Parser.tokens.actual.type=='DIV':
                t=Parser.tokens.selectNext()
                res//=Parser.parseFactor()
            elif Parser.tokens.actual.type=='MULT':
                t=Parser.tokens.selectNext()
                res*=Parser.parseFactor()
        return res

    def parseFactor():
        if Parser.tokens.actual.type=='INT':
            res=Parser.tokens.actual.value
            t=Parser.tokens.selectNext()
            return res
        elif Parser.tokens.actual.type=='PLUS':
            t=Parser.tokens.selectNext()
            return (+Parser.parseFactor())
        elif Parser.tokens.actual.type=='MINUS':
            t=Parser.tokens.selectNext()
            return (-Parser.parseFactor())

        elif Parser.tokens.actual.type=='OPEN_PAR':
            t=Parser.tokens.selectNext()
            res=Parser.parseExpression()
            if Parser.tokens.actual.type=='CLOSE_PAR':
                t=Parser.tokens.selectNext()
                return res
            else:
                raise Exception("Didn't close parenthesis. Column:"+str(Parser.tokens.position))
        else:
            raise Exception("Unexpected token. Column:"+str(Parser.tokens.position))


    def run(code):
        code=PrePro.filter(code)
        Parser.tokens=Tokenizer(code)
        t=Parser.tokens.selectNext()
        return (Parser.parseExpression())
