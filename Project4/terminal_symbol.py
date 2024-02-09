# Class representing terminal symbols

class TerminalSymbol:
    def __init__(self, val: str):
        self._val = val

    def get_val(self) -> None:
        # Yields the terminal symbol
        yield self._val