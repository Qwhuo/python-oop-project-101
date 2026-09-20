import math



class NumValidator:
    def __init__(self, required=False, positive=False, range=(-math.inf, math.inf), funcs={}):
        self._required = required
        self._positive = positive
        self._range = range
        self._functions = funcs
        self._curr_func = None
        self._args = ()

    @property
    def is_required(self):
        return self._required

    @property
    def is_positive(self):
        return self._positive

    @property
    def get_range(self):
        return self._range

    @property
    def get_functions(self):
        return self._functions

    def required(self):
        self._required = True if not self.is_required else False
        return self

    def positive(self):
        self._positive = True if not self.is_positive else False
        return self

    def range(self, lower_bound=-math.inf, upper_bound=math.inf):
        self._range = (lower_bound, upper_bound)
        return self

    def test(self, name, *args):
        if name not in self.get_functions.keys():
            raise AttributeError
        self._curr_func = self._functions[name]
        self._args = args if args else ()
        return self

    def is_valid(self, num):
        if num is None:
            if self.is_required:
                return False
            else:
                return True
        if self.is_positive and num < 0:
            return False
        if num > self.get_range[1] or num < self.get_range[0]:
            return False
        if self._curr_func is not None:
            try:
                if not self._curr_func(num, *self._args):
                    return False
            except TypeError or ValueError or AttributeError:
                return False
        return True
