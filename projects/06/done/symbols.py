symbolCounter = 16

def addLabel(label, instructionCounter):			# add label to symbol table. Called during first pass 
	symbolTable[label] = str(instructionCounter)

def getValue(symbol):								# get value of symbol from symbol table
	global symbolCounter
	try:											# if symbol is already in table
		return symbolTable[symbol]					# return its value
	except:				
		symbolTable[symbol] = str(symbolCounter)	# else, add symbol to table
		symbolCounter += 1							# increment symbol counter
		return symbolTable[symbol]					# return the symbol's value as well

symbolTable = {										# initialize the table with pre-defined symbols
	"SP": 	"0",									# in first pass, labels will then be added
	"LCL": 	"1",									
	"ARG": 	"2",									# when new symbol is encountered, it is added to table
	"THIS": "3",									# when existing symbol is sought, return its value
	"THAT": "4",
	"SCREEN": "16384",
	"KBD": "24576",
	"R0": 	"0",
	"R1": 	"1",
	"R2": 	"2",
	"R3": 	"3",
	"R4": 	"4",
	"R5": 	"5",
	"R6": 	"6",
	"R7": 	"7",
	"R8": 	"8",
	"R9": 	"9",
	"R10": 	"10",
	"R11": 	"11",
	"R12": 	"12",
	"R13": 	"13",
	"R14": 	"14",
	"R15": 	"15"
}