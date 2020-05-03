call_count = 0          # set up unique return symbol each time you call another function

def get_function_calling_code(parsed_fields, file_prefix, current_function_name):
    command = parsed_fields[0]      # function/call/return

    if command == "function":
        return get_function_code(parsed_fields, file_prefix)

    elif command == "call":
        return get_call_code(parsed_fields, file_prefix, current_function_name) # pass in current function name

    elif command == "return":
        return get_return_code(parsed_fields, file_prefix)
    
def get_function_code(parsed_fields, file_prefix):
    function_name = parsed_fields[1]            # [function, function_name, locals]
    locals = int(parsed_fields[2])

    asm_codes = [f"({function_name})"]          # (functionNameLabel)

    for x in range(locals):                     # PUSH 0 for each local variable
        asm_codes += ["@SP", "A=M", "M=0", "@SP", "M=M+1"]

    return asm_codes

def get_call_code(parsed_fields, file_prefix, current_function_name):       # [call, called_function, nArgs]
    global call_count
    return_address = current_function_name + "$" + "RET" + str(call_count)  # e.g. Main.fibonacci$RET0
    call_count += 1                         # ensure unique return symbol each time you call another function

    called_function = parsed_fields[1]      # name of function being called
    nArgs = parsed_fields[2]                # number of arguments being passed
    
    asm_codes = [
        f"@{return_address}", "D=A", "@SP", "A=M", "M=D", "@SP", "M=M+1",   # push return_address
        "@LCL", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1",                 # push LCL
        "@ARG", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1",                 # push ARG
        "@THIS", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1",                # push THIS
        "@THAT", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1",                # push THAT
        "@SP", "D=M", f"@{nArgs}", "D=D-A", "@5", "D=D-A", "@ARG", "M=D",   # ARG = SP-n-5
        "@SP", "D=M", "@LCL", "M=D",                                        # LCL = SP
        f"@{called_function}", "0;JMP",                                     # goto f
        f"({return_address})"
    ]

    return asm_codes

def get_return_code(parsed_fields, file_prefix):
    asm_codes = [
        "@LCL", "D=M", "@FRAME", "M=D",                         # FRAME = LCL
        "@FRAME", "D=M", "@5", "A=D-A", "D=M", "@RET", "M=D",   # RET = *(FRAME - 5)
        "@SP", "M=M-1", "A=M", "D=M", "@ARG", "A=M", "M=D",     # *ARG = pop()
        "@ARG", "D=M+1", "@SP", "M=D",                          # SP = ARG + 1
        "@FRAME", "D=M", "@1", "A=D-A", "D=M", "@THAT", "M=D",  # THAT = *(FRAME - 1)
        "@FRAME", "D=M", "@2", "A=D-A", "D=M", "@THIS", "M=D",  # THIS = *(FRAME - 2)
        "@FRAME", "D=M", "@3", "A=D-A", "D=M", "@ARG", "M=D",   # ARG = *(FRAME - 3)
        "@FRAME", "D=M", "@4", "A=D-A", "D=M", "@LCL", "M=D",   # LCL = *(FRAME - 4)
        "@RET", "A=M", "0;JMP"                                  # goto RET
    ]

    return asm_codes