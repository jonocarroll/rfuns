from rfuns import table, prop_table


def test_table():
    result = table(["a", "b", "a", "c", "b", "a"])
    assert result == {"a": 3, "b": 2, "c": 1}


def test_table_sorted():
    result = table([3, 1, 2, 1, 3, 3])
    assert list(result.keys()) == [1, 2, 3]


def test_prop_table():
    result = prop_table(["a", "a", "b"])
    assert abs(result["a"] - 2 / 3) < 1e-10
    assert abs(result["b"] - 1 / 3) < 1e-10
