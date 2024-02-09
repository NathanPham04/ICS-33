import unittest
from grin import *

class TestRelationalOperatorsBase(unittest.TestCase):
    def test_init(self):
        x = BaseRelationalOperator(1,2)
        self.assertEqual(1, x.val1)
        self.assertEqual(2, x.val2)
    def test_check_validity_int_int(self):
        x = BaseRelationalOperator(1, 2)
        self.assertTrue(x.check_validity())
    def test_check_validity_int_float(self):
        x = BaseRelationalOperator(1, 2.03204)
        self.assertTrue(x.check_validity())
    def test_check_validity_float_int(self):
        x = BaseRelationalOperator(1.234234, 2)
        self.assertTrue(x.check_validity())
    def test_check_validity_float_float(self):
        x = BaseRelationalOperator(1.234234, 2.234234)
        self.assertTrue(x.check_validity())
    def test_check_validity_str_str(self):
        x = BaseRelationalOperator('asdfasdf', 'asdfasdf')
        self.assertTrue(x.check_validity())
    def test_check_validity_str_int(self):
        with self.assertRaises(RelationalComparisonRuntimeError):
            x = BaseRelationalOperator('asdfasdf', 3432)
    def test_check_validity_str_float(self):
        with self.assertRaises(RelationalComparisonRuntimeError):
            x = BaseRelationalOperator('asdfasdf', 3432.324)
    def test_check_validity_float_str(self):
        with self.assertRaises(RelationalComparisonRuntimeError):
            x = BaseRelationalOperator(3432.324, 'asdfasdf')
    def test_check_validity_int_str(self):
        with self.assertRaises(RelationalComparisonRuntimeError):
            x = BaseRelationalOperator(3432, 'asdfasdf')
class TestRelationalComparison(unittest.TestCase):
    def test_init_valid(self):
        RelationalComparison(1, 2, GrinTokenKind.EQUAL)
        RelationalComparison(1.0, 2.0, GrinTokenKind.EQUAL)
        RelationalComparison(1, 2.0, GrinTokenKind.EQUAL)
        RelationalComparison(1.0, 2, GrinTokenKind.EQUAL)
        RelationalComparison('1.0', '2.0', GrinTokenKind.EQUAL)
    def test_init_invalid_str_float(self):
        with self.assertRaises(RelationalComparisonRuntimeError):
            RelationalComparison('1', 2.0, GrinTokenKind.EQUAL)
    def test_init_invalid_float_str(self):
        with self.assertRaises(RelationalComparisonRuntimeError):
            RelationalComparison(1.0, '2', GrinTokenKind.EQUAL)
    def test_init_invalid_str_int(self):
        with self.assertRaises(RelationalComparisonRuntimeError):
            RelationalComparison('1', 2, GrinTokenKind.EQUAL)
    def test_init_invalid_int_str(self):
        with self.assertRaises(RelationalComparisonRuntimeError):
            RelationalComparison(1, '2', GrinTokenKind.EQUAL)
    def test_do_equal_false(self):
        self.assertFalse(RelationalComparison(1, 2, GrinTokenKind.EQUAL).do_operation())
        self.assertFalse(RelationalComparison(1.0, 2.0, GrinTokenKind.EQUAL).do_operation())
        self.assertFalse(RelationalComparison(-1, -2.0, GrinTokenKind.EQUAL).do_operation())
        self.assertFalse(RelationalComparison(1.0, 2, GrinTokenKind.EQUAL).do_operation())
        self.assertFalse(RelationalComparison('bool', 'boo', GrinTokenKind.EQUAL).do_operation())
    def test_do_equal_true(self):
        self.assertTrue(RelationalComparison(-1, -1, GrinTokenKind.EQUAL).do_operation())
        self.assertTrue(RelationalComparison(1.26, 1.260000, GrinTokenKind.EQUAL).do_operation())
        self.assertTrue(RelationalComparison(1, 1.0000, GrinTokenKind.EQUAL).do_operation())
        self.assertTrue(RelationalComparison(-1.0, -1, GrinTokenKind.EQUAL).do_operation())
        self.assertTrue(RelationalComparison('boo', 'boo', GrinTokenKind.EQUAL).do_operation())
    def test_do_gt_false(self):
        self.assertFalse(RelationalComparison(-1, 2, GrinTokenKind.GREATER_THAN).do_operation())
        self.assertFalse(RelationalComparison(-1, -1, GrinTokenKind.GREATER_THAN).do_operation())
        self.assertFalse(RelationalComparison(1.0, 2.0, GrinTokenKind.GREATER_THAN).do_operation())
        self.assertFalse(RelationalComparison(-5, 2.0, GrinTokenKind.GREATER_THAN).do_operation())
        self.assertFalse(RelationalComparison(1.0, 2, GrinTokenKind.GREATER_THAN).do_operation())
        self.assertFalse(RelationalComparison('bo', 'boo', GrinTokenKind.GREATER_THAN).do_operation())
    def test_do_gt_true(self):
        self.assertTrue(RelationalComparison(2, -1, GrinTokenKind.GREATER_THAN).do_operation())
        self.assertTrue(RelationalComparison(1.265, 1.260000, GrinTokenKind.GREATER_THAN).do_operation())
        self.assertTrue(RelationalComparison(1, -1.0000, GrinTokenKind.GREATER_THAN).do_operation())
        self.assertTrue(RelationalComparison(324.345, 1, GrinTokenKind.GREATER_THAN).do_operation())
        self.assertTrue(RelationalComparison('bool', 'boo', GrinTokenKind.GREATER_THAN).do_operation())
    def test_do_gte_false(self):
        self.assertFalse(RelationalComparison(-10, 2, GrinTokenKind.GREATER_THAN_OR_EQUAL).do_operation())
        self.assertFalse(RelationalComparison(1.9999999, 2.0, GrinTokenKind.GREATER_THAN_OR_EQUAL).do_operation())
        self.assertFalse(RelationalComparison(-5, 2.0, GrinTokenKind.GREATER_THAN_OR_EQUAL).do_operation())
        self.assertFalse(RelationalComparison(1.0, 2, GrinTokenKind.GREATER_THAN_OR_EQUAL).do_operation())
        self.assertFalse(RelationalComparison('bo', 'boo', GrinTokenKind.GREATER_THAN_OR_EQUAL).do_operation())
    def test_do_gte_true(self):
        self.assertTrue(RelationalComparison(-1, -1, GrinTokenKind.GREATER_THAN_OR_EQUAL).do_operation())
        self.assertTrue(RelationalComparison(1.265, 1.265000, GrinTokenKind.GREATER_THAN_OR_EQUAL).do_operation())
        self.assertTrue(RelationalComparison(1, -1.0000, GrinTokenKind.GREATER_THAN_OR_EQUAL).do_operation())
        self.assertTrue(RelationalComparison(1, 1, GrinTokenKind.GREATER_THAN_OR_EQUAL).do_operation())
        self.assertTrue(RelationalComparison('boo', 'boo', GrinTokenKind.GREATER_THAN_OR_EQUAL).do_operation())
    def test_do_lt_true(self):
        self.assertTrue(RelationalComparison(-1, 2, GrinTokenKind.LESS_THAN).do_operation())
        self.assertTrue(RelationalComparison(1.0, 2.0, GrinTokenKind.LESS_THAN).do_operation())
        self.assertTrue(RelationalComparison(-5, 2.0, GrinTokenKind.LESS_THAN).do_operation())
        self.assertTrue(RelationalComparison(1.0, 2, GrinTokenKind.LESS_THAN).do_operation())
        self.assertTrue(RelationalComparison('bo', 'boo', GrinTokenKind.LESS_THAN).do_operation())
    def test_do_lt_false(self):
        self.assertFalse(RelationalComparison(2, -1, GrinTokenKind.LESS_THAN).do_operation())
        self.assertFalse(RelationalComparison(-1, -1, GrinTokenKind.LESS_THAN).do_operation())
        self.assertFalse(RelationalComparison(1.265, 1.260000, GrinTokenKind.LESS_THAN).do_operation())
        self.assertFalse(RelationalComparison(1, -1.0000, GrinTokenKind.LESS_THAN).do_operation())
        self.assertFalse(RelationalComparison(324.345, 1, GrinTokenKind.LESS_THAN).do_operation())
        self.assertFalse(RelationalComparison('bool', 'boo', GrinTokenKind.LESS_THAN).do_operation())
    def test_do_lte_true(self):
        self.assertTrue(RelationalComparison(-2, 2, GrinTokenKind.LESS_THAN_OR_EQUAL).do_operation())
        self.assertTrue(RelationalComparison(2.0, 2.0, GrinTokenKind.LESS_THAN_OR_EQUAL).do_operation())
        self.assertTrue(RelationalComparison(-5, 2.0, GrinTokenKind.LESS_THAN_OR_EQUAL).do_operation())
        self.assertTrue(RelationalComparison(1.0, 2, GrinTokenKind.LESS_THAN_OR_EQUAL).do_operation())
        self.assertTrue(RelationalComparison('bo', 'boo', GrinTokenKind.LESS_THAN_OR_EQUAL).do_operation())
        self.assertTrue(RelationalComparison(-1, -1, GrinTokenKind.LESS_THAN_OR_EQUAL).do_operation())
    def test_do_lte_false(self):
        self.assertFalse(RelationalComparison(2, -1, GrinTokenKind.LESS_THAN_OR_EQUAL).do_operation())
        self.assertFalse(RelationalComparison(1.2650, 1.260000, GrinTokenKind.LESS_THAN_OR_EQUAL).do_operation())
        self.assertFalse(RelationalComparison(1, -1.0000, GrinTokenKind.LESS_THAN_OR_EQUAL).do_operation())
        self.assertFalse(RelationalComparison(324.345, 1, GrinTokenKind.LESS_THAN_OR_EQUAL).do_operation())
        self.assertFalse(RelationalComparison('bool', 'boo', GrinTokenKind.LESS_THAN_OR_EQUAL).do_operation())
    def test_do_not_equal_true(self):
        self.assertTrue(RelationalComparison(1, 2, GrinTokenKind.NOT_EQUAL).do_operation())
        self.assertTrue(RelationalComparison(1.0, 2.0, GrinTokenKind.NOT_EQUAL).do_operation())
        self.assertTrue(RelationalComparison(-1, -2.0, GrinTokenKind.NOT_EQUAL).do_operation())
        self.assertTrue(RelationalComparison(1.0, 2, GrinTokenKind.NOT_EQUAL).do_operation())
        self.assertTrue(RelationalComparison('bool', 'boo', GrinTokenKind.NOT_EQUAL).do_operation())
    def test_do_not_equal_false(self):
        self.assertFalse(RelationalComparison(-1, -1, GrinTokenKind.NOT_EQUAL).do_operation())
        self.assertFalse(RelationalComparison(1.26, 1.260000, GrinTokenKind.NOT_EQUAL).do_operation())
        self.assertFalse(RelationalComparison(1, 1.0000, GrinTokenKind.NOT_EQUAL).do_operation())
        self.assertFalse(RelationalComparison(-1.0, -1, GrinTokenKind.NOT_EQUAL).do_operation())
        self.assertFalse(RelationalComparison('boo', 'boo', GrinTokenKind.NOT_EQUAL).do_operation())
if __name__ == '__main__':
    unittest.main()