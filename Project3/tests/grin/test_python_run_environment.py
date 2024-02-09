import unittest
from grin import *
import contextlib
import io
from unittest.mock import patch

class TestPythonRuntimeEnvironment(unittest.TestCase):
    def test_initialization(self):
        grin_lines = list(parse(['LET MESSAGE "Hello Boo!"', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        self.assertEqual(0, x.index)
        self.assertEqual(1, x.max)
        self.assertEqual(dict(), x.variables)
        self.assertEqual([], x.goto_last_index_stack)

    def test_get_variable_with_existing(self):
        grin_lines = list(parse(['PRINT A8923', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.variables['a'] = 'COOL'
        l = x.get_variable('a')
        self.assertEqual('COOL', l)

    def test_get_variable_with_non_existing(self):
        grin_lines = list(parse(['PRINT A8923', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.variables['b'] = 'COOL'
        l = x.get_variable('a')
        self.assertEqual(0, l)

    def test_read_line_with_identifier(self):
        grin_lines = list(parse(['PRINT A8923', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            x.read_line()
            self.assertEqual('0\n', output.getvalue())

    def test_read_line_with_literal_value(self):
        grin_lines = list(parse(['PRINT "COOL"', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            x.read_line()
            self.assertEqual('COOL\n', output.getvalue())

    def test_let_statement_with_literal_int(self):
        grin_lines = list(parse(['LET A 4', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.read_line()
        self.assertEqual(4, x.variables['A'])
    def test_let_statement_with_literal_float(self):
        grin_lines = list(parse(['LET A 4.456', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.read_line()
        self.assertEqual(4.456, x.variables['A'])
    def test_let_statement_with_literal_string(self):
        grin_lines = list(parse(['LET A "BOO"', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.read_line()
        self.assertEqual('BOO', x.variables['A'])
    def test_let_statement_with_non_existing_variable(self):
        grin_lines = list(parse(['LET A A', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.read_line()
        self.assertEqual(0, x.variables['A'])

    def test_let_state_ment_with_existing_variable(self):
        grin_lines = list(parse(['LET A 324', 'LET B A','.']))
        x = PythonRuntimeEnvironment(grin_lines)
        for i in range(2):
            x.read_line()
        self.assertEqual(324, x.variables['B'])

    def test_innum_statement_with_literal_int(self):
        grin_lines = list(parse(['INNUM X', 'INNUM Y', 'INNUM ZERO', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        with patch('builtins.input', side_effect = ['4', '-4', '0']) as mock_input:
            for i in range(3):
                x.read_line()
            self.assertEqual(4, x.variables['X'])
            self.assertEqual(-4, x.variables['Y'])
            self.assertEqual(0, x.variables['ZERO'])
    def test_innum_statement_with_bad_float_positive(self):
        grin_lines = list(parse(['INNUM X', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        with self.assertRaises(SystemExit):
            with patch('builtins.input', side_effect = ['.4']) as mock_input:
                with contextlib.redirect_stdout(io.StringIO()) as output:
                    x.read_line()
    def test_innum_statement_with_bad_float_negative(self):
        grin_lines = list(parse(['INNUM X', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        with self.assertRaises(SystemExit):
            with patch('builtins.input', side_effect = ['-.4']) as mock_input:
                with contextlib.redirect_stdout(io.StringIO()) as output:
                    x.read_line()
    def test_innum_statement_with_literal_float(self):
        grin_lines = list(parse(['INNUM X', 'INNUM Y', 'INNUM ZERO', 'INNUM NEGATIVEZERO','.']))
        x = PythonRuntimeEnvironment(grin_lines)
        with patch('builtins.input', side_effect = ['4.9324', '-4.0', '0.234234', '-0.234234']) as mock_input:
            for i in range(4):
                x.read_line()
            self.assertEqual(4.9324, x.variables['X'])
            self.assertEqual(-4.0, x.variables['Y'])
            self.assertEqual(0.234234, x.variables['ZERO'])
            self.assertEqual(-0.234234, x.variables['NEGATIVEZERO'])

    def test_innum_statement_with_string(self):
        grin_lines = list(parse(['INNUM X', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        with patch('builtins.input', side_effect = ['',]) as mock_input:
            with self.assertRaises(SystemExit):
                with contextlib.redirect_stdout(io.StringIO()) as output:
                    x.read_line()

    def test_innum_statement_with_double_dot(self):
        grin_lines = list(parse(['INNUM X', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        with patch('builtins.input', side_effect = ['92304.234.234',]) as mock_input:
            with self.assertRaises(SystemExit):
                with contextlib.redirect_stdout(io.StringIO()) as output:
                    x.read_line()

    def test_innum_statement_with_existing_variables(self):
        grin_lines = list(parse(['LET X "X-Value"','INNUM X', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        with patch('builtins.input', side_effect = ['2.7']) as mock_input:
            x.read_line()
            self.assertEqual("X-Value", x.variables['X'])
            x.read_line()
            self.assertEqual(2.7, x.variables['X'])

    def test_instr_statement_with_empty_string(self):
        grin_lines = list(parse(['INSTR X', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        with patch('builtins.input', side_effect = ['', ]) as mock_input:
            x.read_line()
            self.assertEqual('', x.variables['X'])

    def test_instr_statement_with_numerics(self):
        grin_lines = list(parse(['INSTR X', 'INSTR Y','.']))
        x = PythonRuntimeEnvironment(grin_lines)
        with patch('builtins.input', side_effect = ['4.78', '-3']) as mock_input:
            x.read_line()
            x.read_line()
            self.assertEqual('4.78', x.variables['X'])
            self.assertEqual('-3', x.variables['Y'])

    def test_instr_statement_with_existing_variable(self):
        grin_lines = list(parse(['INSTR X', 'INSTR X','.']))
        x = PythonRuntimeEnvironment(grin_lines)
        with patch('builtins.input', side_effect = ['4.78', 'BOO']) as mock_input:
            x.read_line()
            self.assertEqual('4.78', x.variables['X'])
            x.read_line()
            self.assertEqual('BOO', x.variables['X'])
    def test_find_labels(self):
        grin_lines = list(parse(['LET A 3', 'TWO: PRINT A',
                                 'PRINT B', 'FOUR: LET B 10', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.find_labels()
        self.assertIn('TWO', x.labels)
        self.assertEqual(1,x.labels['TWO'])
        self.assertIn('FOUR', x.labels)
        self.assertEqual(3, x.labels['FOUR'])
        self.assertNotIn('A', x.labels)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            for i in range(len(grin_lines)):
                x.read_line()
            self.assertEqual('3\n0\n', output.getvalue())
    def test_quit(self):
        grin_lines = list(parse(['END', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        with self.assertRaises(SystemExit):
            x.read_line()
class TestArithmeticOperations(unittest.TestCase):
    def test_get_values_var_int(self):
        grin_lines = list(parse(['ADD X 1', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        y = ArithmeticHandling(x, grin_lines[0])
        self.assertEqual((GrinTokenKind.ADD, 'X', 1), y.get_values())

    def test_get_values_var_str(self):
        grin_lines = list(parse(['ADD X "LKDSJF"', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        y = ArithmeticHandling(x, grin_lines[0])
        self.assertEqual((GrinTokenKind.ADD, 'X', "LKDSJF"), y.get_values())

    def test_get_values_var_float(self):
        grin_lines = list(parse(['ADD X 4.234', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        y = ArithmeticHandling(x, grin_lines[0])
        self.assertEqual((GrinTokenKind.ADD, 'X', 4.234), y.get_values())

    def test_get_values_two_variables(self):
        grin_lines = list(parse(['LET X 4','ADD A X', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.read_line()
        y = ArithmeticHandling(x, grin_lines[1])
        self.assertEqual((GrinTokenKind.ADD, 'A', 4), y.get_values())

    def test_get_values_non_existing_variables(self):
        grin_lines = list(parse(['ADD A X', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        y = ArithmeticHandling(x, grin_lines[0])
        self.assertEqual((GrinTokenKind.ADD, 'A', 0), y.get_values())
        self.assertEqual(GrinTokenKind.ADD, y.operator)
        self.assertEqual('A', y.var)
        self.assertEqual(0, y.val)
        self.assertEqual(0, y.new_val)

    def test_get_values_with_existing_variables(self):
        grin_lines = list(parse(['LET A 10','ADD A X', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.read_line()
        y = ArithmeticHandling(x, grin_lines[1])
        self.assertEqual(10, y.new_val)

    def test_addition_non_existing_var(self):
        grin_lines = list(parse(['LET A 10', 'ADD A X', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.read_line()
        y = ArithmeticHandling(x, grin_lines[1])
        y.do_operation()
        self.assertEqual(10, y.new_val)
    def test_addition_int_int(self):
        grin_lines = list(parse(['LET A 10', 'ADD A 20', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.read_line()
        y = ArithmeticHandling(x, grin_lines[1])
        y.do_operation()
        self.assertEqual(30, y.new_val)

    def test_addition_float_float(self):
        grin_lines = list(parse(['LET A 10.3', 'ADD A 20.6', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.read_line()
        y = ArithmeticHandling(x, grin_lines[1])
        y.do_operation()
        self.assertAlmostEqual(30.9, y.new_val)

    def test_addition_int_float(self):
        grin_lines = list(parse(['LET A 10', 'ADD A 20.6', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.read_line()
        y = ArithmeticHandling(x, grin_lines[1])
        y.do_operation()
        self.assertEqual(30.6, y.new_val)

    def test_addition_float_int(self):
        grin_lines = list(parse(['LET A 10.5', 'ADD A 20', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.read_line()
        x.read_line()
        self.assertEqual(30.5, x.variables['A'])

    def test_addition_str_str(self):
        grin_lines = list(parse(['LET A "BOO"', 'ADD A "DOG"', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.read_line()
        x.read_line()
        self.assertEqual("BOODOG", x.variables['A'])

    def test_addition_failure_str_int(self):
        grin_lines = list(parse(['LET A "BOO"', 'ADD A 4', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.read_line()
        y = ArithmeticHandling(x, grin_lines[1])
        with self.assertRaises(ArithmeticRuntimeError):
            y.do_operation()

    def test_addition_failure_int_str(self):
        grin_lines = list(parse(['LET A 4', 'ADD A "asdf"', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.read_line()
        y = ArithmeticHandling(x, grin_lines[1])
        with self.assertRaises(ArithmeticRuntimeError):
            y.do_operation()

    def test_addition_failure_float_str(self):
        grin_lines = list(parse(['LET A 3.5', 'ADD A "col"', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.read_line()
        y = ArithmeticHandling(x, grin_lines[1])
        with self.assertRaises(ArithmeticRuntimeError):
            y.do_operation()

    def test_addition_failure_str_float(self):
        grin_lines = list(parse(['LET A "acd"', 'ADD A 3.4', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.read_line()
        y = ArithmeticHandling(x, grin_lines[1])
        with self.assertRaises(ArithmeticRuntimeError):
            y.do_operation()
    def test_addition_print_error_statement(self):
        grin_lines = list(parse(['LET A "acd"', 'ADD A 3.4', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.read_line()
        with self.assertRaises(SystemExit):
            with contextlib.redirect_stdout(io.StringIO()) as output:
                x.read_line()
    def test_sub_int_int(self):
        grin_lines = list(parse(['LET A 10', 'SUB A 20', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.read_line()
        y = ArithmeticHandling(x, grin_lines[1])
        y.do_operation()
        self.assertEqual(-10, y.new_val)
    def test_sub_float_float(self):
        grin_lines = list(parse(['LET A 10.3', 'SUB A 20.6', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.read_line()
        y = ArithmeticHandling(x, grin_lines[1])
        y.do_operation()
        self.assertAlmostEqual(-10.3, y.new_val)
    def test_sub_int_float(self):
        grin_lines = list(parse(['LET A 10', 'SUB A 20.6', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.read_line()
        y = ArithmeticHandling(x, grin_lines[1])
        y.do_operation()
        self.assertAlmostEqual(-10.6, y.new_val)
    def test_sub_float_int(self):
        grin_lines = list(parse(['LET A 10.5', 'SUB A 20', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.read_line()
        x.read_line()
        self.assertEqual(-9.5, x.variables['A'])
    def test_sub_non_existing_var(self):
        grin_lines = list(parse(['SUB A 10', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        y = ArithmeticHandling(x, grin_lines[0])
        y.do_operation()
        self.assertEqual(-10, y.new_val)
    def test_sub_in_env(self):
        grin_lines = list(parse(['LET A 10', 'SUB A 20', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.read_line()
        x.read_line()
        self.assertEqual(-10, x.variables['A'])

    def test_sub_print_error_statement_str_float(self):
        grin_lines = list(parse(['LET A "acd"', 'SUB A 3.4', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.read_line()
        with self.assertRaises(SystemExit):
            with contextlib.redirect_stdout(io.StringIO()) as output:
                x.read_line()
    def test_sub_print_error_statement_str_str(self):
        grin_lines = list(parse(['LET A "acd"', 'SUB A "3.4"', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.read_line()
        with self.assertRaises(SystemExit):
            with contextlib.redirect_stdout(io.StringIO()) as output:
                x.read_line()
    def test_mult_non_existing_var(self):
        grin_lines = list(parse(['LET A 10', 'MULT A X', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.read_line()
        y = ArithmeticHandling(x, grin_lines[1])
        y.do_operation()
        self.assertEqual(0, y.new_val)
    def test_mult_int_int(self):
        grin_lines = list(parse(['LET A 10', 'MULT A 20', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.read_line()
        y = ArithmeticHandling(x, grin_lines[1])
        y.do_operation()
        self.assertEqual(200, y.new_val)

    def test_mult_float_float(self):
        grin_lines = list(parse(['LET A 10.3', 'MULT A 20.6', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.read_line()
        y = ArithmeticHandling(x, grin_lines[1])
        y.do_operation()
        self.assertAlmostEqual(212.18, y.new_val)

    def test_mult_int_float(self):
        grin_lines = list(parse(['LET A 10', 'MULT A 20.6', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.read_line()
        y = ArithmeticHandling(x, grin_lines[1])
        y.do_operation()
        self.assertEqual(206.0, y.new_val)

    def test_mult_float_int(self):
        grin_lines = list(parse(['LET A 10.5', 'MULT A 20', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.read_line()
        x.read_line()
        self.assertEqual(210.0, x.variables['A'])
    def test_mult_int_str(self):
        grin_lines = list(parse(['LET A 4', 'MULT A "asdf"', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.read_line()
        y = ArithmeticHandling(x, grin_lines[1])
        y.do_operation()
        self.assertEqual('asdfasdfasdfasdf', y.new_val)
    def test_mult_str_int(self):
        grin_lines = list(parse(['LET A "ALDF"', 'MULT A 0', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.read_line()
        y = ArithmeticHandling(x, grin_lines[1])
        y.do_operation()
        self.assertEqual('', y.new_val)
    def test_mult_failure_str_str(self):
        grin_lines = list(parse(['LET A "BOO"', 'MULT A "DOG"', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.read_line()
        y = ArithmeticHandling(x, grin_lines[1])
        with self.assertRaises(ArithmeticRuntimeError):
            y.do_operation()
    def test_mult_failure_float_str(self):
        grin_lines = list(parse(['LET A 3.5', 'MULT A "col"', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.read_line()
        y = ArithmeticHandling(x, grin_lines[1])
        with self.assertRaises(ArithmeticRuntimeError):
            y.do_operation()

    def test_mult_failure_str_float(self):
        grin_lines = list(parse(['LET A "acd"', 'MULT A 3.4', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.read_line()
        y = ArithmeticHandling(x, grin_lines[1])
        with self.assertRaises(ArithmeticRuntimeError):
            y.do_operation()
    def test_mult_print_error_statement(self):
        grin_lines = list(parse(['LET A "acd"', 'MULT A 3.4', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.read_line()
        with self.assertRaises(SystemExit):
            with contextlib.redirect_stdout(io.StringIO()) as output:
                x.read_line()
    def test_div_int_int(self):
        grin_lines = list(parse(['LET A 10', 'DIV A 20', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.read_line()
        y = ArithmeticHandling(x, grin_lines[1])
        y.do_operation()
        self.assertEqual(0, y.new_val)
    def test_div_float_float(self):
        grin_lines = list(parse(['LET A 20.6', 'DIV A 10.3', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.read_line()
        y = ArithmeticHandling(x, grin_lines[1])
        y.do_operation()
        self.assertAlmostEqual(2.0, y.new_val)
    def test_div_int_float(self):
        grin_lines = list(parse(['LET A 10', 'DIV A 2.5', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.read_line()
        y = ArithmeticHandling(x, grin_lines[1])
        y.do_operation()
        self.assertAlmostEqual(4.0, y.new_val)
    def test_div_float_int(self):
        grin_lines = list(parse(['LET A 10.5', 'DIV A 0.5', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.read_line()
        x.read_line()
        self.assertEqual(21.0, x.variables['A'])
    def test_div_non_existing_var_int(self):
        grin_lines = list(parse(['DIV A 10', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        y = ArithmeticHandling(x, grin_lines[0])
        y.do_operation()
        self.assertEqual(0, y.new_val)

    def test_div_non_existing_var_float(self):
        grin_lines = list(parse(['DIV A 10.45', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        y = ArithmeticHandling(x, grin_lines[0])
        y.do_operation()
        self.assertEqual(0.0, y.new_val)
    def test_div_in_env(self):
        grin_lines = list(parse(['LET A 20', 'DIV A 10', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.read_line()
        x.read_line()
        self.assertEqual(2, x.variables['A'])

    def test_div_print_error_statement_str_float(self):
        grin_lines = list(parse(['LET A "acd"', 'DIV A 3.4', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.read_line()
        with self.assertRaises(SystemExit):
            with contextlib.redirect_stdout(io.StringIO()) as output:
                x.read_line()
    def test_div_print_error_statement_str_str(self):
        grin_lines = list(parse(['LET A "acd"', 'DIV A "3.4"', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.read_line()
        with self.assertRaises(SystemExit):
            with contextlib.redirect_stdout(io.StringIO()) as output:
                x.read_line()
    def test_div_zero_division_int(self):
        grin_lines = list(parse(['DIV A 0', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        y = ArithmeticHandling(x, grin_lines[0])
        with self.assertRaises(ZeroDivisionError):
            y.do_operation()
    def test_div_zero_division_float(self):
        grin_lines = list(parse(['DIV A 0.000', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        y = ArithmeticHandling(x, grin_lines[0])
        with self.assertRaises(ZeroDivisionError):
            y.do_operation()
    def test_div_zero_division_print(self):
        grin_lines = list(parse(['DIV A 0.000', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        with self.assertRaises(SystemExit):
            with contextlib.redirect_stdout(io.StringIO()) as output:
                x.read_line()
class TestGoto(unittest.TestCase):
    def test_get_value_existing_var(self):
        grin_lines = list(parse(['LET A 10', 'GOTO 1 IF A < B', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.read_line()
        y = Goto(x, grin_lines[1])
        self.assertEqual(10, y.get_value(grin_lines[1][3]))
    def test_get_value_non_existing_var(self):
        grin_lines = list(parse(['LET B 10', 'GOTO 1 IF A < B', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.read_line()
        y = Goto(x, grin_lines[1])
        self.assertEqual(0, y.get_value(grin_lines[1][3]))
    def test_get_value_literals(self):
        grin_lines = list(parse(['LET B 10', 'GOTO 1 IF 5 < 4', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.read_line()
        y = Goto(x, grin_lines[1])
        self.assertEqual(5, y.get_value(grin_lines[1][3]))
        self.assertEqual(4, y.get_value(grin_lines[1][5]))
    def test_check_conditional_no_condition(self):
        grin_lines = list(parse(['LET B 10', 'GOTO 1', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.read_line()
        y = Goto(x, grin_lines[1])
        self.assertEqual(True, y.conditional)
    def test_check_conditional_literals(self):
        grin_lines = list(parse(['LET Z 10', 'GOTO 1 IF 5 < 4', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.read_line()
        y = Goto(x, grin_lines[1])
        self.assertEqual(False, y.conditional)
    def test_check_conditional_variables(self):
        grin_lines = list(parse(['LET Z -10.0', 'GOTO 1 IF Z < L', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.read_line()
        y = Goto(x, grin_lines[1])
        self.assertEqual(True, y.conditional)
    def test_check_conditional_invalid(self):
        grin_lines = list(parse(['LET Z -10.0', 'GOTO 1 IF "asdfadsf" < L', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.read_line()
        with self.assertRaises(RelationalComparisonRuntimeError):
            Goto(x, grin_lines[1])
    def test_invalid_goto_value_float(self):
        grin_lines = list(parse(['LET Z -10.0', 'GOTO Z', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.read_line()
        with self.assertRaises(JumpLineError):
            Goto(x, grin_lines[1]).get_new_start_line()
    def test_min_goto_index(self):
        grin_lines = list(parse(['LET Z -10.0', 'GOTO -1','PRINT X', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.read_line()
        self.assertEqual(0, Goto(x, grin_lines[1]).get_new_start_line())
    def test_max_goto_index(self):
        grin_lines = list(parse(['LET Z -10.0', 'GOTO 2','PRINT X', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.read_line()
        self.assertEqual(3, Goto(x, grin_lines[1]).get_new_start_line())
    def test_zero_goto_index(self):
        grin_lines = list(parse(['LET Z -10.0', 'GOTO 0','PRINT X', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.read_line()
        with self.assertRaises(JumpLineError):
            Goto(x, grin_lines[1]).get_new_start_line()
    def test_label_goto_existing(self):
        grin_lines = list(parse(['LET Z -10.0', 'GOTO "LM"', 'LM: PRINT X', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.find_labels()
        x.read_line()
        self.assertEqual(2, Goto(x, grin_lines[1]).get_new_start_line())
    def test_label_goto_existing_behind(self):
        grin_lines = list(parse(['LM: LET Z -10.0', 'GOTO "LM"', 'PRINT X', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.find_labels()
        x.read_line()
        self.assertEqual(0, Goto(x, grin_lines[1]).get_new_start_line())
    def test_label_goto_non_existing(self):
        grin_lines = list(parse(['LET Z -10.0', 'GOTO "LM"', 'PRINT X', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.find_labels()
        x.read_line()
        with self.assertRaises(JumpLineError):
            Goto(x, grin_lines[1]).get_new_start_line()
    def test_label_goto_same_line(self):
        grin_lines = list(parse(['LET Z -10.0', 'LM: GOTO "LM"', 'PRINT X', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.find_labels()
        x.read_line()
        with self.assertRaises(JumpLineError):
            Goto(x, grin_lines[1]).get_new_start_line()
    def test_goto_in_env(self):
        grin_lines = list(parse(['LET Z -10.0', 'GOTO 2', 'PRINT X', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.find_labels()
        x.read_line()
        x.read_line()
        with self.assertRaises(SystemExit):
            x.read_line()
        self.assertEqual(3, x.index)
    def test_goto_in_env_neg(self):
        grin_lines = list(parse(['LET Z -10.0', 'GOTO -1', 'PRINT X', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.find_labels()
        x.read_line()
        x.read_line()
        self.assertEqual(0, x.index)
    def test_goto_in_env_skipping(self):
        grin_lines = list(parse(['LET A 1', 'GOTO 2', 'LET A 2', 'PRINT A','.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.find_labels()
        with self.assertRaises(SystemExit):
            with contextlib.redirect_stdout(io.StringIO()) as output:
                while True:
                    x.read_line()
    def test_goto_in_env_bad_jump(self):
        grin_lines = list(parse(['LET Z -10.0', 'GOTO -2', 'PRINT X', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.find_labels()
        x.read_line()
        with self.assertRaises(SystemExit):
            with contextlib.redirect_stdout(io.StringIO()) as output:
                x.read_line()
    def test_goto_in_env_no_condition(self):
        grin_lines = list(parse(['LET Z "-10.0"', 'GOTO 0 IF Z > 0', 'PRINT X', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.find_labels()
        x.read_line()
        with self.assertRaises(SystemExit):
            with contextlib.redirect_stdout(io.StringIO()) as output:
                x.read_line()
    def test_goto_in_env_false_condition(self):
        grin_lines = list(parse(['LET Z -10.0', 'GOTO -1 IF Z > 0', 'PRINT X', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.find_labels()
        x.read_line()
        x.read_line()
        self.assertEqual(2, x.index)
class TestGOSUB(unittest.TestCase):
    def test_new_start_line(self):
        grin_lines = list(parse(['LET A 1', 'GOSUB 2', 'LET A 2', 'PRINT A', 'RETURN','.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.find_labels()
        with self.assertRaises(SystemExit):
            with contextlib.redirect_stdout(io.StringIO()) as output:
                while True:
                    x.read_line()
    def test_gosub_bad_comparison(self):
        grin_lines = list(parse(['LET A 1', 'GOSUB 2 IF "DF" < 4', 'LET A 2', 'PRINT A', 'RETURN', '.']))
        x = PythonRuntimeEnvironment(grin_lines)
        x.find_labels()
        x.read_line()
        with self.assertRaises(SystemExit):
            with contextlib.redirect_stdout(io.StringIO()) as output:
                x.read_line()
if __name__ == '__main__':
    unittest.main()