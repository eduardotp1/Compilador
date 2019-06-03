from token import *
from tokenizer import *
from prePro import *
from node import *

class Parser:
    
    def parseProgram():
        children=[]
        while Parser.tokens.actual.type!='EOF':
            if Parser.tokens.actual.type=='SUB':
                res=Parser.parseSubDec()
                children.append(res)
            if Parser.tokens.actual.type=='FUNCTION':
                res=Parser.parseFuncDec()
                children.append(res)
            while Parser.tokens.actual.type=='BREAK':
                t=Parser.tokens.selectNext()
        children.append(Call("MAIN",[]))
        return StatementsNode("root",children)

    def parseSubDec():
        if Parser.tokens.actual.type=='SUB':
            t=Parser.tokens.selectNext()
            if Parser.tokens.actual.type=='IDENTIFIER':
                name= Parser.tokens.actual.value
                t=Parser.tokens.selectNext()
                if Parser.tokens.actual.type=='OPEN_PAR':
                    t=Parser.tokens.selectNext()
                    children=[]
                    while Parser.tokens.actual.type=='COMMA' or Parser.tokens.actual.type!='CLOSE_PAR':
                        if Parser.tokens.actual.type=='COMMA':
                            t=Parser.tokens.selectNext()
                            if Parser.tokens.actual.type=='IDENTIFIER':
                                variavel=IdentifierNode(Parser.tokens.actual.value,[])
                                t=Parser.tokens.selectNext()
                                if Parser.tokens.actual.type=='AS':
                                    t=Parser.tokens.selectNext()
                                    tipo=Parser.parseType()
                        else:
                            if Parser.tokens.actual.type=='IDENTIFIER':
                                variavel=IdentifierNode(Parser.tokens.actual.value,[])
                                t=Parser.tokens.selectNext()
                                if Parser.tokens.actual.type=='AS':
                                    t=Parser.tokens.selectNext()
                                    tipo=Parser.parseType()
                        children.append(VarDec("vardec", [variavel, tipo]))
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
                                stmnts = StatementsNode("STATEMENTS",list_of_children)
                                children.append(stmnts)
                                return SubDec(name,children)

                            else:
                                raise Exception("Must insert a SUB at the end.")
                        else:
                            raise Exception("Must break line.")
                    else:
                        raise Exception("Must close parenthesis.")
                else:
                    raise Exception("Must open parenthesis.")
            else:
                raise Exception("Must insert IDENTIFIER in the begin.")
        else:
            raise Exception("Must insert SUB in the begin.")


    def parseFuncDec():
        if Parser.tokens.actual.type=='FUNCTION':
            t=Parser.tokens.selectNext()
            if Parser.tokens.actual.type=='IDENTIFIER':
                name= Parser.tokens.actual.value
                t=Parser.tokens.selectNext()
                if Parser.tokens.actual.type=='OPEN_PAR':
                    t=Parser.tokens.selectNext()
                    children=[]
                    while Parser.tokens.actual.type=='COMMA' or Parser.tokens.actual.type!='CLOSE_PAR':
                        if Parser.tokens.actual.type=='COMMA':
                            t=Parser.tokens.selectNext()
                            if Parser.tokens.actual.type=='IDENTIFIER':
                                variavel=IdentifierNode(Parser.tokens.actual.value,[])
                                t=Parser.tokens.selectNext()
                                if Parser.tokens.actual.type=='AS':
                                    t=Parser.tokens.selectNext()
                                    tipo=Parser.parseType()
                                else:
                                    raise Exception("Must declare type")
                        else:
                            if Parser.tokens.actual.type=='IDENTIFIER':
                                variavel=IdentifierNode(Parser.tokens.actual.value,[])
                                t=Parser.tokens.selectNext()
                                if Parser.tokens.actual.type=='AS':
                                    t=Parser.tokens.selectNext()
                                    tipo=Parser.parseType()
                                else:
                                    raise Exception("Must declare type")
                        children.append(VarDec("vardec", [variavel, tipo]))
                    if Parser.tokens.actual.type=='CLOSE_PAR':
                        t=Parser.tokens.selectNext()
                        if Parser.tokens.actual.type=='AS':
                            t=Parser.tokens.selectNext()
                            tipo=Parser.parseType()
                            children.insert(0, tipo)
                            if Parser.tokens.actual.type=='BREAK':
                                t=Parser.tokens.selectNext()
                                list_of_children=[]
                                while Parser.tokens.actual.type!='END':
                                    list_of_children.append(Parser.parseStatement())
                                    if Parser.tokens.actual.type=='BREAK':
                                        t=Parser.tokens.selectNext()
                                t=Parser.tokens.selectNext()
                                if Parser.tokens.actual.type=='FUNCTION':
                                    t=Parser.tokens.selectNext()
                                    stmnts = StatementsNode("STATEMENTS",list_of_children)
                                    children.append(stmnts)
                                    return FuncDec(name,children)

                                else:
                                    raise Exception("Must insert a SUB at the end.")
                            else:
                                raise Exception("Must break line.")
                    else:
                        raise Exception("Must close parenthesis.")
                else:
                    raise Exception("Must open parenthesis.")
            else:
                raise Exception("Must insert IDENTIFIER in the begin.")
        else:
            raise Exception("Must insert FUNCTIONTION in the begin.")


    def parseStatement():
        if Parser.tokens.actual.type=='IDENTIFIER':
            variavel=IdentifierNode(Parser.tokens.actual.value,[])
            t=Parser.tokens.selectNext()
            if Parser.tokens.actual.type=='EQUAL':
                t=Parser.tokens.selectNext()
                return AssigmentOp("=",[variavel,Parser.parseRelExpression()])
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


        if Parser.tokens.actual.type == 'CALL':
            t=Parser.tokens.selectNext()
            if Parser.tokens.actual.type == 'IDENTIFIER':
                variavel = Parser.tokens.actual.value
                t=Parser.tokens.selectNext()
                if Parser.tokens.actual.type == 'OPEN_PAR':
                    t=Parser.tokens.selectNext()
                    children = []
                    while Parser.tokens.actual.type != 'CLOSE_PAR':
                        if Parser.tokens.actual.type == 'COMMA':
                            t=Parser.tokens.selectNext()
                            children.append(Parser.parseRelExpression())
                        else:
                            children.append(Parser.parseRelExpression())
                    if Parser.tokens.actual.type == 'CLOSE_PAR':
                        Parser.tokens.selectNext()
                        return Call(variavel, children)
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
        while Parser.tokens.actual.type=='PLUS' or Parser.tokens.actual.type=='MINUS' or Parser.tokens.actual.type=='OR':
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
        while Parser.tokens.actual.type=='MULT' or Parser.tokens.actual.type=='DIV' or Parser.tokens.actual.type=='AND':
            if Parser.tokens.actual.type=='DIV':
                t=Parser.tokens.selectNext()
                res = BinOp("/",[res,Parser.parseFactor()])
            elif Parser.tokens.actual.type=='MULT':
                t=Parser.tokens.selectNext()
                res = BinOp("*",[res,Parser.parseFactor()])
            elif Parser.tokens.actual.type=='AND':
                t=Parser.tokens.selectNext()
                res1=Parser.parseFactor()
                res = BinOp("and",[res,res1])
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
            variavel = Parser.tokens.actual.value
            t=Parser.tokens.selectNext()
            if Parser.tokens.actual.type=="OPEN_PAR":
                t=Parser.tokens.selectNext()
                children=[]
                while Parser.tokens.actual.type != 'CLOSE_PAR':
                    if Parser.tokens.actual.type == 'COMMA':
                        t=Parser.tokens.selectNext()
                        children.append(Parser.parseRelExpression())
                    else:
                        children.append(Parser.parseRelExpression())
                if Parser.tokens.actual.type == 'CLOSE_PAR':
                    Parser.tokens.selectNext()
                    return Call(variavel, children)
            res=IdentifierNode(variavel,[])
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
        elif Parser.tokens.actual.type == 'NOT':
            t = Parser.tokens.selectNext()
            return UnOp("NOT", [Parser.parseFactor()])
        elif Parser.tokens.actual.type == 'TRUE' or Parser.tokens.actual.type == 'FALSE':
            res = Boolean(actual.value, [])
            t = Parser.tokens.selectNext()
            return res
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