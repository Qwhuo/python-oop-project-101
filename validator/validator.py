from .TypesValidators.string_validator import StringValidator
from .TypesValidators.num_validator import NumValidator



class Validator:
    def __init__(self):
        self.validators = {
            "string": StringValidator,
            "number": NumValidator
        }

    def string(self):
        return self.validators["string"]()

    def number(self):
        return self.validators["number"]()


# v = Validator()
# schema = v.string()
# print(schema.min_len(10).min_len(3).contains("Nope").is_valid("None"))
