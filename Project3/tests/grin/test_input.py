import unittest
from unittest.mock import patch
import grin
import project3
import contextlib
import io


class TestInputGrin(unittest.TestCase):
    def test_input(self):
        with patch('builtins.input', side_effect = ['LET MESSAGE "Hello Boo!"',
                                             'PRINT MESSAGE',
                                             '.']) as mock_input:
            grin_lines = grin.read_input()
        self.assertEqual(['LET MESSAGE "Hello Boo!"',
                          'PRINT MESSAGE',
                          '.'], grin_lines)

class TestInputParsing(unittest.TestCase):
    def test_parse_input(self):
        with patch('builtins.input', side_effect = ['LET MESSAGE "Hello Boo!"',
                                                    '.']) as mock_input:
            grin_lines = grin.read_input()
        grin_tokens = list(grin.parse(grin_lines))
        self.assertEqual("LET", grin_tokens[0][0].text())
        self.assertEqual('LET', grin_tokens[0][0].value())
        self.assertEqual(grin.GrinLocation(1, 1) , grin_tokens[0][0].location())
        self.assertEqual("MESSAGE", grin_tokens[0][1].text())
        self.assertEqual('"Hello Boo!"', grin_tokens[0][2].text())

    def test_invalid_input(self):
        with patch('builtins.input', side_effect = ['',
                                                    '.']) as mock_input:
            grin_lines = grin.read_input()
        with self.assertRaises(grin.parsing.GrinParseError):
            grin_tokens = list(grin.parse(grin_lines))

class TestProject3Input(unittest.TestCase):
    def test_get_input(self):
        with patch('builtins.input', side_effect = ['',
                                                    '.']) as mock_input:
            with contextlib.redirect_stdout(io.StringIO()) as output:
                with self.assertRaises(SystemExit):
                    x = project3.get_input()

if __name__ == '__main__':
    unittest.main()