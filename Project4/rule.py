# Class representing rules
import option
import random
class Rule:
    def __init__(self, name: str, weights: list[int], options: list[option.Option]):
        self._name = name
        self._weights = weights
        self._options = options
    def get_name(self) -> str:
        # Returns the name of the rule
        return self._name
    def get_weights(self) -> list[int]:
        # Returns the list of weights
        return self._weights
    def get_options(self) -> list[option.Option]:
        # Returns the list of weights
        return self._options
    def choose_random_option(self) -> option.Option:
        # Returns a random option using the weights
        return random.choices(self.get_options(), self.get_weights())[0]
    def get_val(self) -> str:
        # Yields the result of the option chosen randomly
        rand_option = self.choose_random_option()
        yield from rand_option.get_val()