from .TypesValidators.string_validator import StringValidator



class Validator:
    def __init__(self):
        self.validators = {
            "string": StringValidator
        }

    def string(self):
        return self.validators["string"]()


v = Validator()
schema = v.string()
print(schema.min_len(10).min_len(3).contains("Nope").is_valid("None"))
