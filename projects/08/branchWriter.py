def get_branching_code(parsed_fields, current_function_name):
    command = parsed_fields[0]
    label = parsed_fields[1]

    if command == "label":                                              # label LABEL
        asm_codes = [f"({current_function_name}${label})"]                              # (LABEL)
    elif command == "goto":                                             # goto LABEL
        asm_codes = [f"@{current_function_name}${label}", "0;JMP"]                      # @LABEL, 0;JMP
    elif command == "if-goto":                                          # if-goto LABEL
        asm_codes = ["@SP", "M=M-1", "A=M", "D=M", f"@{current_function_name}${label}", "D;JNE"]    # jump if top of stack not equal to zero

    return asm_codes