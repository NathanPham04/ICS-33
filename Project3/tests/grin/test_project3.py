import unittest
import project3
import io
import contextlib
from unittest.mock import patch

class TestProject3(unittest.TestCase):
    def test_get_input(self):
        with patch('builtins.input', side_effect = ['LET A 1',
                                                    '5',
                                                    '.']) as mock_input:
            with self.assertRaises(SystemExit):
                project3.get_input()
    def test_main(self):
        with patch('builtins.input', side_effect = ['LET A 1',
                                                    'GOSUB 5',
                                                    'PRINT A',
                                                    'END',
                                                    'LET A 3',
                                                    'RETURN',
                                                    'PRINT A',
                                                    'LET A 2',
                                                    'GOSUB -4',
                                                    'PRINT A',
                                                    'RETURN',
                                                    '.']) as mock_input:
            with contextlib.redirect_stdout(io.StringIO()) as output:
                with self.assertRaises(SystemExit):
                    project3.main()
                    self.assertEqual('1\n2\n3\n', output.getvalue())
if __name__ == '__main__':
    unittest.main()