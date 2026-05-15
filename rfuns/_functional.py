def lapply(x, func):
    """Apply func to each element of x, return list. Like R's lapply()."""
    return [func(v) for v in x]


def sapply(x, func):
    """Apply func to each element of x, simplify if possible. Like R's sapply()."""
    result = [func(v) for v in x]
    return result


def vapply(x, func, expected_type):
    """
    Like sapply() but checks that each result is of expected_type.
    Like R's vapply() for type safety.
    """
    result = []
    for v in x:
        r = func(v)
        if not isinstance(r, expected_type):
            raise TypeError(
                f"vapply: result element {r!r} is {type(r).__name__}, "
                f"expected {expected_type.__name__}"
            )
        result.append(r)
    return result


def tapply(x, index, func):
    """
    Apply func to subsets of x grouped by index. Like R's tapply().
    Returns a dict of {group: result}.
    """
    groups = {}
    for v, k in zip(x, index):
        groups.setdefault(k, []).append(v)
    return {k: func(v) for k, v in sorted(groups.items())}


def rapply(x, func):
    """
    Recursively apply func to all non-list elements in a nested list.
    Like R's rapply().
    """
    if isinstance(x, list):
        return [rapply(v, func) for v in x]
    return func(x)


def Filter(func, x):
    """Return elements of x for which func returns True. Like R's Filter()."""
    return [v for v in x if func(v)]


def Map(func, *args):
    """Apply func element-wise across args. Like R's Map()."""
    return [func(*vals) for vals in zip(*args)]


def Reduce(func, x, init=None, accumulate=False):
    """
    Reduce x with func. Like R's Reduce().
    If accumulate=True, return all intermediate results.
    """
    import functools

    if accumulate:
        result = []
        acc = init if init is not None else x[0]
        start = 0 if init is not None else 1
        if init is None:
            result.append(x[0])
        for v in x[start:]:
            acc = func(acc, v)
            result.append(acc)
        return result
    if init is not None:
        return functools.reduce(func, x, init)
    return functools.reduce(func, x)
