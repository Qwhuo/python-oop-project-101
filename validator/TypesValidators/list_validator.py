

class ListValidator:
    def __init__(self, required=False, sizeof=None, funcs=None):
        self._required = required
        self._sizeof = sizeof
        self._functions = funcs
        self._curr_func = None
        self._args = ()

    @property
    def is_required(self):
        return self._required

    @property
    def get_sizeof(self):
        return self._sizeof if self._sizeof else None

    @property
    def get_functions(self):
        return self._functions

    def required(self):
        self._required = True if not self.is_required else False
        return self

    def sizeof(self, size):
        if type(size) is not int or size < 0:
            raise ValueError
        self._sizeof = size
        return self

    def test(self, name, *args):
        if name not in self.get_functions.keys():
            raise AttributeError
        self._curr_func = self.get_functions[name]
        self._args = args
        return self

    def is_valid(self, val):
        if self.is_required and type(val) is not list:
            return False
        if self.get_sizeof is not None:
            try:
                if len(val) != self.get_sizeof:
                    return False
            except Exception:
                return False
        if self._curr_func is not None:
            try:
                if not self._curr_func(val, *self._args):
                    return False
            except TypeError or ValueError or AttributeError:
                return False
        return True

