equality_code_counter = 0   # ensure unique equality labels in same program (EQUAL_0, EQUAL_1, LESSER_2, EQUAL_3)

def get_arith_codes(command):
    if command in ["eq", "gt", "lt"]:
        return get_equality_codes(command)
    else:
        return ARITH_LOGIC_CODES[command]

def get_equality_codes(command):                                            # eq, gt, lt
    global equality_code_counter

    equality_label = EQUALITY_LABELS[command] + str(equality_code_counter)  # "EQUAL_" + "3" => "EQUAL_3"
    done_label = "DONE_" + str(equality_code_counter)                       # "DONE_" + "2" => "DONE_2"
    jump_code = JUMP_CODES[command]                                         # "D;JEQ"
    equality_code_counter += 1                                              # ensure uniqueness

    asm_codes = [
        "@SP", "M=M-1", "A=M", "D=M", "@SP", "A=M-1", "D=M-D",
        f"@{equality_label}",  jump_code, "@SP", "A=M-1", "M=0",
        f"@{done_label}", "0;JMP",
        f"({equality_label})", "@SP", "A=M-1", "M=-1", f"({done_label})"
    ]

    return asm_codes

EQUALITY_LABELS = {
    "eq": "EQUAL_",
    "gt": "GREATER_",
    "lt": "LESSER_"
}

JUMP_CODES = {
    "eq": "D;JEQ",
    "gt": "D;JGT",
    "lt": "D;JLT"
}

ARITH_LOGIC_CODES = {
    "add": ["@SP", "M=M-1", "A=M", "D=M", "@SP", "A=M-1", "M=M+D"],
    "sub": ["@SP", "M=M-1", "A=M", "D=M", "@SP", "A=M-1", "M=M-D"],
    "neg": ["@SP", "A=M-1", "M=-M", "M=M+1"],                           # add 1 after
    "and": ["@SP", "M=M-1", "A=M", "D=M", "@SP", "A=M-1", "M=M&D"],
    "or": ["@SP", "M=M-1", "A=M", "D=M", "@SP", "A=M-1", "M=M|D"],
    "not": ["@SP", "A=M-1", "M=!M"]
}

