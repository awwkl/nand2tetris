def get_push_pop_codes(parsed_fields, file_prefix):
    command = parsed_fields[0]                              # push or pop

    if (command == "push"):
        return get_push_codes(parsed_fields, file_prefix)   # push
    else:
        return get_pop_codes(parsed_fields, file_prefix)    # pop

def get_push_codes(parsed_fields, file_prefix):
    asm_codes = []
    segment = parsed_fields[1]                              # constant/static/local/argument/this/that/temp/pointer
    i = parsed_fields[2]                                    # 3

    if segment == "constant":
        asm_codes = [f"@{i}", "D=A", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
    elif segment == "static":
        asm_codes = [f"@{file_prefix}.{i}", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
    else:                                                   # local/argument/this/that/temp/pointer
        segment_code = SEGMENT_CODES[segment]               # local => @LCL, argument => @ARG, temp => @5, etc.

        asm_codes = [
            segment_code, "D=M", f"@{i}", "A=D+A", "D=M",
            "@SP", "A=M", "M=D",
            "@SP", "M=M+1"
        ]

        if segment in ["temp", "pointer"]:  # reference addresses directly; push temp 3 => push (5 + 3)
            asm_codes[1] = "D=A"            # no need to dereference, unlike LCL, ARG, THIS, THAT

    return asm_codes

def get_pop_codes(parsed_fields, file_prefix):
    asm_codes = []
    segment = parsed_fields[1]
    i = parsed_fields[2]

    if segment == "static":
        asm_codes = ["@SP", "M=M-1", "A=M", "D=M", f"@{file_prefix}.{i}", "M=D"]
    else:
        segment_code = SEGMENT_CODES[segment]

        asm_codes = [
            segment_code, "D=M", f"@{i}", "D=D+A", "@addr", "M=D",
            "@SP", "M=M-1", "A=M", "D=M",
            "@addr", "A=M", "M=D"
        ]

        if segment in ["temp", "pointer"]:    
            asm_codes[1] = "D=A"                        

    return asm_codes

SEGMENT_CODES = {
    "local": "@LCL",        # push local 3 -> push (*LCL + 3) => first need to get value stored in LCL register
    "argument": "@ARG",
    "this": "@THIS",
    "that": "@THAT",
    "temp": "@5",           # push temp 3 => push (5 + 3)
    "pointer": "@3",
}