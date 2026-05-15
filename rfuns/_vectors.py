from ._utils import _vec


def which(x):
    """Return 0-based indices where x is True, like R's which() but Python-indexed."""
    return [i for i, v in enumerate(x) if v]


def which_min(x):
    """Return 0-based index of the minimum value."""
    return x.index(min(x))


def which_max(x):
    """Return 0-based index of the maximum value."""
    return x.index(max(x))


def diff(x, lag=1):
    """Return lagged differences of x."""
    return [x[i] - x[i - lag] for i in range(lag, len(x))]


def cumsum(x):
    """Cumulative sum."""
    result, total = [], 0
    for v in x:
        total += v
        result.append(total)
    return result


def cumprod(x):
    """Cumulative product."""
    result, total = [], 1
    for v in x:
        total *= v
        result.append(total)
    return result


def cummax(x):
    """Cumulative maximum."""
    result, current = [], x[0]
    for v in x:
        current = max(current, v)
        result.append(current)
    return result


def cummin(x):
    """Cumulative minimum."""
    result, current = [], x[0]
    for v in x:
        current = min(current, v)
        result.append(current)
    return result


def rev(x):
    """Reverse a list."""
    return list(reversed(x))


def duplicated(x):
    """Return boolean list: True where element has appeared earlier."""
    seen, result = set(), []
    for v in x:
        result.append(v in seen)
        seen.add(v)
    return result


def setdiff(x, y):
    """Elements in x not in y, preserving order."""
    sy = set(y)
    return [v for v in x if v not in sy]


def intersect(x, y):
    """Elements in both x and y, preserving order of x."""
    sy = set(y)
    return [v for v in x if v in sy]


def union(x, y):
    """Unique elements from x and y combined, preserving order."""
    seen, result = set(), []
    for v in list(x) + list(y):
        if v not in seen:
            result.append(v)
            seen.add(v)
    return result


def seq_along(x):
    """Return 0-based indices along x, like R's seq_along() but Python-indexed."""
    return list(range(len(x)))


def seq_len(n):
    """Return 0-based sequence of length n, like R's seq_len() but Python-indexed."""
    return list(range(n))


def seq(from_=0, to=None, by=None, length_out=None):
    """
    Generate a sequence, like R's seq(), but 0-based by default.
    seq(0, 9), seq(0, 10, by=2), seq(length_out=5), seq(5)
    """
    if to is None and length_out is None:
        return list(range(from_))
    if length_out is not None:
        if to is None:
            to = from_ + length_out - 1
            from_ = 0
        step = (to - from_) / (length_out - 1)
        return [from_ + i * step for i in range(length_out)]
    by = by or 1
    result, v = [], from_
    assert to is not None
    while (by > 0 and v <= to) or (by < 0 and v >= to):
        result.append(v)
        v += by
    return result


@_vec(arg=0)
def sign(x):
    """Return -1, 0, or 1 depending on sign of x. Vectorised."""
    if x > 0:
        return 1
    elif x < 0:
        return -1
    return 0


def r_range(x):
    """
    Return [min, max] of x, like R's range().
    Named r_range to avoid shadowing builtin.
    """
    return [min(x), max(x)]


def unique(x):
    """Return unique elements preserving order."""
    seen, result = set(), []
    for v in x:
        if v not in seen:
            result.append(v)
            seen.add(v)
    return result
