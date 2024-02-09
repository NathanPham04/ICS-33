# Tests for read_input functions
import unittest
import tempfile
from read_input import *

class TestReadInput(unittest.TestCase):
    def test_create_rule(self):
        rule = ['HowIsBoo', '1 Boo is [Adjective] today']
        name, rest = create_rule(rule)
        self.assertEqual('HowIsBoo', name)
        self.assertEqual([1], rest[0])
        self.assertEqual(['Boo is [Adjective] today'], rest[1])

    def test_create_rule_empty(self):
        rule = ['HowIsBoo', '1']
        name, rest = create_rule(rule)
        self.assertEqual('HowIsBoo', name)
        self.assertEqual([1], rest[0])
        self.assertEqual([''], rest[1])

    def test_with_file(self):
        with tempfile.NamedTemporaryFile(mode = 'w', encoding = 'utf-8',
                                         delete = False) as input_file:
            input_file.write('{\n')
            input_file.write('HowIsBoo\n')
            input_file.write('1 Boo is [Adjective] today\n')
            input_file.write('}\n')
            input_file.write('\n')
            input_file.write('{\n')
            input_file.write('Adjective\n')
            input_file.write('100 perfect\n')
            input_file.write('}\n')
        rules = read_file(input_file.name)
        self.assertEqual({'HowIsBoo': [[1], ['Boo is [Adjective] today']],
                          'Adjective': [[100], ['perfect']]}, rules)
if __name__ == '__main__':
    unittest.main()