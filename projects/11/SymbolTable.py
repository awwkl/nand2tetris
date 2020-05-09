# list of classes; to prevent adding class names to symbol tables
class_list = ["Math", "String", "Array", "Output", "Screen", "Keyboard", "Memory", "Sys"]		# OS classes

class_table = {}					# reset every new .jack file				
subroutine_table = {}				# reset every new subroutine declaration

field_index = 0
static_index = 0
local_index = 0
argument_index = 0

def define(name, var_type, kind):	# add variable to symbol table (either class-level or subroutine-level)
	global class_list
	global class_table, subroutine_table
	global field_index, static_index, local_index, argument_index

	if name in class_list:			# do not add class names
		return

	print("---DEFINING IN SYMBOL TABLE: " + name + " " + var_type + " " + kind)

	if kind == "field":
		class_table[name] = [var_type, kind, field_index]
		field_index += 1

	elif kind == "static":
		class_table[name] = [var_type, kind, static_index]
		static_index += 1

	elif kind == "local":
		subroutine_table[name] = [var_type, kind, local_index]
		local_index += 1

	elif kind == "argument":
		subroutine_table[name] = [var_type, kind, argument_index]
		argument_index += 1

def varCount(kind):			# kind => "static", "field", "argument", "local"
	global class_table, subroutine_table
	count = 0

	for name in subroutine_table:
		if subroutine_table[name][1] == kind:
			count += 1
	
	for name in class_table:
		if class_table[name][1] == kind:
			count += 1
	
	return str(count)

def typeOf(name):
	global class_table, subroutine_table

	try:
		return subroutine_table[name][0]
	except:
		try:
			return class_table[name][0]
		except:
			return "NONE"

def kindOf(name):
	global class_table, subroutine_table

	try:
		return subroutine_table[name][1]
	except:
		try:
			return class_table[name][1]
		except:
			return "NONE"

def indexOf(name):
	global class_table, subroutine_table
	
	try:
		return subroutine_table[name][2]
	except:
		try:
			return class_table[name][2]
		except:
			return "NONE"

def checkIfInTable(name):					# returns true if the name provided is in either class or subroutine table
	try:
		check = subroutine_table[name][1]	# try and see if name in subroutine table
		return True							# if no exception raised, it must be found in subroutine_table
	except:
		try:
			check = class_table[name][1]	# try and see if name in class table
			return True						# if no exception raised, it must be found in class_table
		except:
			return False					# else return false

def startClass():
	global class_table, subroutine_table
	global field_index, static_index, local_index, argument_index

	class_table = {}						# reset field, static, local, argument variables
	subroutine_table = {}

	field_index = 0
	static_index = 0
	local_index = 0
	argument_index = 0

def startSubroutine():
	global class_table, subroutine_table
	global field_index, static_index, local_index, argument_index

	subroutine_table = {}					# reset local, argument variables

	local_index = 0
	argument_index = 0