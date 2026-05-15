from rfuns import (
    which,
    which_min,
    which_max,
    diff,
    cumsum,
    rev,
    duplicated,
    setdiff,
    intersect,
    union,
    seq_along,
    seq_len,
    seq,
    vec,
    r_range,
)


def test_which():
    assert which([True, False, True, False]) == [0, 2]


def test_which_min_max():
    assert which_min([3, 1, 2]) == 1
    assert which_max([3, 1, 2]) == 0


def test_diff():
    assert diff([1, 3, 6, 10]) == [2, 3, 4]


def test_cumsum():
    assert cumsum([1, 2, 3, 4]) == [1, 3, 6, 10]


def test_rev():
    assert rev([1, 2, 3]) == [3, 2, 1]


def test_duplicated():
    assert duplicated([1, 2, 1, 3, 2]) == [False, False, True, False, True]


def test_setdiff():
    assert setdiff([1, 2, 3, 4], [2, 4]) == [1, 3]


def test_intersect():
    assert intersect([1, 2, 3], [2, 3, 4]) == [2, 3]


def test_union():
    assert union([1, 2, 3], [2, 3, 4]) == [1, 2, 3, 4]


def test_seq_along():
    assert seq_along(["a", "b", "c"]) == [0, 1, 2]


def test_seq_len():
    assert seq_len(4) == [0, 1, 2, 3]


def test_seq_default_zero_based():
    assert seq(length_out=5) == [0, 1, 2, 3, 4]
    assert seq(5) == [0, 1, 2, 3, 4]
    assert seq(0, 4) == [0, 1, 2, 3, 4]
    assert seq(0, 5, by=2) == [0, 2, 4]


def test_vec_and_which():
    data = vec(["a", "b", "a"])
    assert which(data == "a") == [0, 2]
    assert data[1] == "b"
    assert data[1:] == vec(["b", "a"])
    assert data + ["x", "y", "z"] == ["ax", "by", "az"]


def test_vec_elementwise_comparisons():
    data = vec(["a", "b", "a", "c"])
    assert which(data == "a") == [0, 2]
    assert which(data != "a") == [1, 3]
    assert which(data == ["a", "b", "c", "d"]) == [0, 1]


def test_vec_arithmetic_and_slicing():
    numbers = vec([1, 2, 3, 4])
    assert numbers + 1 == [2, 3, 4, 5]
    assert numbers * [2, 2, 2, 2] == [2, 4, 6, 8]
    assert numbers[1:3] == vec([2, 3])


def test_r_range():
    assert r_range([3, 1, 4, 1, 5]) == [1, 5]
