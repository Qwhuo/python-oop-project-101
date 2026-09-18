from .TypesValidators.string_validator import StringValidator
from .TypesValidators.num_validator import NumValidator
from .TypesValidators.list_validator import ListValidator




class Validator:
    def __init__(self):
        self.validators = {
            "string": StringValidator,
            "number": NumValidator,
            "list": ListValidator
        }

    def string(self):
        return self.validators["string"]()

    def number(self):
        return self.validators["number"]()

    def list(self):
        return self.validators["list"]()


# v = Validator()
# schema = v.string()
# print(schema.min_len(10).min_len(3).contains("Nope").is_valid("None"))
