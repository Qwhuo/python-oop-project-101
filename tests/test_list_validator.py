import pytest
from validator.validator import Validator

v = Validator()

def test_equality():
    schema1 = v.list()
    schema2 = v.list()
    assert schema1 is not schema2
    schema1.required()
    assert schema1.is_required != schema2.is_required

def test_standard():
    schema = v.list()
    assert schema.is_valid(None)
    assert schema.is_valid([])
    assert schema.is_valid({"1": 3})


def test_list():
    schema = v.list()
    assert schema.is_valid(None)
    schema.required()
    assert not schema.is_valid(None)
    assert schema.is_valid([])
    assert not schema.is_valid({"1": 3})
    assert schema.required().is_valid(None)

def test_sizeof():
    schema = v.list()
    assert schema.is_valid(None)
    with pytest.raises(ValueError):
        schema.sizeof(-3)
    with pytest.raises(ValueError):
        schema.sizeof(3.33)
    assert schema.get_sizeof is None
    schema.sizeof(2)
    assert schema.is_valid(["Hello", "World"])
    assert not schema.is_valid(["Apelsin"])
    assert schema.is_valid([None, -33])
    assert schema.is_valid({"3": "three", "4": "four"})
    assert not schema.is_valid(3)


def test_all():
    schema = v.list()
    assert schema.is_valid(None)
    assert schema.is_valid([])
    assert schema.required().sizeof(1).is_valid(["Hi"])
    assert not schema.is_valid(["Hi", "Ohayo"])
    assert schema.required().is_valid({"7": "sieben"})
    assert not schema.is_valid(7)