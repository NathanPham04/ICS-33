# Testing for variable_symbol_class
import unittest
from variable_symbol import *
from terminal_symbol import *

class TestVariableSymbol(unittest.TestCase):
    def test_get_rules(self):
        rule = {'a': TerminalSymbol('b')}
        x = VariableSymbol('a', rule)
        self.assertEqual(rule, x.get_rules())

    def test_get_val(self):
        x = VariableSymbol('a', {'a': TerminalSymbol('b')})
        self.assertEqual('b', next(x.get_val()))
if __name__ == '__main__':
    unittest.main()