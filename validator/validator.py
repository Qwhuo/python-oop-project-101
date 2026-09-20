from .TypesValidators.custom_validator import CustomValidator
from .TypesValidators.string_validator import StringValidator
from .TypesValidators.num_validator import NumValidator
from .TypesValidators.list_validator import ListValidator
from .TypesValidators.dict_validator import DictValidator




class Validator:
    def __init__(self):
        self.validators = {
            "string": StringValidator,
            "number": NumValidator,
            "list": ListValidator,
            "dict": DictValidator
        }
        self.functions = {
            "string": {},
            "number": {},
            "list": {},
            "dict": {}
        }

    def string(self):
        return self.validators["string"](funcs=self.functions["string"])

    def number(self):
        return self.validators["number"](funcs=self.functions["number"])

    def list(self):
        return self.validators["list"](funcs=self.functions["list"])

    def dict(self):
        return self.validators["dict"](self, funcs=self.functions["dict"])

    def add_validator(self, type, name, func):
        self.functions[type][name] = func

    def get_validators(self):
        return self.validators

    def get_functions(self):
        return self.functions


# v = Validator()
# schema = v.string()
# print(schema.min_len(10).min_len(3).contains("Nope").is_valid("None"))

v = Validator()
# schema = v.dict()
# schema.shape(
#     {
#         "name": v.string().required(),
#         "age": v.number().positive()
#     }
# )
#
# print("D1: ", schema.is_valid({'name': 'kolya', 'age': 100}))  # True
# print("D2: ", schema.is_valid({'name': 'maya', 'age': None}))  # True
# print(schema.is_valid({'name': '', 'age': None}))  # False
# print(schema.is_valid({'name': 'ada', 'age': -5}))  # False