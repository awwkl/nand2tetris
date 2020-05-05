import re

def tokenize(jack_filename):                                    # tokenize("Square/Main.jack")
    split_lines = []    # after splitting by symbols
    tokens = []         # after splitting by spaces
    xml_tokens = []     # after adding xml markup

    jack_file = open(jack_filename, "r")
    lines = jack_file.readlines()                               # lines of .jack file

    for line in lines:
        line = line.strip()

        if line.startswith("//") or line == "":                 # if comment line or empty
            continue
        if line.startswith("/**") or line.startswith("/*"):     # if comment line
            continue
        if line.strip().startswith("*"):                        # multi-line comment
            continue

        line = line.split("//")[0].strip()                      # remove trailing comment

        # split by symbols, but do not remove symbols
        line = re.split("([}{\(\)\[\].,;\+\-*/&|<>=~])", line)  # "class Main {" => ["class Main", "{"]

        split_lines += line

    split_lines = [x for x in split_lines if x.strip() != ""]             # remove empty lines

    for i in range(len(split_lines)):
        split_lines[i] = split_lines[i].strip()
        if split_lines[i].startswith('"'):
            tokens.append(split_lines[i])                       # add "string of words" to list
        else:
            tokens += split_lines[i].split(" ")                 # add list of tokens to final list

    tokens = [x for x in tokens if x.strip() != ""]             # after splitting by spaces

    xml_tokens = convertToXML(tokens)                           # convert tokens to XML tokens
    xml_tokens.insert(0, "<tokens>")
    xml_tokens.append("</tokens>")                              # <tokens> ... </tokens>

    return xml_tokens
    

def convertToXML(tokens):                                       # var => <keyword> var </keyword>
    for i in range(len(tokens)):
        if tokens[i] in keyword_list:
            tokens[i] = "<keyword> " + tokens[i] + " </keyword>"

        elif tokens[i] in symbol_list:
            tokens[i] = tokens[i].replace("&", "&amp;")         # & => &amp;
            tokens[i] = tokens[i].replace("<", "&lt;")          # < => &lt;
            tokens[i] = tokens[i].replace(">", "&gt;")          # > => &gt;
            tokens[i] = "<symbol> " + tokens[i] + " </symbol>"

        elif tokens[i].isdigit():                               # <integerConstant> 16 </integerConstant>
            tokens[i] = "<integerConstant> " + tokens[i] + " </integerConstant>"

        elif tokens[i].startswith('"'):                         # <stringConstant> string constant </stringConstant>
            tokens[i] = "<stringConstant> " + tokens[i][1:-1] + " </stringConstant>"

        else:                                                   # otherwise, it is an identifier
            tokens[i] = "<identifier> " + tokens[i] + " </identifier>"
    
    return tokens

keyword_list = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 
                'char', 'boolean', 'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if',
                'else', 'while', 'return']

symbol_list = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']