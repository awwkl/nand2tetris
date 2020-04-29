import sys                  # used to get .asm file name from command line arguments
import codeConverter        # import from codeConverter.py (converts A-, C-instructions to 16-bit binary)
import symbols              # import from symbols.py (stores symbol table and related functions)

# using Pong.asm as example

asm_file_name = sys.argv[1]                         # get Pong.asm file name from command-line arguments
asm_file = open(asm_file_name, "r")                 # open Pong.asm file

firstpassLines = []                                         # store first pass code            
firstpass_file_name = asm_file_name[:-4] + "_first.asm"     # Pong_first.asm
firstpass_file = open(firstpass_file_name, "w")             # open Pong_first.asm file to write into

hackLines = []                                      # array of binary lines to write to Pong.hack file
hack_file_name = asm_file_name[:-4] + ".hack"       # define file name as Pong.hack
hack_file = open(hack_file_name, "w")               # open Pong.hack file

instructionCounter = 0                              # keep track of instruction counter; for adding labels

Lines = asm_file.readlines()                        # get lines of Pong.asm file
for line in Lines:
    line = line.strip()                             # strip leading, trailing whitespace, and \n
    if line.startswith("//") or line == "":         # if line is a comment, or empty, SKIP line
        continue        
    if " " in line:                                 # there is comment later in the line; D=M+1    // some comment
        line = line.split(" ")[0]                   # removes comment, remaining command

    if line[0] == "(":                              # if is label e.g. (LOOP), (END)
        label = line.replace("(", "")               # extract label name -> LOOP from (LOOP)
        label = label.replace(")", "")
        symbols.addLabel(label, instructionCounter) # add label to symbol table
        continue                                    # SKIP. Do not print to Pong_first.asm
                                                    # Do not increase instruction counter
    firstpassLines += line + "\n"                   # if line is not label, just add it normally
    instructionCounter += 1                         # increment instructionCounter

firstpass_file.writelines(firstpassLines)


firstpass_file = open(firstpass_file_name, "r")     # read from Pong_first.asm; ready to assemble into machine language
Lines = firstpass_file.readlines()                  # get lines from firstpass file

for line in Lines:
    line = line.strip()                             # just in case; it was stripped earlier on as well
    if line.startswith("//") or line == "":         # the last line of Pong_first.asm is actually a \n
        continue                                    # make sure to SKIP it, else error thrown

    if line.startswith("@"):                        # A-instruction; could be variable symbol or integer
        try:                                        # use a try except to check if variable symbol or integer
            int(line[1:])   # tries to convert to integer; will work if is integer
            binaryCode = codeConverter.getAddressBinary(line)    # get 16-bit binary from @2451
            hackLines += binaryCode + "\n"
        except:                                                         # if not integer, must be variable symbol
            symbol = line.replace("@", "")                              # extract symbol; 'count' from '@count'
            value = symbols.getValue(symbol)                            # get symbol value (count -> 19)
            binaryCode = codeConverter.getAddressBinary("@" + value)    # convert @19 to 16-bit binary code
            hackLines += binaryCode + "\n"
    else:
        binaryCode = codeConverter.getComputeBinary(line)   # get 16-bit binary from dest=comp;jump
        hackLines += binaryCode + "\n"


hack_file.writelines(hackLines)                             # write to Pong.hack