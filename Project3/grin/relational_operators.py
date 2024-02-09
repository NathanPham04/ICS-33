# python_runtime_env.py
#
# ICS 33 Winter 2023
# Project 3: Why Not Smile?
#
# Classes of the grin relational operators
from grin import GrinTokenKind

class RelationalComparisonRuntimeError(Exception):
    def __init__(self, val1, val2):
        self.val1 = val1
        self.val2 = val2
        super().__init__(self.message())
    def message(self):
        return f'Unsupported Comparison Between {type(self.val1)} {self.val1} and {type(self.val2)} {self.val2}'
class BaseRelationalOperator:
    def __init__(self, val1, val2):
        self.val1 = val1
        self.val2 = val2
        self.valid = self.check_validity()

    def check_validity(self):
        """Returns True if the two values are able to be compared to each other
        else returns False"""
        match self.val1, self.val2:
            case (int(), int()) | \
                 (float(), float()) | \
                 (int(), float()) | \
                 (float(), int()) | \
                 (str(), str()):
                return True
            case _:
                raise RelationalComparisonRuntimeError(self.val1, self.val2)
class RelationalComparison(BaseRelationalOperator):
    def __init__(self, int1, int2, operation):
        super().__init__(int1, int2)
        self.operation = operation
    def do_operation(self):
        """Will return the result of operation"""
        match self.operation:
            case GrinTokenKind.EQUAL:
                return self.do_eq()
            case GrinTokenKind.GREATER_THAN:
                return self.do_gt()
            case GrinTokenKind.GREATER_THAN_OR_EQUAL:
                return self.do_gt() or self.do_eq()
            case GrinTokenKind.LESS_THAN:
                return self.do_lt()
            case GrinTokenKind.LESS_THAN_OR_EQUAL:
                return self.do_lt() or self.do_eq()
            case GrinTokenKind.NOT_EQUAL:
                return not self.do_eq()
    def do_eq(self):
        """Handles equality operator"""
        if type(self.val1) is str or type(self.val2) is str:
            return self.val1 == self.val2
        else:
            return float(self.val1) == float(self.val2)
    def do_gt(self):
        """Handles equality operator"""
        if type(self.val1) is str or type(self.val2) is str:
            return self.val1 > self.val2
        else:
            return float(self.val1) > float(self.val2)
    def do_lt(self):
        """Handles equality operator"""
        if type(self.val1) is str or type(self.val2) is str:
            return self.val1 < self.val2
        else:
            return float(self.val1) < float(self.val2)