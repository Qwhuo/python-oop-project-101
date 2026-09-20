

class DictValidator:
    def __init__(self, validator, shape=None, funcs=None):
        self.v = validator
        self._shape = shape
        self._functions = funcs
        self._curr_func = None
        self._args = ()

    @property
    def get_shape(self):
        return self._shape

    @property
    def get_functions(self):
        return self._functions

    def shape(self, sh):
        validators = self.v.get_validators().values()
        if type(sh) is not dict:
            raise TypeError("Not a dict")
        for val in sh.values():
            if type(val) not in validators:
                raise TypeError("Incorrect Format")
        self._shape = sh

    def test(self, name, *args):
        if name not in self.get_functions.keys():
            raise AttributeError
        self._curr_func = self.get_functions[name]
        self._args = args
        return self

    def is_valid(self, d):
        for key, val in d.items():
            if key not in self.get_shape.keys():
                return False
            if not self.get_shape[key].is_valid(val):
                return False
        if self._curr_func is not None:
            try:
                if not self._curr_func(d, *self._args):
                    return False
            except TypeError or AttributeError or ValueError:
                return False
        return True