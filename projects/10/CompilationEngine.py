current_token_number = 0    # allow program to march through list of tokens
tokens = []                 # tokens received from tokenizer
parsed_tokens = []          # tokens after parsing by compilation engine is done

def compileTokens(token_list):
    global tokens, parsed_tokens, current_token_number

    current_token_number = 0        # need to reset because there are multiple .jack files
    tokens = token_list             # compileTokens will be called multiple times
    parsed_tokens = []              # reset

    compile_class()                 # every .jack file begins with class declaration 
    return parsed_tokens

def compile_class():                # class className { classVarDec* subroutineDec* }
    add_token("<class>")

    compile_token()     # class
    compile_token()     # className
    compile_token()     # {

    while (get_current_token() in ["static", "field"]): # check if any classVarDec to parse
        compile_classVarDec()
    
    while (get_current_token() in ["constructor", "function", "method"]):   # check if any subroutineDec to parse
        compile_subroutineDec()

    compile_token()     # }
        
    add_token("</class>")

def compile_classVarDec():          # (static | field) type varName (, varName)* ;
    add_token("<classVarDec>")

    compile_token()     # static / field
    compile_token()     # type
    compile_token()     # varName

    while (not get_current_token() == ";"):
        compile_token()

    compile_token()     # ;

    add_token("</classVarDec>")

def compile_subroutineDec():        # (constructor | function | method) (void | type) subroutineName 
    add_token("<subroutineDec>")    # ( paramaterList ) subroutineBody

    compile_token()                 # constructor / function / method
    compile_token()                 # void / type    
    compile_token()                 # subroutineName

    compile_token()                 # (
    compile_parameterList()
    compile_token()                 # )

    compile_subroutineBody()

    add_token("</subroutineDec>")

def compile_parameterList():        # (type varName (, type varName)*)?
    add_token("<parameterList>")

    while (not get_current_token() == ")"):
        compile_token()

    add_token("</parameterList>")
    
def compile_subroutineBody():       # { varDec* statements }
    add_token("<subroutineBody>")

    compile_token()                 # {

    while (get_current_token() == "var"):
        compile_varDec()            # varDec*

    compile_statements()

    compile_token()                 # }

    add_token("</subroutineBody>")

def compile_varDec():               # var type varName (, varName)* ;
    add_token("<varDec>")

    while (not get_current_token() == ";"):
        compile_token()
    
    compile_token()                 # ;

    add_token("</varDec>")

def compile_statements():           # statement*
    add_token("<statements>")

    while (get_current_token() in ["let", "if", "while", "do", "return"]):
        compile_statement()

    add_token("</statements>")

def compile_statement():            # let | if | while | do | return
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

def compile_letStatement():         # let varName ([ expression ])? = expression;
    add_token("<letStatement>")

    compile_token()                 # let
    compile_token()                 # varName

    if (get_current_token() == "["):        # varName '[]' MUST represent an array indexing
        compile_arrayIndex()                

    compile_token()                 # =

    compile_expression()            # expression

    compile_token()                 # ;

    add_token("</letStatement>")

def compile_ifStatement():          # if ( expression ) { statements }
    add_token("<ifStatement>")

    compile_token()         # if

    compile_token()         # ( expression )
    compile_expression()    
    compile_token()

    compile_token()         # { statements }
    compile_statements()
    compile_token()

    if (get_current_token() == "else"):
        compile_token()         # else
        compile_token()         # { statements }
        compile_statements()
        compile_token()

    add_token("</ifStatement>")

def compile_whileStatement():       # while ( expression ) { statements }
    add_token("<whileStatement>")

    compile_token()         # while

    compile_token()         # ( expression )
    compile_expression()    
    compile_token()

    compile_token()         # { statements }
    compile_statements()
    compile_token()

    add_token("</whileStatement>")

def compile_doStatement():          # do subroutineCall ;
    add_token("<doStatement>")

    compile_token()                 # do
    
    compile_subroutineCall()        # subroutineCall

    compile_token()                 # ;

    add_token("</doStatement>")

def compile_returnStatement():      # return expression? ;
    add_token("<returnStatement>")

    compile_token()                         # return
    if (not get_current_token() == ";"):    # there must be an expression if current token is not ';'
        compile_expression()
        
    compile_token()                         # ;
    add_token("</returnStatement>")

def compile_subroutineCall():
    while (not get_current_token() == ";"):
        if get_current_token() == "(":
            compile_token()
            compile_expressionList()

        compile_token()

def compile_expression():           # term (op term)*
    add_token("<expression>")

    compile_term()          # term

    while (get_current_token() in operator_list):   # an operator has been spotted!
        compile_token()     # op
        compile_term()      # term

    add_token("</expression>")

def compile_arrayIndex():           # [1]
    compile_token()                 # <symbol> [ </symbol>
    add_token("<expression>")       # <expression>
    add_token("<term>")             #   <term>
    compile_token()                 #     <integerConstant> 1 </integerConstant>
    add_token("</term>")            #   </term>
    add_token("</expression>")      # </expression>
    compile_token()                 # <symbol> ] </symbol>

def compile_term():                 # may contain array indexing[], subroutineCall, or ( expression )
    add_token("<term>")
    lookahead_type = "array_entry"              # default compile array entry

    if (get_current_token() in ["-", "~"]):     # unary operators (-j)
        compile_token()                         # -
        compile_term()                          # j

    while (not get_current_token() in operator_list):
        if get_current_token() in [",", ";", "}", ")"]:
            break

        if get_current_token() == "]":
            compile_token()
            break

        if get_current_token() == ".":
            lookahead_type = "subroutine_call"      # anticipate to compile subroutine call

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

def compile_expressionList():       # (expression (, expression)*)?

    add_token("<expressionList>")

    if (not get_current_token() == ")"):    # if not empty expression list => not '()'
        compile_expression()
        

    while (get_current_token() == ","):     # more expressions in the list spotted!
        compile_token()                     # ,
        compile_expression()                # expression
    
    add_token("</expressionList>")

def compile_token():                # used to add TERMINAL elements (tokens) to parsed_tokens
    token = get_current_token()
    token_type = get_current_type()

    if token_type == "stringConstant":
        token = token[1:-1]         # "some string constant" => some string constant

    token_list = []
    add_token(f"<{token_type}> {token} </{token_type}>")

    advance()                       # increase current_token_number

def add_token(token):               # add single token to parsed_tokens
    global tokens, parsed_tokens, current_token_number

    parsed_tokens.append(token)

def add_tokens(token_list):         # add multiple tokens to parsed_tokens
    global tokens, parsed_tokens, current_token_number

    parsed_tokens += token_list

def advance():                      # increment current_token_number
    global tokens, parsed_tokens, current_token_number

    current_token_number += 1

def get_current_token():            # returns the current token to be parsed
    global tokens, parsed_tokens, current_token_number

    return tokens[current_token_number]

def get_current_type():             # returns the token_type of the current token to be parsed
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