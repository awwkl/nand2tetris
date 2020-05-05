import re

def tokenize(jack_filename):
    tokens = []
    final_tokens = []

    jack_file = open(jack_filename, "r")
    lines = jack_file.readlines()

    for line in lines:
        line = line.strip()

        if line.startswith("//") or line == "":                 # if comment line or empty
            continue
        if line.startswith("/**") or line.startswith("/*"):     # if comment line
            continue
        if line.strip().startswith("*"):
            continue

        line = line.split("//")[0].strip()                      # remove trailing comment
        line = re.split("([}{\(\)\[\].,;\+\-*/&|<>=~])", line)  # split by symbols, but do not remove symbols

        tokens += line

    tokens = [x for x in tokens if x.strip() != ""]

    for i in range(len(tokens)):
        tokens[i] = tokens[i].strip()
        if tokens[i].startswith('"'):
            final_tokens.append(tokens[i])                      # add string to list
        else:
            final_tokens += tokens[i].split(" ")                # add list of tokens to final list

    final_tokens = [x for x in final_tokens if x.strip() != ""]

    final_tokens = convertToXML(final_tokens)
    final_tokens.insert(0, "<tokens>")
    final_tokens.append("</tokens>")

    return final_tokens
    

def convertToXML(tokens):

    for i in range(len(tokens)):
        
        if tokens[i] in keyword_list:
            tokens[i] = "<keyword> " + tokens[i] + " </keyword>"
        elif tokens[i] in symbol_list:
            tokens[i] = tokens[i].replace("&", "&amp;")
            tokens[i] = tokens[i].replace("<", "&lt;")
            tokens[i] = tokens[i].replace(">", "&gt;")
            tokens[i] = "<symbol> " + tokens[i] + " </symbol>"
        elif tokens[i].isdigit():
            tokens[i] = "<integerConstant> " + tokens[i] + " </integerConstant>"
        elif tokens[i].startswith('"'):
            tokens[i] = "<stringConstant> " + tokens[i][1:-1] + " </stringConstant>"
        else:
            tokens[i] = "<identifier> " + tokens[i] + " </identifier>"
    
    return tokens

keyword_list = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 
                'char', 'boolean', 'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if',
                'else', 'while', 'return']

symbol_list = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']