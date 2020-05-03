import arithWriter      # ARITHMETIC / LOGICAL COMMANDS
import pushpopWriter    # PUSH, POP COMMANDS
import branchWriter     # BRANCHING COMMANDS
import functionWriter   # FUNCTION COMMANDS

current_function_name = "NULL.NIL"  # will be updated each time code encounters function declaration

def translate(parsed_fields, file_prefix):   # accepts vm instruction array - ["push", "local", "3"], and "StaticTest" file prefix
    global current_function_name    # updates what the current function being translated is

    command = parsed_fields[0]      # use name of command to check which writing function to use

    # ARITHMETIC / LOGICAL COMMANDS
    if command in ["eq", "gt", "lt", "add", "sub", "neg", "and", "or", "not"]:
        return arithWriter.get_arith_codes(command) 

    # PUSH, POP COMMANDS
    elif command in ["push", "pop"]:
        return pushpopWriter.get_push_pop_codes(parsed_fields, file_prefix)   # file_prefix provided for static variable names

    # BRANCHING COMMANDS
    elif command in ["label", "if-goto", "goto"]:
        return branchWriter.get_branching_code(parsed_fields, current_function_name)    # pass current function name

    # FUNCTION COMMANDS
    else:
        if command == "function":
            current_function_name = parsed_fields[1]    # update current function name

        return functionWriter.get_function_calling_code(parsed_fields, file_prefix, current_function_name)

