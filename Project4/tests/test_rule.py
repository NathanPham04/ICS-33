# Tests for rule_class
import unittest
from rule import *
from terminal_symbol import *

class TestRule(unittest.TestCase):
    def test_init(self):
        x = Rule('name', [1,2,3], [option.Option('asdfadf')])

    def test_get_name(self):
        x = Rule('name', [1,2,3], [option.Option('asdfadf')])
        self.assertEqual('name', x.get_name())
    def test_get_weights(self):
        x = Rule('name', [1,2,3], [option.Option('asdfadf')])
        self.assertEqual([1,2,3], x.get_weights())
    def test_get_options(self):
        b = option.Option('asdfadf')
        x = Rule('name', [1,2,3], [b])
        self.assertEqual([b], x.get_options())
    def test_choose_random_option(self):
        b = option.Option('asdfadf')
        x = Rule('name', [1], [b])
        self.assertEqual(b, x.choose_random_option())
    def test_get_val(self):
        b = option.Option('boo [a]')
        b.set_rules({'a': TerminalSymbol('happy')})
        x = Rule('name', [1], [b])
        self.assertEqual('boo', list(x.get_val())[0])
        self.assertEqual('happy', list(x.get_val())[1])
if __name__ == '__main__':
    unittest.main()