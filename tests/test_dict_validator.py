import pytest
from validator.validator import Validator

v = Validator()

def test_equality():
    schema1 = v.dict()
    schema2 = v.dict()
    assert not schema1 is schema2
    schema1.shape({
        "cat": v.string().required()
    })
    schema2.shape({
        "cat": v.string().required()
    })
    assert not schema1 is schema2

def test_standard():
    schema = v.dict()
    schema.shape({
        "name": v.string().required(),
        "age": v.number().positive()
    })
    assert schema.is_valid({"name": "kolya", "age": 100})
    assert schema.is_valid({"name": "SuperMasha", "age": 18})
    assert not schema.is_valid({"name": "", "age": 22})
    assert not schema.is_valid({"name": "Karin", "age": -100})

def test_shape_creation():
    schema = v.dict()
    schema.shape({
        "name": v.string().required(),
        "age": v.number().positive()
    })
    with pytest.raises(TypeError):
        schema.shape(["lalala"])
    with pytest.raises(TypeError):
        schema.shape({"name": "name", "age": v.number().positive()})

def test_validation():
    schema = v.dict()
    schema.shape({
        "flower": v.string().required().min_len(3),
        "type": v.string().min_len(1000).min_len(3),
        "avg_lifespan": v.number().positive().range(0, 500),
        "bloom_seasons": v.list().required()
    })
    assert schema.is_valid({
        "flower": "lavander",
        "type": "field plant",
        "avg_lifespan": 2,
        "bloom_seasons": ["spring"]
    })
    assert not schema.is_valid({
        "flower": "daisy",
        "type": "",
        "avg_lifespan": 1,
        "bloom_seasons": ["spring", "sommer"]
    })
    assert schema.is_valid({
        "flower": "oak",
        "type": "forest tree",
        "avg_lifespan": 500,
        "bloom_seasons": [None]
    })
    assert not schema.is_valid({
        "flower": "chrestmas tree",
        "type": "tree",
        "avg_lifespan": 10,
        "bloom_seasons": "sommer"
    })

def test_empty_shape():
    schema = v.dict()
    schema.shape({})
    assert not schema.is_valid({"name": "manechka"})
    assert schema.is_valid({})