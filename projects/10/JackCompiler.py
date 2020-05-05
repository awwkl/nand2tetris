import os
import sys
import JackTokenizer

pathname = sys.argv[1]

tokens = []

def main():
    global pathname

    if os.path.isfile(pathname):                            # Square/Main.jack (is a file)
        foldername = pathname.rsplit("/", 1)[0] + "/mine/"  # Square/mine/
        
        if (not os.path.isdir(foldername)):                 # if Square/mine/ does NOT exist
            os.mkdir(foldername)                            # make directory              
        
        filename = pathname.split("/")[-1]                  # Main.jack
        generateXML(foldername, filename)                   #(Square/mine/, Main.jack)

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

    jack_filename = foldername.rsplit("/", 2)[0] + "/" + filename
    tokens = JackTokenizer.tokenize(jack_filename)          # returns tokens generated from .jack file

    xml_filename = foldername + filename.split(".")[0] + ".xml"
    xml_file = open(xml_filename, "w")

    for i, token in enumerate(tokens):
        tokens[i] += "\n"

    xml_file.writelines(tokens)


main()