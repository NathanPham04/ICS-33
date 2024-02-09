# Class representing grammar class
import rule
import read_input
import option
class Grammar:
    def __init__(self):
        self.file_path = None
        self.times = None
        self.starting_var = None
        self.rule_dict = None
    def initialize(self) -> None:
        # Initializes the 3 inputs for file, times, and starting variable
        self.file_path = input()
        self.times = int(input())
        self.starting_var = input()
    def make_rules(self) -> None:
        # Gets the words from the file and makes them rules in an attribute
        self.rule_dict = read_input.read_file(self.file_path)
        for key, val in self.rule_dict.items():
            weights = val[0]
            options = [option.Option(x) for x in val[1]]
            for option_ in options:
                option_.process_line()
            self.rule_dict[key] = rule.Rule(key, weights, options)
    def set_rules(self) -> None:
        # Sets the rules for each option
        for val in self.rule_dict.values():
            options = val.get_options()
            for option_ in options:
                option_.set_rules(self.rule_dict)
    def generate_statement(self) -> None:
        starting_rule = self.rule_dict[self.starting_var]
        statement = ' '.join(list(starting_rule.get_val()))
        yield statement
    def execute(self, testing = False, **kwargs):
        # Executes the grammar to create a statement as many times as desired with a testing double
        if not testing:
            self.initialize()
        else:
            self.file_path = kwargs['list']
            self.times = kwargs['times']
            self.starting_var = kwargs['starting_var']
        self.make_rules()
        self.set_rules()
        for i in range(self.times):
            print(next(self.generate_statement()))