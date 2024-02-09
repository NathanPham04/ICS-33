# Testing for grammar class
from grammar import *
from unittest.mock import patch
import unittest
import tempfile
import contextlib
import io
class GrammarTesting(unittest.TestCase):
    def setUp(self) -> None:
        with tempfile.NamedTemporaryFile(mode = 'w', encoding = 'utf-8',
                                         delete = False) as self.input_file:
            self.input_file.write('{\n')
            self.input_file.write('HowIsBoo\n')
            self.input_file.write('1 Boo is [Adjective] today\n')
            self.input_file.write('}\n')
            self.input_file.write('\n')
            self.input_file.write('{\n')
            self.input_file.write('Adjective\n')
            self.input_file.write('100 perfect\n')
            self.input_file.write('}\n')
    def test_initialize(self):
        x = Grammar()
        with patch('builtins.input', side_effect = ['temp.txt',
                                                    '13',
                                                    'CoolBeans']) as mock_input:
            x.initialize()
        self.assertEqual('temp.txt', x.file_path)
        self.assertEqual(13, x.times)
        self.assertEqual('CoolBeans', x.starting_var)
    def test_make_rules(self):
        x = Grammar()
        x.file_path = self.input_file.name
        x.make_rules()
        self.assertIn('HowIsBoo', x.rule_dict.keys())
        self.assertIn('Adjective', x.rule_dict.keys())
    def test_set_rules(self):
        x = Grammar()
        x.file_path = self.input_file.name
        x.make_rules()
        x.set_rules()
        self.assertIn('HowIsBoo', x.rule_dict['HowIsBoo'].get_options()[0].get_rules().keys())
        self.assertIn('HowIsBoo', x.rule_dict['Adjective'].get_options()[0].get_rules().keys())
    def test_generate_statement(self):
        x = Grammar()
        x.file_path = self.input_file.name
        x.make_rules()
        x.set_rules()
        x.starting_var = 'HowIsBoo'
        self.assertEqual('Boo is perfect today', next(x.generate_statement()))
    def test_execute(self):
        x = Grammar()
        with contextlib.redirect_stdout(io.StringIO()) as output:
            with patch('builtins.input', side_effect = [self.input_file.name,
                                                        '2',
                                                        'HowIsBoo']) as mock_input:
                x.execute()
        self.assertEqual("Boo is perfect today\nBoo is perfect today\n", output.getvalue())
    def testing_double(self):
        x = Grammar()
        list_temp = ['{',
                    'Boo',
                    '1 MEOW MEOW [Cool]',
                    '}',
                    '',
                    '{',
                    'Cool',
                    '1 Bark',
                    '}']
        with contextlib.redirect_stdout(io.StringIO()) as output:
            x.execute(testing = True, times = 1, starting_var ='Boo', list = list_temp)
            self.assertEqual('MEOW MEOW Bark\n', output.getvalue())
if __name__ == '__main__':
    unittest.main()