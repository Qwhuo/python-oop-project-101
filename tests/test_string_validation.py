from validator.validator import Validator

v = Validator()

def test_equality():
    schema1 = v.string()
    schema2 = v.string()
    assert not schema1 == schema2
    schema1.required()
    assert schema1.is_required != schema2.is_required

def test_empty():
    schema = v.string()
    assert schema.is_valid("")
    assert schema.is_valid(None)
    assert schema.is_valid("Rozmarin")

def test_required():
    schema = v.string()
    assert schema.is_valid("")
    schema.required()
    assert not schema.is_valid(None)
    assert not schema.is_valid("")
    schema.min_len(0)
    assert not schema.is_valid(None)
    assert schema.is_valid("Mandarin")

def test_min_len():
    schema = v.string()
    assert schema.is_valid("")
    assert not schema.min_len(10).is_valid("")
    assert schema.is_valid("Mandarin777")
    assert schema.min_len(20).min_len(3).is_valid("Yabloko")


def test_contains():
    schema = v.string()
    assert schema.is_valid("")
    assert schema.contains("q").is_valid("queue")
    assert not schema.is_valid("hello world")
    assert not schema.contains("none").is_valid(None)
    assert schema.contains("").is_valid("")

def test_all():
    schema = v.string()
    assert schema.is_valid("")
    assert schema.required().min_len(3).contains("q").is_valid("queue")
    assert not schema.required().min_len(3).contains("none").is_valid("hello world")
    assert not schema.required().min_len(3).contains("no").is_valid("no")
    assert not schema.required().min_len(3).contains("q").min_len(1).is_valid("no")