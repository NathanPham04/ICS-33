# Tests for option_class
import unittest

import terminal_symbol
from option import *

class TestOption(unittest.TestCase):
    def test_init(self):
        x = Option('asdf')

    def test_get_rules(self):
        b = {'a':5}
        x = Option('asdf')
        x.set_rules(b)
        self.assertEqual(b, x.get_rules())

    def test_process_line(self):
        b = {'Adjective': terminal_symbol.TerminalSymbol('happy')}
        x = Option('Boo is [Adjective] today')
        x.set_rules(b)
        x.process_line()
        self.assertEqual('Boo', next(x._lines[0].get_val()))
        self.assertEqual('is', next(x._lines[1].get_val()))
        self.assertEqual('happy', next(x._lines[2].get_val()))
        self.assertEqual('today', next(x._lines[3].get_val()))

    def test_get_val(self):
        b = {'Adjective': terminal_symbol.TerminalSymbol('happy')}
        x = Option('Boo is [Adjective] today')
        x.set_rules(b)
        result = list(x.get_val())
        self.assertEqual('Boo is happy today', ' '.join(result))
if __name__ == '__main__':
    unittest.main()