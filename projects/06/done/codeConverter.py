def getAddressBinary(address):          # given @333, return "0000000101001101"
    decimal = int(address[1:])          # remove @, convert to int
    binary = format(decimal, "016b")    # convert to 16-bit binary
    return binary


def getComputeBinary(command):          # convert C-instruction to 16-bit binary
    dest = "null"						# given "D=A", return "1110110000010000"
    jump = "null"
    comp = "0"                        	# initialize dest, jump to null; as they may not be provided

    if "=" in command and ";" in command:  	# dest=comp;jump
        dest = command.split("=")[0]
        comp = command.split("=")[1].split(";")[0]
        jump = command.split(";")[-1]
    elif "=" in command:  					# dest=comp
        dest = command.split("=")[0]
        comp = command.split("=")[1]
    else:  									# comp;jump
        comp = command.split(";")[0]
        jump = command.split(";")[1]

    dd = destDictionary[dest]
    jj = jumpDictionary[jump]
    cc = compDictionary[comp]
    return "111" + cc + dd + jj


destDictionary = {
    "null": "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111",
}

jumpDictionary = {
    "null": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111",
}

compDictionary = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "M": "1110000",
    "!D": "0001101",
    "!A": "0110001",
    "!M": "1110001",
    "-D": "0001111",
    "-A": "0110011",
    "-M": "1110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "M+1": "1110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "M-1": "1110010",
    "D+A": "0000010",
    "D+M": "1000010",
    "D-A": "0010011",
    "D-M": "1010011",
    "A-D": "0000111",
    "M-D": "1000111",
    "D&A": "0000000",
    "D&M": "1000000",
    "D|A": "0010101",
    "D|M": "1010101",
}
