from sys import argv
whitespace = "   "

class ProgramError(Exception):
    def __init__(self, message="ProgramError: Provide an input file!\n\t(Executable Name)\n                      ^ File name goes here"):
        self.message = message
        super().__init__(self.message)

if len(argv) > 1:
    with open(argv[1], "r") as BFFile:
        content = BFFile.read()
        BFFile.close()
else:
    raise ProgramError

ops = ["+", "-", ".", ",", "[", "]", "<", ">"]
pointer = 0
tape = [0]
prog_ops = ["-so", "--saveoutput"]
savefile = ""
to_save = ""

for i in range(0, len(argv)):
    if argv[i] in prog_ops:
        if prog_ops[prog_ops.index(argv[i])] == "-so" or prog_ops[prog_ops.index(argv[i])] == "-saveoutput":
            savefile = "log.txt"

for i in range(0, len(content)):
    if content[i] in ops:
        if content[i] == "<":
            if pointer == 0:
                tape.insert(0, 0)
            else:
                pointer -= 1
            if savefile != "":
                to_save += "Decrement pointer:\n"+str(tape)+f"\n {whitespace * pointer}^\n"
        elif content[i] == ">":
            if pointer == len(tape)-1:
                pointer += 1
                tape.append(0)
            else:
                pointer += 1
            if savefile != "":
                to_save += "Increment pointer:\n"+str(tape)+f"\n {whitespace * pointer}^\n"
        elif content[i] == "+":
            tape[pointer] += 1
            if savefile != "":
                to_save += "Increment value at pointer:\n"+str(tape)+f"\n {whitespace * pointer}^\n{whitespace * pointer} | {tape[pointer]-1} -> {tape[pointer]}\n"
        elif content[i] == "-":
            tape[pointer] -= 1
            if savefile != "":
                to_save += "Decrement value at pointer:\n"+str(tape)+f"\n {whitespace * pointer}^\n{whitespace * pointer} | {tape[pointer]+1} -> {tape[pointer]}\n"
        #elif 
if savefile != "":
    try:
        with open(savefile, "w") as SaveFile:
            SaveFile.write(to_save)
            SaveFile.close()
    except FileNotFoundError:
        with open(savefile, "a") as SaveFile:
            SaveFile.write(to_save)
            SaveFile.close()
