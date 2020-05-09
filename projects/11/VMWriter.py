vm_filename = "/dev/null"						# default write to dummy file
vm_file = open(vm_filename, "w")

def writeCommand(command):						
	global vm_filename, vm_file					# centralize to 1 writing function, so only need 'global' once

	vm_file.write(command + "\n")				# newline after each vm instruction

def initializeFile(filename):					# called by JackCompiler
	global vm_filename, vm_file

	vm_filename = filename
	vm_file = open(vm_filename, "w")


def writePush(segment, index):
	writeCommand("push " + segment + " " + str(index))

def writePop(segment, index):
	writeCommand("pop " + segment + " " + str(index))

def writeArithmetic(command):
	writeCommand(command)

def writeLabel(label):
	writeCommand("label " + label)

def writeGoto(label):
	writeCommand("goto " + label)

def writeIfGoto(label):
	writeCommand("if-goto " + label)

def writeCall(name, nArgs):
	writeCommand("call " + name + " " + str(nArgs))

def writeFunction(function_name, nLocals):
	writeCommand("function " + function_name + " " + str(nLocals))

def writeReturn():
	writeCommand("return")