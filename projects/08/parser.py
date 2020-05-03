def parse(line):
    line = line.strip()

    if line.startswith("//") or line == "":     # comment line or empty line
        return None
    
    line = line.split("/")[0].strip()           # removes trailing comments e.g. in "pop local 0    // initializes sum = 0"

    return line.split(" ")                      # returns array - ["push", "local", "3"]