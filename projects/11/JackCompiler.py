import os
import sys
import JackTokenizer
import CompilationEngine

def main():
    pathname = sys.argv[1]                                  # python3 JackCompiler.py Square/

    if os.path.isfile(pathname):                            # Square/Main.jack => is a file
        foldername = pathname.rsplit("/", 1)[0] + "/mine/"  # Square/mine/
        
        if (not os.path.isdir(foldername)):                 # if Square/mine/ does NOT exist
            os.mkdir(foldername)                            # create directory              
        
        filename = pathname.split("/")[-1]                  # Main.jack
        generateXML(foldername, filename)                   # (Square/mine/, Main.jack)

    elif os.path.isdir(pathname):                           # Square/
        if pathname.endswith("/"):
            pathname = pathname[:-1]                        # Square
        
        foldername = pathname + "/mine/"                    # Square/mine/

        if (not os.path.isdir(foldername)):                 # if Square/mine/ does NOT exist
            os.mkdir(foldername)                            # make directory
        
        for filename in os.listdir(pathname):       
            if filename.endswith(".jack"):                  # Main.jack
                generateXML(foldername, filename)           # (Square/mine/, Main.jack)


def generateXML(foldername, filename):                      # (Square/mine/, Main.jack)

    jack_filename = foldername.rsplit("/", 2)[0] + "/" + filename   # "Square" + "/" + "Main.jack"
    tokens = JackTokenizer.tokenize(jack_filename)                  # returns tokens generated from .jack file

    xml_filename = foldername + filename.split(".")[0] + ".xml"     # Square/mine/Main.xml
    xml_file = open(xml_filename, "w")

    parsed_tokens = CompilationEngine.compileTokens(tokens) # return parsed tokens

    for i, token in enumerate(parsed_tokens):
        parsed_tokens[i] += "\n"

    xml_file.writelines(parsed_tokens)                      # write parsed tokens to xml file


main()