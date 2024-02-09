# Testing for terminal_symbol_class
import unittest
from terminal_symbol import *

class TestTerminalSymbol(unittest.TestCase):
    def test_get_value(self):
        x = TerminalSymbol('asdf')
        self.assertEqual('asdf', next(x.get_val()))

    def test_failed_init(self):
        with self.assertRaises(TypeError):
            x = TerminalSymbol()
if __name__ == '__main__':
    unittest.main()