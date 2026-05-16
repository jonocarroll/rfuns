import pytest  # type: ignore

from rfuns import r_range, strsplit
from tests.r_compare import assert_matches_r, r_available, r_status

# Explicit checks for consistency not relying on the wrapper and r2y2


def test_strsplit_matches_r():
    if not r_available():
        pytest.skip(r_status())

    value = strsplit(["abc def", "these words are split"], " ")
    assert_matches_r("strsplit", value, ["abc def", "these words are split"], split=" ")


def test_r_range_matches_r():
    if not r_available():
        pytest.skip(r_status())

    value = r_range([10, 2, 7])
    assert_matches_r("r_range", value, [10, 2, 7])
