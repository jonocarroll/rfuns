import math

from rfuns import abs, ceiling, exp, floor, log, log10, log2, sign, sqrt, trunc


def test_math_vectorised_functions():
    assert sign([-1, 0, 2]) == [-1, 0, 1]
    assert trunc([1.9, -1.1]) == [1, -1]
    assert ceiling([1.2, -1.2]) == [2, -1]
    assert floor([1.8, -1.8]) == [1, -2]
    assert sqrt([4, 9]) == [2.0, 3.0]
    assert log([1, math.e]) == [0.0, 1.0]
    assert log([8, 4], base=2) == [3.0, 2.0]
    assert log2([2, 4]) == [1.0, 2.0]
    assert log10([10, 100]) == [1.0, 2.0]
    assert exp([0, 1]) == [1.0, math.e]
    assert abs([-1, 0, 1]) == [1, 0, 1]
