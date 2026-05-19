# rfuns <img src='rfuns_logo.png' align="right" height="138" />

rfuns is a Python package providing implementations of common base R functions, adapted for Python with 0-based indexing and vectorisation support. This was mainly built to address my own desire to use these functions in exactly the way I would use them in R, but without calling out to an R session. All of these are implemented in Python without external/non-standard dependencies. 

This is not intended to be used in production, and makes no guarantees about performance - this is purely for ergonomics of someone who usually writes code in R, but is using Python.

See this blog post for more info: [https://jcarroll.click/rfuns]()

## Installation

Install with uv:

    uv add rfuns

Or with pip:

    pip install rfuns

## Important notes

All indexing is 0-based, unlike R's 1-based system. Vectorisation is opt-in using the `vec()` function or `@_vec` decorator on your own functions. Some functions differ from standard Python equivalents to match R behavior, such as setdiff preserving order from the first argument.

## Examples

Trim whitespace from strings:

    from rfuns import trimws
    trimws(["  hello  ", "world "])
    # ['hello', 'world']

Split strings:

    from rfuns import strsplit
    strsplit("these words are split", " ") 
    # ["these", "words", "are", "split"]

Find indices of `True` values:

    from rfuns import which
    which([False, True, False, True])
    # [1, 3]

Find indices where vector equals a value:

    from rfuns import which, vec
    x = vec(['a', 'b', 'c', 'b'])
    which(x == 'b')
    # [1, 3]

(note that since Python is not vectorised, a simple `==` between a list and a value is `False`, so the list is wrapped in `vec()` which implements vectorised binary operations)

Generate sequences:

    from rfuns import seq, seq_len
    seq(2, 5)
    # [2, 3, 4, 5]

    seq_len(5)
    # [0, 1, 2, 3, 4]

Compute set difference preserving order:

    set([4, 3, 1, 2]) - set([2, 4])
    # {1, 3} 
    
    from rfuns import setdiff
    setdiff([4, 3, 1, 2], [2, 4])
    # [3, 1]

Apply math functions vectorised:

    from rfuns import abs, sqrt
    abs([-1, 2, -3])
    # [1, 2, 3]

    sqrt([81, 9, 4])
    # [9.0, 3.0, 2.0]

List files in a directory:

    from rfuns import list_files
    list_files(".")
    # ['file1.txt', 'file2.py']

## Implemented functions

The package includes utilities for strings, vectors, math operations, and file handling, working with vector arguments where possible. Functions are designed to work with Python data structures like lists and support manual vectorisation through the `vec()` wrapper.

Names based on R's dot-separated functions are written with underscores because Python identifiers cannot contain `.`. Functions marked with <sup>†</sup> are renamed from R-style dot names, and functions marked with <sup>‡</sup> are vectorised via the `_vec` decorator.

### Strings

- `nchar(x)` <sup>‡</sup>
- `nzchar(x)` <sup>‡</sup>
- `paste(*args, sep=" ", collapse=None)`
- `paste0(*args, collapse=None)`
- `grepl(pattern, x, ignore_case=False, fixed=False)` <sup>‡</sup>
- `grep(pattern, x, ignore_case=False, fixed=False, value=False, invert=False)`
- `gsub(pattern, replacement, x, ignore_case=False, fixed=False)` <sup>‡</sup>
- `sub(pattern, replacement, x, ignore_case=False, fixed=False)` <sup>‡</sup>
- `trimws(x, which="both", whitespace=r"[ \t\r\n]")` <sup>‡</sup>
- `toupper(x)` <sup>‡</sup>
- `tolower(x)` <sup>‡</sup>
- `startsWith(x, prefix)` <sup>‡</sup>
- `endsWith(x, suffix)` <sup>‡</sup>
- `strsplit(x, split, fixed=False)` <sup>‡</sup>
- `substr(x, start, stop)`
- `chartr(old, new, x)` <sup>‡</sup>
- `formatC(x, digits=6, format="g", width=None)` <sup>‡</sup>

### Vectors

- `which(x)`
- `which_min(x)` <sup>†</sup>
- `which_max(x)` <sup>†</sup>
- `diff(x, lag=1)`
- `cumsum(x)`
- `cumprod(x)`
- `cummax(x)`
- `cummin(x)`
- `rev(x)`
- `duplicated(x)`
- `setdiff(x, y)`
- `intersect(x, y)`
- `union(x, y)`
- `unique(x)`
- `seq_along(x)` 
- `seq_len(n)`
- `seq(from_=0, to=None, by=None, length_out=None)` (`from` is a reserved keyword)
- `sign(x)` <sup>‡</sup>
- `r_range(x)` (renamed to not conflict with `range()`)

### Math

- `sign(x)` <sup>‡</sup>
- `trunc(x)` <sup>‡</sup>
- `ceiling(x)` <sup>‡</sup>
- `floor(x)` <sup>‡</sup>
- `sqrt(x)` <sup>‡</sup>
- `log(x, base=None)` <sup>‡</sup>
- `log2(x)` <sup>‡</sup>
- `log10(x)` <sup>‡</sup>
- `exp(x)` <sup>‡</sup>
- `abs(x)` <sup>‡</sup>
- `var(x, na_rm=False)`
- `sd(x, na_rm=False)`
- `mean(x, na_rm=False)`
- `median(x, na_rm=False)`
- `quantile(x, probs=None, na_rm=False)`
- `scale(x, center=True, scale_=True)`
- `round(x, digits=0)`

### Files

- `list_files(path=".", pattern=None, all_files=False, full_names=False, recursive=False, ignore_case=False, include_dirs=False, no_dot=False)` <sup>†</sup>
- `file_exists(path)` <sup>†</sup> <sup>‡</sup>
- `dir_exists(path)` <sup>†</sup> <sup>‡</sup>
- `basename(path)` <sup>‡</sup>
- `dirname(path)` <sup>‡</sup>
- `file_path(*args)` <sup>†</sup>

### Table

- `table(x)`
- `prop_table(x)` <sup>†</sup>
- `margin_table(x)` <sup>†</sup>

### Functional

- `lapply(x, func)`
- `sapply(x, func)`
- `vapply(x, func, expected_type)`
- `tapply(x, index, func)`
- `rapply(x, func)`
- `Filter(func, x)`
- `Map(func, *args)`
- `Reduce(func, x, init=None, accumulate=False)`

### Inspect

- `head(x, n=6)`
- `tail(x, n=6)`
- `length(x)`
- `nrow(x)`
- `ncol(x)`
- `dim(x)`
- `summary(x)`
- `rstr(x)` (renamed to not conflict with `str()`)

### Utils

- `vec(x)`

## Development

The repository includes a `Makefile` for common tasks.

- `make install` installs the package in editable mode with dev dependencies.
- `make test` runs `pytest` on `tests/`.
- `make test-r` runs `pytest --r-check` and compares rfuns outputs against R when available.
- `make lint` runs `ruff` on `rfuns/` and `tests/`.
- `make format` formats code with `ruff`.
- `make clean` removes build artifacts and caches.
- `make repl` starts a Python REPL using `uv`.

R-backed comparison tests use `rpy2` and are only run when `rpy2` and R are available.

