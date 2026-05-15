from collections import Counter


def table(x):
    """
    Frequency table of x, sorted by name, like R's table().
    Returns a dict of {value: count}.
    """
    return dict(sorted(Counter(x).items()))


def prop_table(x):
    """
    Proportional frequency table, like R's prop.table().
    Returns a dict of {value: proportion}.
    """
    counts = table(x)
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}


def margin_table(x):
    """
    Marginal sums of a contingency table (dict).
    For a flat table, total is returned.
    """
    if isinstance(x, dict):
        return sum(x.values())
    raise TypeError("x must be a dict (as returned by table())")
