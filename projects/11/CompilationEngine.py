# tokens are passed from JackTokenizer -> JackCompiler -> CompilationEngine
# CompilationEngine calls write functions of VMWriter module to write VM instructions

import SymbolTable                  # keeps track of class-scope and subroutine-scope symbols (field, static, local, argument)
import VMWriter                     # writes VM instructions to each .vm file

current_token_number = 0            # allow program to march through list of tokens
tokens = []                         # tokens received from tokenizer (used as global variable)
class_name = ""                     # global class name

global_while_index = -1             # allow unique WHILE labels when generating whileStatements
global_if_index = -1                # allow unique IF labels when generating ifStatements

def compileTokens(token_list, input_class): # called by JackCompiler, passing in current list of tokens and current class
    print("---COMPILING TOKENS---")

    SymbolTable.startClass()        # resets symbol table for class and subroutine, as well as indices

    global tokens, current_token_number, class_name

    current_token_number = 0        # reset; because there are multiple .jack files, thus
    tokens = token_list             # compileTokens will be called multiple times
    class_name = input_class        # current class being compiled

    compile_class()                 # every .jack file begins with class declaration 

    print("---DONE COMPILING TOKENS---")


def compile_class():                # class className { classVarDec* subroutineDec* }
    print("---COMPILING CLASS---")

    advance()                       # class
    advance()                       # className
    advance()                       # {

    while (get_current_token() in ["static", "field"]): # check if any classVarDec to parse
        compile_classVarDec()
    
    while (get_current_token() in ["constructor", "function", "method"]):   # check if any subroutineDec to parse
        compile_subroutine()

    print("---DONE COMPILING CLASS---")

def compile_classVarDec():          # (static | field) type varName (, varName)* ;
    print("---COMPILING CLASS VAR DEC")

    var_kind = get_and_advance()    # static / field
    var_type = get_and_advance()    # type; defined only once per classVarDec
    var_name = get_and_advance()    # varName

    SymbolTable.define(var_name, var_type, var_kind)

    while (get_current_token() != ";"): # field int x, y; 
        advance()
        var_name = get_and_advance()
        SymbolTable.define(var_name, var_type, var_kind)
        
    advance()                       # ;

    print("---DONE COMPILING CLASS---")

def compile_subroutine():           # (constructor | function | method) (void | type) subroutineName 
    print("---COMPILING SUBROUTINE---")

    SymbolTable.startSubroutine()   # resets subroutine-scope variables (local, argument)

    subroutine_kind = get_and_advance()     # constructor | function | method
    advance()                               # void | type
    subroutine_name = get_and_advance()     # subroutineName

    if subroutine_kind == "method":
        SymbolTable.define("this", get_class_name(), "argument")

    advance()                       # (
    compile_parameterList()
    advance()                       # )

    advance()                       # {
    
    while get_current_token() == "var":
        compile_varDec()
    
    function_name = get_class_name() + "." + subroutine_name
    num_locals = SymbolTable.varCount("local")
    VMWriter.writeFunction(function_name, num_locals)

    if subroutine_kind == "constructor":
        num_fields = SymbolTable.varCount("field")  # get number of field (instance) variables declared in current subroutine
        VMWriter.writePush("constant", num_fields)
        VMWriter.writeCall("Memory.alloc", 1)       # call Memory.alloc, after pushing the number onto the stack
        VMWriter.writePop("pointer", 0)             # store pointer returned in pointer 0
    elif subroutine_kind == "method":
        VMWriter.writePush("argument", 0)
        VMWriter.writePop("pointer", 0)

    compile_statements()
    advance()                       # } 

    print("---DONE COMPILING SUBROUTINE---")

def compile_parameterList():        # (type varName (, type varName)*)?
    print("---COMPILING PARAMETER LIST---")

    if get_current_token() != ")":
        var_type = get_and_advance()
        var_name = get_and_advance()

        SymbolTable.define(var_name, var_type, "argument")

    while (get_current_token() != ")"):     # new(int Ax, int Ay, ...)
        advance()                   # ,

        var_type = get_and_advance()
        var_name = get_and_advance()

        SymbolTable.define(var_name, var_type, "argument")

    print("---DONE COMPILING PARAMETER LIST---")
    
    
def compile_varDec():               # var type varName (, varName)* ;
    print("---COMPILING VAR DEC---")
    advance()
    var_type = get_and_advance()    # defined only once per varDec
    var_name = get_and_advance()

    SymbolTable.define(var_name, var_type, "local")

    while (get_current_token() != ";"):     # var int dx, dy, dz
        advance()
        var_name = get_and_advance()

        SymbolTable.define(var_name, var_type, "local")
    
    advance()                       # ;

    print("---DONE COMPILING VAR DEC---")

def compile_statements():           # statement*
    print("---COMPILING STATEMENTS---")
    token = ""

    while (get_current_token() in ["let", "if", "while", "do", "return"]):
        token = get_and_advance()

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

    print("---DONE COMPILING STATEMENTS---")
    

def compile_doStatement():          # do subroutineCall ;
    print("---COMPILING DO STATEMENT---")

    compile_subroutineCall()        # subroutineCall
    VMWriter.writePop("temp", 0)
    advance()   

    print("---DONE COMPILING DO STATEMENT---")


def compile_letStatement():         # let varName ([ expression ])? = expression;
    print("---COMPILING LET STATEMENT---")

    var_name = get_and_advance()    # varName
    var_kind = convert_kind(SymbolTable.kindOf(var_name))
    var_index = SymbolTable.indexOf(var_name)

    if (get_current_token() == "["):    # varName '[]' MUST represent an array indexing
        advance()                       # [ expression ]
        compile_expression()
        advance()

        VMWriter.writePush(var_kind, var_index)
        VMWriter.writeArithmetic("add")

        VMWriter.writePop("temp", 0)
        
        advance()                   # =
        compile_expression()
        advance()                   # ;

        VMWriter.writePush("temp", 0)
        VMWriter.writePop("pointer", 1)
        VMWriter.writePop("that", 0)
    else:
        advance()                   # =
        compile_expression()
        advance()                   # ;

        VMWriter.writePop(var_kind, var_index)

    print("---DONE COMPILING LET STATEMENT---")

def compile_whileStatement():       # while ( expression ) { statements }
    print("---COMPILING WHILE STATEMENT---")

    global global_while_index
    global_while_index += 1

    while_index = global_while_index    # local var used; ensure while_index consistent throughout this function
                                        # global_while_index may be changed by other functions without you knowing

    VMWriter.writeLabel("WHILE_EXP" + str(while_index))         # label WHILE_1

    advance()                       # (           
    compile_expression()            # expression
    VMWriter.writeArithmetic("not") # NOT expression
    advance()                       # )
    advance()                       # {

    VMWriter.writeIfGoto("WHILE_END" + str(while_index))    # if-goto WHILE_END_1
    compile_statements()
    VMWriter.writeGoto("WHILE_EXP" + str(while_index))          # goto WHILE_1

    VMWriter.writeLabel("WHILE_END" + str(while_index))
    advance()                       # }

    print("---DONE COMPILING WHILE STATEMENT---")


def compile_returnStatement():              # return expression? ;
    print("---COMPILING RETURN STATEMENT---")

    if (get_current_token() != ";"):        # there must be an expression if current token is not ';'
        compile_expression()                # push return value of expression onto stack
    else:
        VMWriter.writePush("constant", 0)   # if void function, push constant 0   

    VMWriter.writeReturn()
    advance()                               # ;

    print("---DONE COMPILING RETURN STATEMENT---")


def compile_ifStatement():          # if ( expression ) { statements }
    print("---COMPILING IF STATEMENT---")

    global global_if_index
    global_if_index += 1
    
    if_index = global_if_index      # 

    advance()                       # ( expression )
    compile_expression()    
    advance()

    advance()                       # {

    VMWriter.writeIfGoto("IF_TRUE" + str(if_index))
    VMWriter.writeGoto("IF_FALSE" + str(if_index))

    VMWriter.writeLabel("IF_TRUE" + str(if_index))
    compile_statements()
    VMWriter.writeGoto("IF_END" + str(if_index))

    advance()                       # }

    VMWriter.writeLabel("IF_FALSE" + str(if_index))

    if (get_current_token() == "else"):
        advance()                   # else
        advance()                   # { statements }
        compile_statements()
        advance()

    VMWriter.writeLabel("IF_END" + str(if_index))

def compile_expression():           # term (op term)*
    print("---COMPILING EXPRESSION---")
    compile_term()                  # term

    while (get_current_token() in operator_list):   # an operator has been spotted!
        op = get_and_advance()      # op
        compile_term()              # term

        if op in ARITHMETIC.keys():
            VMWriter.writeArithmetic(ARITHMETIC[op])
        elif op == "*":
            VMWriter.writeCall("Math.multiply", 2)
        elif op == "/":
            VMWriter.writeCall("Math.divide", 2)

    print("---DONE COMPILING EXPRESSION---")



# integerConstant | stringConstant | keywordConstant | varName |
# varName '[' expression ']' | subroutineCall | '(' expression ')' | unaryOp term
def compile_term():                 # may contain array indexing[], subroutineCall, or ( expression )
    print("---COMPILING TERM---")

    if get_current_token() in ARITHMETIC_UNARY.keys():
        unary_op = get_and_advance()    # unaryOp
        compile_term()                  # term
        VMWriter.writeArithmetic(ARITHMETIC_UNARY[unary_op])
    elif get_current_token() == "(":
        advance()
        compile_expression()
        advance()
    elif get_current_type() == "integerConstant":
        VMWriter.writePush("constant", get_current_token())
        advance()
    elif get_current_type() == "stringConstant":
        compile_string()
    elif get_current_type() == "keyword":
        compile_keyword()
    else:                           # var / subroutine
        if get_next_token() == "[": # array
            array_name = get_and_advance()

            advance()
            compile_expression()
            advance()

            array_kind = SymbolTable.kindOf(array_name)
            array_index = SymbolTable.indexOf(array_name)
            VMWriter.writePush(convert_kind(array_kind), array_index)

            VMWriter.writeArithmetic("add")
            VMWriter.writePop("pointer", 1)
            VMWriter.writePush("that", 0)
        elif get_next_token() in [".", "("]:    # subroutineCall
            compile_subroutineCall()
        else:
            var_name = get_and_advance()
            var_kind = convert_kind(SymbolTable.kindOf(var_name))
            var_index = SymbolTable.indexOf(var_name)
            VMWriter.writePush(var_kind, var_index)

    print("---DONE COMPILING TERM---")

def compile_expressionList():       # (expression (, expression)*)?
    print("---COMPILING EXPRESSION LIST---")

    number_args = 0

    if get_current_token() != ")":
        number_args += 1
        compile_expression()

    while get_current_token() != ")":
        number_args += 1
        advance()                   # ,
        compile_expression()

    print("---DONE COMPILING EXPRESSION LIST---")
    return number_args

    
def compile_keyword():
    print("---COMPILING KEYWORD---")

    keyword = get_and_advance()

    if keyword == "this":
        VMWriter.writePush("pointer", 0)
    else:
        VMWriter.writePush("constant", 0)

        if keyword == "true":
            VMWriter.writeArithmetic("not")

# subroutineName ( expressionList ) | (className | varName) . subroutineName ( expressionList )
def compile_subroutineCall():
    print("---COMPILING SUBROUTINE CALL---")

    identifier = get_and_advance()
    function_name = identifier
    number_args = 0
    
    if get_current_token() == ".":                  # className (class) | varName (object)
        advance()                                   # .
        subroutine_name = get_and_advance()         # subroutine_name

        var_type = SymbolTable.typeOf(identifier)

        if var_type != "NONE":      # object_instance.subroutineCall(params)
            obj_type = SymbolTable.typeOf(identifier)
            obj_kind = convert_kind(SymbolTable.kindOf(identifier))
            obj_index = SymbolTable.indexOf(identifier)
            VMWriter.writePush(obj_kind, obj_index)      # push local 3

            function_name = obj_type + "." + subroutine_name
            number_args += 1
        else:                       # class_name.subroutineCall(params)
            class_name = identifier
            function_name = class_name + "." + subroutine_name

    elif get_current_token() == "(":                # subroutineName ( expressionList )
        subroutine_name = identifier
        class_name = get_class_name()
        function_name = class_name + "." + subroutine_name
        number_args += 1

        VMWriter.writePush("pointer", 0)            # this is a method call

    advance()       # (
    number_args += compile_expressionList()
    advance()       # )

    VMWriter.writeCall(function_name, number_args)
    print("---DONE COMPILING SUBROUTINE CALL---")


def compile_string():
    print("---COMPILING STRING---")

    string = get_and_advance()

    VMWriter.writePush("constant", len(string))
    VMWriter.writeCall("String.new", 1)

    for char in string:
        VMWriter.writePush("constant", ord(char))
        VMWriter.writeCall("String.appendChar", 2)

    print("---DONE COMPILING STRING---")

        
def get_and_advance():              # get current token, then increment current_token_number
    token = get_current_token()
    advance()
    return token

def advance():                      # increment current_token_number
    global tokens, current_token_number

    print(tokens[current_token_number])

    current_token_number += 1

def get_current_token():            # returns the current token to be parsed
    global tokens, current_token_number

    try:
        token = tokens[current_token_number]
    except:
        token = "FAILED_GET_CURRENT_TOKEN"

    # if token.startswith('"'):   # stringConstant
    #     return token[1:-1]

    return token

def get_next_token():
    global tokens, current_token_number

    try:
        return tokens[current_token_number + 1]
    except:
        return "FAILED_GET_NEXT_TOKEN"

def get_previous_token():
    global tokens, current_token_number

    return tokens[current_token_number - 1]  

def get_current_type():             # returns the token_type of the current token to be parsed
    global tokens, current_token_number

    token = get_current_token()

    if token in keyword_list:
        return "keyword"
    elif token in symbol_list:
        return "symbol"
    elif token.isdigit():
        return "integerConstant"
    elif token.startswith('"'):
        return "stringConstant"
    else:
        return "identifier"

def get_class_name():
    global class_name

    return class_name 

keyword_list = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 
                'char', 'boolean', 'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if',
                'else', 'while', 'return']

symbol_list = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&amp;', '|', '&lt;', '&gt;', '=', '~']

operator_list = ['+', '-', '*', '/', '&', '|', '<', '>', '=']

ARITHMETIC = {
    '+': 'add',
    '-': 'sub',
    '=': 'eq',
    '>': 'gt',
    '<': 'lt',
    '&': 'and',
    '|': 'or'
}

ARITHMETIC_UNARY = {
    '-': 'neg',
    '~': 'not'
}

def convert_kind(kind):     # converts "field" to "this"
    if kind == "field": 
        return "this"
    
    return kind