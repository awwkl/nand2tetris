import os
import sys
import JackTokenizer        # generates set of tokens from each .jack file
import CompilationEngine    # receives tokens and calls VMWriter write functions
import SymbolTable          # keeps track of class-scope and subroutine-scope symbols (field, static, local, argument)
import VMWriter             # writes VM instructions to each .vm file

def main():
    pathname = sys.argv[1]                                  # python3 JackCompiler.py Square/

    if os.path.isfile(pathname):                            # Square/Main.jack => is a file
        foldername = pathname.rsplit("/", 1)[0] + "/mine/"  # Square/mine/
        
        if (not os.path.isdir(foldername)):                 # if Square/mine/ does NOT exist
            os.mkdir(foldername)                            # create directory              
        
        filename = pathname.split("/")[-1]                  # Main.jack
        generateFile(foldername, filename)                  # (Square/mine/, Main.jack)

    elif os.path.isdir(pathname):                           # Square/
        if pathname.endswith("/"):
            pathname = pathname[:-1]                        # Square
        
        foldername = pathname + "/mine/"                    # Square/mine/

        if (not os.path.isdir(foldername)):                 # if Square/mine/ does NOT exist
            os.mkdir(foldername)                            # make directory
        
        for filename in os.listdir(pathname):       
            if filename.endswith(".jack"):
                class_name = filename.split(".")[0]         # create list of class names, to avoid adding them to SymbolTable
                SymbolTable.class_list.append(class_name)   # Ball, Bat, Main, PongGame, etc.

        for filename in os.listdir(pathname):       
            if filename.endswith(".jack"):                  # Main.jack
                generateFile(foldername, filename)          # (Square/mine/, Main.jack)

def generateFile(foldername, filename):                     # (Square/mine/, Main.jack)

    jack_filename = foldername.rsplit("/", 2)[0] + "/" + filename   # "Square" + "/" + "Main.jack"
    tokens = JackTokenizer.tokenize(jack_filename)                  # returns tokens generated from .jack file

    vm_filename = foldername + filename.split(".")[0] + ".vm"       # let VMWriter know what file to write to
    VMWriter.initializeFile(vm_filename)                            # open .vm file to begin writing to it

    # pass tokens from Tokenizer to CompilationEngine
    class_name = filename.split(".")[0]
    CompilationEngine.compileTokens(tokens, class_name)

main()