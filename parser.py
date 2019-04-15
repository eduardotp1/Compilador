from token import *
from tokenizer import *
from prePro import *
from node import *

class Parser:
    def parseStatements():
        list_of_children=[]
        while Parser.tokens.actual.type!='EOF' and Parser.tokens.actual.type!='WEND' and Parser.tokens.actual.type!='END' and Parser.tokens.actual.type!='ELSE':
            list_of_children.append(Parser.parseStatement())
            
            if Parser.tokens.actual.type != 'BREAK':
                raise Exception("tem que dar break line")
            t=Parser.tokens.selectNext()
        res = StatementsNode("STATEMENTS",list_of_children)
        return res


    def parseStatement():
        if Parser.tokens.actual.type=='IDENTIFIER':
            variavel=IdentifierNode(Parser.tokens.actual.value,[])
            t=Parser.tokens.selectNext()

            if Parser.tokens.actual.type=='EQUAL':
                t=Parser.tokens.selectNext()
                res = AssigmentOp("=",[variavel,Parser.parseExpression()])
                return res
            else:
                raise Exception("Must define a value for the variable. Column:"+str(Parser.tokens.position))
        if Parser.tokens.actual.type=='PRINT':
            t=Parser.tokens.selectNext()
            res=PrintNode("PRINT",[Parser.parseExpression()])
            return res
        # if Parser.tokens.actual.type=='BEGIN':
        #     res=Parser.parseStatements()
        #     return res
        if Parser.tokens.actual.type=='IF':
            children=[]
            t=Parser.tokens.selectNext()
            condicao=Parser.parseRelExpression()
            children.append(condicao)
            if Parser.tokens.actual.type=='THEN':
                t=Parser.tokens.selectNext()
                if Parser.tokens.actual.type=='BREAK':
                    t=Parser.tokens.selectNext()
                    verdade=Parser.parseStatements()
                    children.append(verdade)
                    if Parser.tokens.actual.type=='ELSE':
                        t=Parser.tokens.selectNext()
                        if Parser.tokens.actual.type=='BREAK':
                            t=Parser.tokens.selectNext()
                            mentira=Parser.parseStatements()
                            children.append(mentira)
                    if Parser.tokens.actual.type=='END':
                        t=Parser.tokens.selectNext()
                        if Parser.tokens.actual.type=='IF':
                            t=Parser.tokens.selectNext()
                            return IfNode("IF",children)

        if Parser.tokens.actual.type=='WHILE':
            t=Parser.tokens.selectNext()
            condicao=Parser.parseRelExpression()
            if Parser.tokens.actual.type=='BREAK':
                t=Parser.tokens.selectNext()
                verdade=Parser.parseStatements()
                if Parser.tokens.actual.type=='WEND':
                    t=Parser.tokens.selectNext()
                    return WhileNode("WHILE",[condicao,verdade])
        else:
            return NoOp(None,None)
        

    def parseRelExpression():
        res=Parser.parseExpression()
        if Parser.tokens.actual.type=='EQUAL':
            t=Parser.tokens.selectNext()
            res = BinOp("=",[res,Parser.parseExpression()])
        elif Parser.tokens.actual.type=='BIGGER':
            t=Parser.tokens.selectNext()
            res = BinOp(">",[res,Parser.parseExpression()])
        elif Parser.tokens.actual.type=='SMALLER':
            t=Parser.tokens.selectNext()
            res = BinOp("<",[res,Parser.parseExpression()])
        return res

    def parseExpression():
        res=Parser.parseTerm()
        while Parser.tokens.actual.type=='PLUS' or Parser.tokens.actual.type=='MINUS':
            if Parser.tokens.actual.type=='PLUS':
                t=Parser.tokens.selectNext()
                res = BinOp("+",[res,Parser.parseTerm()])
            elif Parser.tokens.actual.type=='MINUS':
                t=Parser.tokens.selectNext()
                res = BinOp("-",[res,Parser.parseTerm()])
            elif Parser.tokens.actual.type=='OR':
                t=Parser.tokens.selectNext()
                res = BinOp("or",[res,Parser.parseTerm()])
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
            elif Parser.tokens.actual.type=='AND':
                t=Parser.tokens.selectNext()
                res = BinOp("and",[res,Parser.parseFactor()])
        return res

    def parseFactor():
        if Parser.tokens.actual.type=='INT':
            res=IntVal(Parser.tokens.actual.value,[])
            t=Parser.tokens.selectNext()
            return res
        elif Parser.tokens.actual.type=='INPUT':
            res = InputNode(Parser.tokens.actual.value, [])
            t=Parser.tokens.selectNext()
            return res
        elif Parser.tokens.actual.type=='IDENTIFIER':
            res=IdentifierNode(Parser.tokens.actual.value,[])
            t=Parser.tokens.selectNext()
            return res
        elif Parser.tokens.actual.type=='PLUS':
            t=Parser.tokens.selectNext()
            res=UnOp("+",[Parser.parseFactor()])
            return res
        elif Parser.tokens.actual.type=='MINUS':
            t=Parser.tokens.selectNext()
            res=UnOp("-",[Parser.parseFactor()])
            return res
        elif Parser.tokens.actual.type=='PLUS':
            t=Parser.tokens.selectNext()
            res=UnOp("+",[Parser.parseFactor()])
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
        res=Parser.parseStatements()

        if Parser.tokens.actual.type == 'EOF':
            return res
        else:
            raise Exception("Unexpected token. Column:"+str(Parser.tokens.position))