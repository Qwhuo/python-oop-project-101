import pytest
from validator.validator import Validator

v = Validator()

def test_creation():
    fn1 = lambda value, div: True if value % div == 0 else False
    fn2 = lambda value, max_len: len(value) < max_len
    v.add_validator("number", "division", fn1)
    v.add_validator("string", "max_length", fn2)
    assert v.get_functions() == {
            "string": {"max_length": fn2},
            "number": {"division": fn1},
            "list": {},
            "dict": {}
        }

def test_string_custom_validator():
    fn = lambda value, start: value.startswith(start)
    v.add_validator("string", "startWith", fn)
    schema = v.string().test("startWith", "Q")
    assert schema.is_valid("Q")
    assert not schema.is_valid("abcde")

    assert v.string().min_len(3).test("startWith", "Q").is_valid("Queue")
    assert not v.string().min_len(3).test("startWith", "Q").is_valid("Q")
    assert not v.string().min_len(3).test("startWith", "Q").is_valid("uwu")

    fn2 = lambda value, max_len: len(value) < max_len
    v.add_validator("string", "max_length", fn2)
    assert schema.test("max_length", 3).is_valid("q")
    assert schema.is_valid("qu")
    assert not schema.is_valid("abcde")

def test_number_custom_validator():
    fn = lambda value, greater: value >= greater
    v.add_validator("number", "greater", fn)
    schema = v.number().test("greater", 3)
    assert schema.is_valid(3)
    assert not schema.is_valid(0)
    assert not schema.range(-3, 2).is_valid(3)
    assert not schema.range(-3, 2).is_valid(-1)
    assert not schema.required().is_valid(None)

    fn2 = lambda value, values: value in values
    v.add_validator("number", "isin", fn2)
    schema = v.number().test("isin", [1, 1, 3, 5, 30, 133, -200])
    assert schema.is_valid(30)
    assert not schema.is_valid(100)
    assert schema.positive().is_valid(1)
    assert not schema.is_valid(-200)
    assert not schema.is_valid(10)

    v.add_validator("number", "div", lambda value, div: True if value % div == 0 else False)
    assert schema.required().positive().range(-10, 13).test("div", 2).is_valid(8)
    assert schema.is_valid(-6)
    assert not schema.is_valid(22)

def test_list_custom_validator():
    fn = lambda value, req: req in value
    v.add_validator("list", "req_element", fn)
    schema = v.list().test("req_element", 3)
    assert schema.is_valid([0, 3, -3])
    assert not schema.is_valid(None)
    assert not schema.is_valid([1, 2, 5])

    fn2 = lambda value, sorted_: True if sorted(value) == value and sorted_ is True else False
    v.add_validator("list", "is_sorted", fn2)
    schema = v.list().test("is_sorted", True)
    assert schema.is_valid([0, 1, 3])
    assert not schema.is_valid([3, 2, 67])
    assert not schema.test("is_sorted", False).is_valid([0, 3, -10])
    assert not schema.is_valid([1, 2, 3])

    assert schema.sizeof(3).test("req_element", "apple").is_valid(["apple", "appleee", 3])
    assert not schema.is_valid(["apple"])
    assert not schema.is_valid(["app", "le", "pie"])



def test_complex_functions():
    fn_num = lambda value: value % 2 == 0
    v.add_validator("number", "is_even", fn_num)
    fn_str = lambda value, banned_words: len([word for word in value.split() if word.lower().strip() in banned_words]) == 0
    v.add_validator("string", "is_banned_words_in_str", fn_str)
    fn_list = lambda value, word, amount: len([w for w in value if w == word]) == amount
    v.add_validator("list", "given_amount", fn_list)
    import re
    fn_email = lambda value: False if re.search(r"[^@\n]+@[^@\n]+\.[^@\n]{2,6}", value) is None else True
    v.add_validator("string", "email", fn_email)

    # test strings
    schema = v.string().test("is_banned_words_in_str", ["rediska", "sosiska"])
    assert schema.is_valid("good string")
    assert not schema.is_valid("rediska ~")
    assert not schema.min_len(20).is_valid("apelsinka")
    assert schema.min_len(33).min_len(3).is_valid("abc")
    assert not schema.is_valid("sosiska sosiska")

    schema = v.string().test("email")
    assert schema.is_valid("jane_doe@mail.ru")
    assert not schema.is_valid("not a email")

    # test nums
    schema = v.number().test("is_even")
    assert schema.is_valid(8)
    assert not schema.is_valid(3)
    assert schema.test("isin", [1, 2, 3]).is_valid(3)

    # test list
    schema = v.list().test("given_amount", "pineapple", 2)
    assert schema.is_valid(["pineapple", "apple", "pineapple"])
    assert not schema.is_valid(["pine", "apple"])
    assert not schema.sizeof(3).is_valid(["pineapple", "pineapple"])

def test_dict_custom_validator():
    schema = v.dict()
    schema.shape({
        "name": v.string().required().test("max_length", 13),
        "email": v.string().test("email"),
        "age": v.number().positive().test("greater", 18),
        "pets": v.list().test("req_element", "cat")
    })
    assert schema.is_valid({
        "name": "Masha",
        "email": "supermasha@icloud.com",
        "age": 22,
        "pets": ["cat", "cat"]
    })
    assert not schema.is_valid({
        "name": None,
        "email": "supermasha@icloud.com",
        "age": 25,
        "pets": ["cat"]
    })
    assert not schema.is_valid({
        "name": "Masha Aleksandrovna",
        "email": "supermasha@icloud.com",
        "age": 25,
        "pets": ["cat"]
    })
    assert not schema.is_valid({
        "name": "Masha",
        "email": "supermasha@ququmail",
        "age": 25,
        "pets": ["cat"]
    })
    assert not schema.is_valid({
        "name": "Masha",
        "email": "supermasha@icloud.com",
        "age": 12,
        "pets": ["cat"]
    })
    assert not schema.is_valid({
        "name": "Masha",
        "email": "supermasha@icloud.com",
        "age": 28,
        "pets": ["rabbit", "maxim"]
    })

    fn_dict = lambda value, search_word: search_word in value.keys()
    v.add_validator("dict", "search", fn_dict)
    assert schema.test("search", "pets").is_valid({
        "name": "Masha",
        "email": "supermasha@icloud.com",
        "age": 28,
        "pets": ["rabbit", "cat"]
    })
    assert not schema.test("search", "abc").is_valid({
        "name": "Masha",
        "email": "supermasha@icloud.com",
        "age": 28,
        "pets": ["rabbit", "cat"]
    })
    assert not schema.test("search", "pets").is_valid({
        "name": "Mashka",
        "email": "supermasha_icloud.com",
        "age": 10,
        "pets": ["rabbit", "cat"]
    })

def test_type_error():
    schema = v.string().test("max_length", "3")
    assert not schema.is_valid("mandarin")

def test_unknown_func_error():
    with pytest.raises(AttributeError):
        schema = v.string().test("does not exist", 3)

    with pytest.raises(AttributeError):
        schema = v.list().test("byaka")