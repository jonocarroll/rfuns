from rfuns import (
    nchar,
    grepl,
    grep,
    gsub,
    sub,
    paste,
    paste0,
    trimws,
    toupper,
    tolower,
    startsWith,
    endsWith,
    strsplit,
    substr,
    chartr,
    formatC,
    nzchar,
)


def test_nchar_scalar():
    assert nchar("hello") == 5


def test_nchar_vector():
    assert nchar(["hi", "hello", ""]) == [2, 5, 0]


def test_grepl_scalar():
    assert grepl("he", "hello")
    assert not grepl("x", "hello")


def test_grepl_vector():
    assert grepl("he", ["hello", "world", "hey"]) == [True, False, True]


def test_grepl_ignore_case():
    assert grepl("HE", "hello", ignore_case=True)


def test_gsub():
    assert gsub("o", "0", "foobar") == "f00bar"
    assert gsub("o", "0", ["foo", "boo"]) == ["f00", "b00"]


def test_sub():
    assert sub("o", "0", "foobar") == "f0obar"


def test_paste():
    assert paste("a", "b", "c") == "a b c"
    assert paste(["a", "b"], ["x", "y"]) == ["a x", "b y"]
    assert paste(["a", "b"], collapse="-") == "a-b"
    assert paste("butter", "fly") == "butter fly"
    assert paste(["butter", "house"], "fly") == ["butter fly", "house fly"]
    assert paste(["a", "b", "c"], ["st", "nd", "rd"]) == ["a st", "b nd", "c rd"]
    assert paste(["a", "b"], ["x", "y", "z"], sep="_*_") == ["a_*_x", "b_*_y", "a_*_z"]
    assert paste(["a", "b"], ["x", "y"], collapse="; ") == "a x; b y"
    assert paste("1st", "2nd", "3rd", sep=", ") == "1st, 2nd, 3rd"


def test_paste_zero_length():
    assert paste("foo", [], "bar", collapse="|") == "foo  bar"
    assert paste([], collapse="|") == ""
    assert paste([]) == []


def test_grep_and_grepl():
    letters = [chr(c) for c in range(ord("a"), ord("z") + 1)]
    assert grep("[a-z]", letters) == list(range(0, 26))
    assert grep("foo", ["foo", "bar", "foo"], value=True) == ["foo", "foo"]
    assert grep("foo", ["foo", "bar", "foo"], value=False, invert=True) == [1]
    assert grepl("foo", ["foo", "bar", "foo"]) == [True, False, True]


def test_sub_and_gsub():
    assert sub(r" +$", "", "trail   ") == "trail"
    assert gsub(r"([ab])", r"\1_\1_", "abc and ABC") == "a_a_b_b_c a_a_nd ABC"


def test_trimws_behavior():
    assert trimws("  a \t\n") == "a"
    assert trimws("  a \t\n", which="l") == "a \t\n"
    assert trimws("  a \t\n", which="r") == "  a"


def test_strsplit_behavior():
    assert strsplit("a.b.c", ".", fixed=True) == ["a", "b", "c"]
    assert strsplit("a.b.c", "[.]") == ["a", "b", "c"]
    assert strsplit("", " ") == []
    assert strsplit(" ", " ") == [""]


def test_strsplit_vectorised():
    assert strsplit(["abc def", "these words are split"], " ") == [
        ["abc", "def"],
        ["these", "words", "are", "split"],
    ]


def test_string_vectorised_functions():
    assert nchar(["a", ""]) == [1, 0]
    assert grepl("a", ["a", "b"]) == [True, False]
    assert gsub("o", "0", ["foo", "boo"]) == ["f00", "b00"]
    assert sub("o", "0", ["foo", "boo"]) == ["f0o", "b0o"]
    assert trimws([" a ", " b"], which="both") == ["a", "b"]
    assert toupper(["a", "b"]) == ["A", "B"]
    assert tolower(["A", "B"]) == ["a", "b"]
    assert startsWith(["foo", "bar"], "f") == [True, False]
    assert endsWith(["foo", "bar"], "o") == [True, False]
    assert substr(["hello", "world"], 1, 3) == ["ell", "orl"]
    assert chartr("ab", "AB", ["abc", "bab"]) == ["ABc", "BAB"]
    assert nzchar(["a", ""]) == [True, False]
    assert formatC([1.23, 4.56], digits=1, format="f") == ["1.2", "4.6"]


def test_substr_recycling():
    assert substr(["abcdef", "xyz"], [1, 0], [3, 1]) == ["bcd", "xy"]


def test_chartr_and_case():
    x = "MiXeD cAsE 123"
    assert chartr("iXs", "why", x) == "MwheD cAyE 123"
    assert chartr("a-cX", "D-Fw", "aXc") == "DwF"
    assert toupper(x) == "MIXED CASE 123"
    assert tolower(x) == "mixed case 123"
    assert startsWith("foobar", "foo")
    assert not startsWith("foobar", "bar")
    assert endsWith("foobar", "bar")
    assert not endsWith("foobar", "foo")


def test_formatC():
    assert formatC(1.23456, digits=2, format="f", width=6) == "  1.23"
    assert formatC(1234, digits=3, format="g") == "1.23e+03"


def test_paste0():
    assert paste0("a", "b") == "ab"
    assert paste0(["butter", "house"], "fly") == ["butterfly", "housefly"]
    assert paste0([1, 2, 3], ["st", "nd", "rd"]) == ["1st", "2nd", "3rd"]
    assert paste0(["1st", "2nd"], collapse=", ") == "1st, 2nd"


def test_trimws():
    assert trimws("  hi  ") == "hi"
    assert trimws(["  a ", " b"]) == ["a", "b"]


def test_toupper_tolower():
    assert toupper("hello") == "HELLO"
    assert tolower(["HI", "THERE"]) == ["hi", "there"]


def test_substr():
    assert substr("hello", 1, 3) == "ell"
    assert substr(["hello", "world"], 0, 2) == ["hel", "wor"]


def test_strsplit():
    assert strsplit("a,b,c", ",", fixed=True) == ["a", "b", "c"]


def test_nzchar():
    assert nzchar(["a", "", "b"]) == [True, False, True]
    assert nzchar(123) is True
    assert nzchar(0) is True
    assert nzchar("") is False
