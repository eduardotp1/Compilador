from token import *
from tokenizer import *
from prePro import *
from node import *

class Parser:
    def parseStatements():
        if Parser.tokens.actual.type=='BEGIN':
            t=Parser.tokens.selectNext()
            if Parser.tokens.actual.type=='BREAK':
                t=Parser.tokens.selectNext()
                list_of_children=[]
                while Parser.tokens.actual.type!='END':
                    list_of_children.append(Parser.parseStatement())
                    if Parser.tokens.actual.type=='BREAK':
                        t=Parser.tokens.selectNext()
                    else:
                        raise Exception("Didn't break line. Column:"+str(Parser.tokens.position))
                t=Parser.tokens.selectNext()
                res = StatementsNode("STATEMENTS",list_of_children)
                return res
            else:
                raise Exception("Didn't break line. Column:"+str(Parser.tokens.position))
        else:
            raise Exception("Didn't start code with a Begin. Column:"+str(Parser.tokens.position))


    def parseStatement():
        if Parser.tokens.actual.type=='IDENTIFIER':
            variavel=IdentifierNode(Parser.tokens.actual.value,[])
            t=Parser.tokens.selectNext()
            if Parser.tokens.actual.type=='ASSIGMENT':
                t=Parser.tokens.selectNext()
                res = AssigmentOp("=",[variavel,Parser.parseExpression()])
                return res
            else:
                raise Exception("Must define a value for the variable. Column:"+str(Parser.tokens.position))
        if Parser.tokens.actual.type=='PRINT':
            t=Parser.tokens.selectNext()
            res=PrintNode("PRINT",[Parser.parseExpression()])
            return res
        if Parser.tokens.actual.type=='BEGIN':
            res=Parser.parseStatements()
            return res
        else:
            return NoOp(None,None)
        


    def parseExpression():
        res=Parser.parseTerm()
        while Parser.tokens.actual.type=='PLUS' or Parser.tokens.actual.type=='MINUS':
            if Parser.tokens.actual.type=='PLUS':
                t=Parser.tokens.selectNext()
                res = BinOp("+",[res,Parser.parseTerm()])
            elif Parser.tokens.actual.type=='MINUS':
                t=Parser.tokens.selectNext()
                res = BinOp("-",[res,Parser.parseTerm()])
        return res

    def parseTerm():
        res=Parser.parseFactor()
        while Parser.tokens.actual.type=='MULT' or Parser.tokens.actual.type=='DIV':
            if Parser.tokens.actual.type=='DIV':
                t=Parser.tokens.selectNext()
                res = BinOp("/",[res,Parser.parseFactor()])
            elif Parser.tokens.actual.type=='MULT':
                t=Parser.tokens.selectNext()
                res = BinOp("*",[res,Parser.parseFactor()])
        return res

    def parseFactor():
        if Parser.tokens.actual.type=='INT':
            res=IntVal(Parser.tokens.actual.value,[])
            t=Parser.tokens.selectNext()
            return res
        elif Parser.tokens.actual.type=='IDENTIFIER':
            res=IdentifierNode(Parser.tokens.actual.value,[])
            t=Parser.tokens.selectNext()
            return res
        elif Parser.tokens.actual.type=='PLUS':
            res=UnOp("+",[Parser.parseFactor()])
            t=Parser.tokens.selectNext()
            return res
        elif Parser.tokens.actual.type=='MINUS':
            res=UnOp("-",[Parser.parseFactor()])
            t=Parser.tokens.selectNext()
            return res

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
        return (Parser.parseStatements())
