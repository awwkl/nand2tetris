current_token_number = 0
tokens = []
parsed_tokens = []

def compileTokens(token_list):
    global tokens, parsed_tokens, current_token_number

    current_token_number = 0                                # need to reset because there are multiple .jack files
    tokens = token_list                                     # compileTokens will be called multiple times
    parsed_tokens = []

    compile_class()
    return parsed_tokens

def compile_class():
    global tokens, parsed_tokens, current_token_number

    add_token("<class>")


    compile_token()     # class
    compile_token()     # className
    compile_token()     # {

    while (get_current_token() in ["static", "field"]):
        compile_classVarDec()
    
    while (get_current_token() in ["constructor", "function", "method"]):
        compile_subroutineDec()

    compile_token()     # {
        
    add_token("</class>")


def compile_classVarDec():
    add_token("<classVarDec>")

    compile_token()     # static / field
    compile_token()     # type
    compile_token()     # varName

    while (not get_current_token() == ";"):
        compile_token()

    compile_token()     # ;

    add_token("</classVarDec>")

def compile_subroutineDec():
    add_token("<subroutineDec>")

    compile_token()                 # constructor / function / method
    compile_token()                 # void / type    
    compile_token()                 # subroutineName

    compile_token()                 # (
    compile_parameterList()
    compile_token()                 # )

    compile_subroutineBody()

    add_token("</subroutineDec>")

def compile_parameterList():
    add_token("<parameterList>")

    while (not get_current_token() == ")"):
        compile_token()

    add_token("</parameterList>")
    
def compile_subroutineBody():
    add_token("<subroutineBody>")

    compile_token()                 # {

    while (get_current_token() == "var"):
        compile_varDec()            # varDec*

    compile_statements()

    compile_token()                 # }

    add_token("</subroutineBody>")

def compile_varDec():
    add_token("<varDec>")

    while (not get_current_token() == ";"):
        compile_token()
    
    compile_token()                 # ;

    add_token("</varDec>")

def compile_statements():
    add_token("<statements>")

    # while (get_current_token() in ["let", "if", "while", "do", "return"]):
    while (get_current_token() in ["let", "do", "return", "if", "while"]):
        compile_statement()

    add_token("</statements>")

def compile_statement():
    token = get_current_token()

    if token == "let":
        compile_letStatement()
    elif token == "if":
        compile_ifStatement()
    elif token == "while":
        compile_whileStatement()
    elif token == "do":
        compile_doStatement()
    elif token == "return":
        compile_returnStatement()

def compile_letStatement():
    add_token("<letStatement>")


    compile_token()                 # let
    compile_token()                 # varName

    if (get_current_token() == "["):
        compile_arrayIndex()

    compile_token()                 # =

    compile_expression()            # expression

    compile_token()                 # ;

    add_token("</letStatement>")

def compile_doStatement():
    add_token("<doStatement>")

    compile_token()                 # do
    
    compile_subroutineCall()

    compile_token()                 # ;

    add_token("</doStatement>")

def compile_subroutineCall():
    while (not get_current_token() == ";"):
        if get_current_token() == "(":
            compile_token()
            compile_expressionList()

        compile_token()

def compile_ifStatement():
    add_token("<ifStatement>")

    compile_token()         # if
    compile_token()         # (

    compile_expression()    

    compile_token()         # )

    compile_token()         # {
    compile_statements()
    compile_token()         # }

    if (get_current_token() == "else"):
        compile_token()         # else
        compile_token()         # {
        compile_statements()
        compile_token()         # }

    add_token("</ifStatement>")
    
def compile_whileStatement():
    add_token("<whileStatement>")

    compile_token()         # while
    compile_token()         # (

    compile_expression()    

    compile_token()         # )

    compile_token()         # {
    compile_statements()
    compile_token()         # }

    add_token("</whileStatement>")

def compile_returnStatement():
    add_token("<returnStatement>")

    compile_token()         # return
    if (not get_current_token() == ";"):
        compile_expression()
        
    compile_token()
    add_token("</returnStatement>")


def compile_expression():
    add_token("<expression>")

    compile_term()

    while (get_current_token() in operator_list):
        compile_token()     # op
        compile_term()      # term

    # while (not get_current_token() in [",", "]", ")", ";"]):
    #     compile_term()
    #     if (get_current_token() in operator_list):
    #         compile_token()

    add_token("</expression>")

def compile_arrayIndex():
    compile_token()             # <symbol> [ </symbol>
    add_token("<expression>")
    add_token("<term>")
    compile_token()               # <integerConstant> 1 </integerConstant>
    add_token("</term>")
    add_token("</expression>")
    compile_token()             # <symbol> ] </symbol>

def compile_term():
    add_token("<term>")
    lookahead_type = "array_entry"      # default compile 

    if (get_current_token() in ["-", "~"]): #unary operators
        compile_token()
        compile_term()

    while (not get_current_token() in operator_list):
        if get_current_token() in [",", ";", "}", ")"]:
            break

        if get_current_token() == "]":
            compile_token()
            break

        if get_current_token() == ".":
            lookahead_type = "subroutine_call"

        if get_current_token() == "[":
            compile_arrayIndex()
            break

        if get_current_token() == "(":
            compile_token()

            if lookahead_type == "subroutine_call":
                compile_expressionList()
            else:
                compile_expression()
        
        compile_token()
        
    
    add_token("</term>")

def compile_expressionList():

    add_token("<expressionList>")

    if (not get_current_token() == ")"):
        compile_expression()
        

    while (get_current_token() == ","):
        compile_token()
        compile_expression()
    
    add_token("</expressionList>")

def compile_token():                                                    # used for TERMINAL elements
    token = get_current_token()
    token_type = get_current_type()

    if token_type == "stringConstant":
        token = token[1:-1]

    token_list = []
    add_token(f"<{token_type}> {token} </{token_type}>")

    advance()


def add_token(token):
    global tokens, parsed_tokens, current_token_number

    parsed_tokens.append(token)

def add_tokens(token_list):
    global tokens, parsed_tokens, current_token_number

    parsed_tokens += token_list

def advance():
    global tokens, parsed_tokens, current_token_number

    current_token_number += 1

def get_current_token():
    global tokens, parsed_tokens, current_token_number

    return tokens[current_token_number]

def get_current_type():
    global tokens, parsed_tokens, current_token_number

    if get_current_token() in keyword_list:
        return "keyword"
    elif get_current_token() in symbol_list:
        return "symbol"
    elif get_current_token().isdigit():
        return "integerConstant"
    elif get_current_token().startswith('"'):
        return "stringConstant"
    else:
        return "identifier"

keyword_list = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 
                'char', 'boolean', 'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if',
                'else', 'while', 'return']

symbol_list = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&amp;', '|', '&lt;', '&gt;', '=', '~']

operator_list = ['+', '-', '*', '/', '&amp;', '|', '&lt;', '&gt;', '=', '~']