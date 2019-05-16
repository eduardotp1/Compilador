from token import *
from tokenizer import *
from prePro import *
from node import *

class Parser:

    def parseProgram():
        if Parser.tokens.actual.type=='SUB':
            t=Parser.tokens.selectNext()
            if Parser.tokens.actual.type=='MAIN':
                t=Parser.tokens.selectNext()
                if Parser.tokens.actual.type=='OPEN_PAR':
                    t=Parser.tokens.selectNext()
                    if Parser.tokens.actual.type=='CLOSE_PAR':
                        t=Parser.tokens.selectNext()
                        if Parser.tokens.actual.type=='BREAK':
                            t=Parser.tokens.selectNext()
                            list_of_children=[]
                            while Parser.tokens.actual.type!='END':
                                list_of_children.append(Parser.parseStatement())
                                if Parser.tokens.actual.type=='BREAK':
                                    t=Parser.tokens.selectNext()
                            t=Parser.tokens.selectNext()
                            if Parser.tokens.actual.type=='SUB':
                                t=Parser.tokens.selectNext()
                                return StatementsNode("STATEMENTS",list_of_children)
                            else:
                                raise Exception("Must insert a SUB at the end.")
                        else:
                            raise Exception("Must break line.")
                    else:
                        raise Exception("Must close parenthesis.")
                else:
                    raise Exception("Must open parenthesis.")
            else:
                raise Exception("Must insert MAIN in the begin.")
        else:
            raise Exception("Must insert SUB in the begin.")


    def parseStatement():
        if Parser.tokens.actual.type=='IDENTIFIER':
            variavel=IdentifierNode(Parser.tokens.actual.value,[])
            t=Parser.tokens.selectNext()

            if Parser.tokens.actual.type=='EQUAL':
                t=Parser.tokens.selectNext()
                return AssignmentOp("=",[variavel,Parser.parseRelExpression()])
            else:
                raise Exception("Must define a value for the variable.")


        if Parser.tokens.actual.type=='PRINT':
            t=Parser.tokens.selectNext()
            return PrintNode("PRINT",[Parser.parseRelExpression()])


        if Parser.tokens.actual.type=='IF':
            children=[]
            t=Parser.tokens.selectNext()
            condicao=Parser.parseRelExpression()
            children.append(condicao)
            if Parser.tokens.actual.type=='THEN':
                t=Parser.tokens.selectNext()
                if Parser.tokens.actual.type=='BREAK':
                    t=Parser.tokens.selectNext()
                    verdade=[]
                    while Parser.tokens.actual.type!='END' and Parser.tokens.actual.type!='ELSE':
                        verdade.append(Parser.parseStatement())
                        if Parser.tokens.actual.type=='BREAK':
                            t=Parser.tokens.selectNext()
                    verdades=StatementsNode("STATEMENTS",verdade)
                    children.append(verdades)
                    if Parser.tokens.actual.type=='ELSE':
                        t=Parser.tokens.selectNext()
                        if Parser.tokens.actual.type=='BREAK':
                            t=Parser.tokens.selectNext()
                            mentira=[]
                            while Parser.tokens.actual.type!='END':
                                mentira.append(Parser.parseStatement())
                                if Parser.tokens.actual.type=='BREAK':
                                    t=Parser.tokens.selectNext()
                            mentiras=StatementsNode("STATEMENTS",mentira)
                            children.append(mentiras)                                
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
                verdade=[]
                while Parser.tokens.actual.type!='WEND':
                    verdade.append(Parser.parseStatement())
                    if Parser.tokens.actual.type=='BREAK':
                        t=Parser.tokens.selectNext()
                verdades=StatementsNode("STATEMENTS",verdade)
                if Parser.tokens.actual.type=='WEND':
                    t=Parser.tokens.selectNext()
                    return WhileNode("WHILE",[condicao,verdades])
        

        if Parser.tokens.actual.type=='DIM':
            t=Parser.tokens.selectNext()
            if Parser.tokens.actual.type=='IDENTIFIER':
                variavel=IdentifierNode(Parser.tokens.actual.value,[])
                t=Parser.tokens.selectNext()
                if Parser.tokens.actual.type=='AS':
                    t=Parser.tokens.selectNext()
                    tipo=Parser.parseType()
                    return VarDec("vardec", [variavel, tipo])
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
        elif Parser.tokens.actual.type == 'TRUE' or Parser.tokens.actual.type == 'FALSE':
            res = BooleanVal(Parser.tokens.actual.value, [])
            t = Parser.tokens.selectNext()
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
            res=Parser.parseRelExpression()
            if Parser.tokens.actual.type=='CLOSE_PAR':
                t=Parser.tokens.selectNext()
                return res
            else:
                raise Exception("Didn't close parenthesis. ")
        else:
            raise Exception("Unexpected token.")


    def parseType():
        if Parser.tokens.actual.type=="INTEGER":
            t=Parser.tokens.selectNext()
            return TypeNode('INTEGER', [])
        if Parser.tokens.actual.type=="BOOLEAN":
            t=Parser.tokens.selectNext()
            return TypeNode('BOOLEAN', [])


    def run(code):
        code=PrePro.filter(code)
        Parser.tokens=Tokenizer(code)
        t=Parser.tokens.selectNext()
        res=Parser.parseProgram()

        while Parser.tokens.actual.type == "BREAK":
            Parser.tokens.selectNext()

        if Parser.tokens.actual.type == 'EOF':
            return res
        else:
            raise Exception("Unexpected token.")