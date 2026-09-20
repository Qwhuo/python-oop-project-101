from validator.validator import Validator

v = Validator()

def test_equality():
    schema1 = v.number()
    schema2 = v.number()
    assert schema1 is not schema2
    schema1.required()
    assert schema1.is_required != schema2.is_required

def test_standard():
    schema = v.number()
    assert schema.is_valid(None)
    assert schema.is_valid(33)
    assert schema.is_valid(3.14)
    assert schema.is_valid(-100)

def test_required():
    schema = v.number()
    assert schema.is_valid(None)
    schema.required()
    assert not schema.is_valid(None)
    assert schema.is_valid(33)
    assert schema.required().is_valid(None)

def test_positive():
    schema = v.number()
    assert schema.is_valid(None)
    schema.required().positive()
    assert schema.is_valid(33)
    assert not schema.is_valid(-33)
    assert schema.positive().is_valid(-42)
    assert not schema.is_valid(None)

def test_range():
    schema = v.number()
    assert schema.is_valid(None)
    schema.required().range(1, 100)
    assert schema.is_valid(33)
    assert not schema.is_valid(333)
    assert schema.range(-12, 2).range(0, 19).is_valid(3)
    assert not schema.is_valid(None)

def test_all():
    schema = v.number()
    assert schema.is_valid(None)
    schema.required().positive()
    assert schema.is_valid(33)
    assert not schema.is_valid(-33)
    schema.range(-50, 50)
    assert not schema.is_valid(-3)
    assert schema.positive().is_valid(33)
    assert not schema.is_valid(142)
    assert not schema.is_valid(None)