# Class representing variable symbol

class VariableSymbol:
    def __init__(self, val: str, rules: dict):
        self._val = val
        self._rules = rules

    def get_val(self) -> None:
        # Yields the value referring to a variable
        yield from self.get_rules()[self._val].get_val()

    def get_rules(self) -> dict:
        # Returns the rules dictionary
        return self._rules