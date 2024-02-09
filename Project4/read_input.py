# Reads the input file and generates all the rules inside
from pathlib import Path
def read_file(file_path: str | list) -> dict:
    # Reads a grammar file and creates a dictionary with names as the keys
    # and the name, weights, and options in a list as the value
    rules = {}
    if type(file_path) is str:
        file_path = Path(file_path)
        with open(file_path) as file:
            file_path = file.readlines()
    in_rule = False
    for line in file_path:
        line = line.strip('\n')
        if line == '{':
            in_rule = True
            current_rule = []
            continue
        if line == '}':
            in_rule = False
            name, rest = create_rule(current_rule)
            rules[name] = rest
            continue
        if not in_rule:
            continue
        else:
            line = line.strip()
            current_rule.append(line)
    return rules
def create_rule(rule: list[str]) -> (str, list[list[int], list[str]]):
    # Processes a list of strings to a rule and adds it to a dictionary
    name = rule[0]
    weight = []
    option = []
    for index in range(1, len(rule)):
        rule_split = rule[index].split()
        weight.append(int(rule_split[0]))
        option.append(' '.join(rule_split[1:]))
    return name, [weight, option]