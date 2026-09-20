

class StringValidator:
    def __init__(self, required=False, min_len=0, contains="", funcs={}):
        self._required = required
        self._min_len = min_len
        self._contains = contains
        self._functions = funcs
        self._curr_func = None
        self._args = ()

    @property
    def is_required(self):
        return self._required

    @property
    def get_min_len(self):
        return self._min_len

    @property
    def get_contains(self):
        return self._contains

    @property
    def get_functions(self):
        return self._functions

    def required(self):
        self._required = True if not self.is_required else False
        return self

    def min_len(self, min_len_set):
        self._min_len = min_len_set
        return self

    def contains(self, contains_string_set):
        self._contains = contains_string_set
        return self

    def test(self, name, *args):
        if name not in self.get_functions.keys():
            raise AttributeError
        self._curr_func = self.get_functions[name]
        self._args = args if args else ()
        return self

    def is_valid(self, s):
        if s is None:
            s = ""
        if self.is_required and len(s) == 0:
            return False
        if len(s) < self.get_min_len:
            return False
        if s.find(self.get_contains) == -1:
            return False
        if self._curr_func is not None:
            try:
                if not self._curr_func(s, *self._args):
                    return False
            except TypeError or ValueError or AttributeError:
                return False
        return True