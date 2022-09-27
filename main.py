from multiprocessing.sharedctypes import Value
from sys import argv
from unittest import skip
whitespace = "   "

class ProgramError(Exception):
    def __init__(self, message="ProgramError: Provide an input file!\n\t(Executable Name)\n                      ^ File name goes here"):
        self.message = message
        super().__init__(self.message)
class LoopError(Exception):
    def __init__(self, message="LoopError: \"[\" must be closed with a \"]\""):
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
        if prog_ops[prog_ops.index(argv[i])] == "-so" or prog_ops[prog_ops.index(argv[i])] == "--saveoutput":
            savefile = "log.log"
char = 1
ln = 1
i = 0
while i != len(content):
    char += 1
    if content[i] == '\n':
        char = 0
        ln += 1
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
                to_save += "Increment pointer:\n"+str(tape)+f"\n {whitespace * pointer}^ -> (Line {ln} Char {char})\n"
        elif content[i] == "+":
            tape[pointer] += 1
            if savefile != "":
                to_save += "Increment value at pointer:\n"+str(tape)+f"\n {whitespace * pointer}^ -> (Line {ln} Char {char})\n{whitespace * pointer} | {tape[pointer]-1} -> {tape[pointer]}\n"
        elif content[i] == "-":
            tape[pointer] -= 1
            if savefile != "":
                to_save += "Decrement value at pointer:\n"+str(tape)+f"\n {whitespace * pointer}^ -> (Line {ln} Char {char})\n{whitespace * pointer} | {tape[pointer]+1} -> {tape[pointer]}\n"
        elif content[i] == "[":
            if tape[pointer] == 0:
                while content[i] != "]":
                    i += 1
                    if i == len(content)-1:
                        if savefile != "":
                            to_save += "Broke at error."
                            try:
                                with open(savefile, "w") as SaveFile:
                                    SaveFile.write(to_save)
                                    SaveFile.close()
                            except FileNotFoundError:
                                with open(savefile, "a") as SaveFile:
                                    SaveFile.write(to_save)
                                    SaveFile.close()
                        raise LoopError
            else:
                pass
            if savefile != "":
                try:
                    to_save += "Begin Loop at pointer:\n"+str(content[i-5:i+5]).replace("\n", "\\n")+f"\n  {whitespace}^ -> (Line {ln} Char {char})\n"
                except:
                    to_save += "Begin Loop at pointer:\n"+str(content[i:i+1]).replace("\n", "\\n")+f" . . . \n  {whitespace}^ -> (Line {ln} Char {char})\n"
        elif content[i] == "]":
            if savefile != "":
                try:
                    to_save += "Check Loop at pointer:\n"+str(content[i-5:i+5]).replace("\n", "\\n")+f"\n  {whitespace}^ -> (Line {ln} Char {char})\n"
                except:
                    to_save += "Check Loop at pointer:\n"+str(content[i:i+1]).replace("\n", "\\n")+f" . . .\n  {whitespace}^ -> (Line {ln} Char {char})\n"
            if tape[pointer] == 0:
                if savefile != "":
                    try:
                        to_save += "End Loop at pointer:\n"+str(content[i-5:i+5]).replace("\n", "\\n")+f"\n  {whitespace}^ -> (Line {ln} Char {char})\n"
                    except:
                        to_save += "End Loop at pointer:\n"+str(content[i:i+1]).replace("\n", "\\n")+f" . . .\n  {whitespace}^ -> (Line {ln} Char {char})\n"
            else:
                if savefile != "":
                    try:
                        to_save += "Re-Enter Loop at pointer:\n"+str(content[i-5:i+5]).replace("\n", "\\n")+f"\n  {whitespace}^ -> (Line {ln} Char {char})\n"
                    except:
                        to_save += "Re-Enter at pointer:\n"+str(content[i:i+1]).replace("\n", "\\n")+f" . . .\n  {whitespace}^ -> (Line {ln} Char {char})\n"
                while content[i] != "[":
                    i -= 1
                    char -= 1
                    if char < 0:
                        ln -= 1
                        char = len(content.split('\n')[ln-1])
                if savefile != "":
                    to_save += f"{whitespace}  | -> Re-Enters at: "+str(content[i:i+1]).replace("\n", "\\n")+f" . . . \t -> (Line {ln} Char {char})\n                        ^\n"
        elif content[i] == ".":
            if tape[pointer] > 0:
                print(chr(tape[pointer]), end="")
            else:
                if savefile != "":
                    to_save += "Broke at error."
                    try:
                        with open(savefile, "w") as SaveFile:
                            SaveFile.write(to_save)
                            SaveFile.close()
                    except FileNotFoundError:
                        with open(savefile, "a") as SaveFile:
                            SaveFile.write(to_save)
                            SaveFile.close()
                raise ValueError(f'Error while printing from tape: Cannot print values less than zero! (Line {ln} Char {char})')
            if savefile != "":
                to_save += "Printed value at pointer:\n"+str(tape)+f"\n {whitespace * pointer}^ -> (Line {ln} Char {char})\n{whitespace * pointer} | {tape[pointer]} -> CONSOLE\n"
        elif content[i] == ",":
            print(chr(tape[pointer]), end="")
            if savefile != "":
                to_save += "Put input value at pointer:\n"+str(tape)+f"\n {whitespace * pointer}^ -> (Line {ln} Char {char})\n{whitespace * pointer} | CONSOLE -> {tape[pointer]}\n"
        #elif 
    i += 1
if savefile != "":
    try:
        with open(savefile, "w") as SaveFile:
            SaveFile.write(to_save)
            SaveFile.close()
    except FileNotFoundError:
        with open(savefile, "a") as SaveFile:
            SaveFile.write(to_save)
            SaveFile.close()