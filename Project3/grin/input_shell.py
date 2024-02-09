# input_shell.py
#
# ICS 33 Winter 2023
# Project 3: Why Not Smile?
#
# Handles taking in the input of grin commands

def read_input() -> list[str]:
    # This will take in input until a . is reached
    grin_lines = []
    end = False
    while True:
        line = input()
        temp = line
        line_split = line.split()
        if len(line_split) == 1 and line_split[0] == '.':
            end = True
        grin_lines.append(temp)
        if end:
            break
    return grin_lines