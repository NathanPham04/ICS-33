# Testing for project 4
import unittest
from unittest.mock import patch
import contextlib
import io
import tempfile
import project4

class TestProject4(unittest.TestCase):
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
            self.input_file.write('3 happy\n')
            self.input_file.write('3 perfect\n')
            self.input_file.write('1 relaxing\n')
            self.input_file.write('1 fulfilled\n')
            self.input_file.write('1 excited\n')
            self.input_file.write('}\n')

    def test_main(self):
        with patch('builtins.input', side_effect = [self.input_file.name,
                                                    '1',
                                                    'HowIsBoo']) as mock_input:
            with contextlib.redirect_stdout(io.StringIO()) as output:
                possible = ['Boo is happy today\n',
                            'Boo is perfect today\n',
                            'Boo is relaxing today\n',
                            'Boo is fulfilled today\n',
                            'Boo is excited today\n']
                project4.main()
                self.assertIn(output.getvalue(), possible)
if __name__ == '__main__':
    unittest.main()