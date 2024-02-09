# Class representing options
import variable_symbol
import terminal_symbol

class Option:
    def __init__(self, val: str):
        self._val = val
        self._rules = None
        self._lines = None

    def get_val(self) -> None:
        # Yields the terminal symbol of the option or the result of the variables in it
        self.process_line()
        for index, val in enumerate(self._lines):
            self._lines[index] = yield from val.get_val()

    def set_rules(self, rules: dict) -> None:
        # Sets the rules of each an option
        self._rules = rules
    def get_rules(self) -> dict:
        # Returns the rules
        return self._rules

    def process_line(self):
        # Processes a line into terminals and variables
        self._lines = self._val.split()
        for index, word in enumerate(self._lines):
            if word[0] == '[' and word[-1] == ']' and word[1:-1].isalnum():
                self._lines[index] = variable_symbol.VariableSymbol(word[1:len(word)-1],
                                                                   self.get_rules())
            else:
                self._lines[index] = terminal_symbol.TerminalSymbol(word)