def head(x, n=6):
    """Return first n elements, like R's head()."""
    return x[:n]


def tail(x, n=6):
    """Return last n elements, like R's tail()."""
    return x[-n:]


def length(x):
    """Length of x, like R's length()."""
    return len(x)


def nrow(x):
    """Number of rows of a list-of-lists. Like R's nrow()."""
    return len(x)


def ncol(x):
    """Number of columns of a list-of-lists (assumes rectangular). Like R's ncol()."""
    if len(x) == 0:
        return 0
    return len(x[0])


def dim(x):
    """Return [nrow, ncol] of a list-of-lists. Like R's dim()."""
    return [nrow(x), ncol(x)]


def summary(x):
    """
    Basic numeric summary, like R's summary() on a numeric vector.
    Returns a dict with Min, Q1, Median, Mean, Q3, Max.
    """
    from ._math import quantile, mean as _mean

    q = quantile(x, [0, 0.25, 0.5, 0.75, 1])
    return {
        "Min": q[0],
        "Q1": q[1],
        "Median": q[2],
        "Mean": _mean(x),
        "Q3": q[3],
        "Max": q[4],
    }


def rstr(x):
    """
    Compact display of object structure, loosely like R's str().
    Named rstr to avoid shadowing Python's str().
    """
    t = type(x).__name__
    if isinstance(x, list):
        inner = type(x[0]).__name__ if x else "?"
        prefix = "..." if len(x) > 5 else ""
        print(f"list [{inner}] of length {len(x)}: {x[:5]}{prefix}")
    elif isinstance(x, dict):
        print(f"dict with {len(x)} keys: {list(x.keys())[:5]}")
    else:
        print(f"{t}: {x}")
