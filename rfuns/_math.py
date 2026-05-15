import math as _math
from ._utils import _vec


@_vec(arg=0)
def sign(x):
    """Return -1, 0, or 1. Vectorised."""
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


@_vec(arg=0)
def trunc(x):
    """Truncate toward zero. Vectorised."""
    return int(x)


@_vec(arg=0)
def ceiling(x):
    """Ceiling. Vectorised."""
    return _math.ceil(x)


@_vec(arg=0)
def floor(x):
    """Floor. Vectorised."""
    return _math.floor(x)


@_vec(arg=0)
def sqrt(x):
    """Square root. Vectorised."""
    return _math.sqrt(x)


@_vec(arg=0)
def log(x, base=None):
    """Natural log, or log to given base. Vectorised."""
    if base is None:
        return _math.log(x)
    return _math.log(x, base)


@_vec(arg=0)
def log2(x):
    """Log base 2. Vectorised."""
    return _math.log2(x)


@_vec(arg=0)
def log10(x):
    """Log base 10. Vectorised."""
    return _math.log10(x)


@_vec(arg=0)
def exp(x):
    """e^x. Vectorised."""
    return _math.exp(x)


@_vec(arg=0)
def abs(x):
    """Absolute value. Vectorised."""
    if isinstance(__builtins__, dict):
        return __builtins__["abs"](x)
    return __builtins__.abs(x)


def var(x, na_rm=False):
    """Sample variance (ddof=1), like R's var()."""
    x = [v for v in x if v is not None] if na_rm else x
    n = len(x)
    if n < 2:
        return float("nan")
    mean = sum(x) / n
    return sum((v - mean) ** 2 for v in x) / (n - 1)


def sd(x, na_rm=False):
    """Sample standard deviation, like R's sd()."""
    return var(x, na_rm=na_rm) ** 0.5


def mean(x, na_rm=False):
    """Arithmetic mean. Like R's mean()."""
    x = [v for v in x if v is not None] if na_rm else x
    return sum(x) / len(x)


def median(x, na_rm=False):
    """Median. Like R's median()."""
    x = [v for v in x if v is not None] if na_rm else x
    s = sorted(x)
    n = len(s)
    mid = n // 2
    if n % 2 == 0:
        return (s[mid - 1] + s[mid]) / 2
    return s[mid]


def quantile(x, probs=None, na_rm=False):
    """
    Sample quantiles, like R's quantile().
    probs: list of probabilities in [0, 1]. Defaults to [0, 0.25, 0.5, 0.75, 1].
    Uses R's type 7 method (linear interpolation).
    """
    if probs is None:
        probs = [0, 0.25, 0.5, 0.75, 1]
    x = [v for v in x if v is not None] if na_rm else list(x)
    s = sorted(x)
    n = len(s)
    result = []
    for p in probs:
        if p == 0:
            result.append(s[0])
        elif p == 1:
            result.append(s[-1])
        else:
            h = (n - 1) * p
            lo, hi = int(h), int(h) + 1
            result.append(s[lo] + (h - lo) * (s[hi] - s[lo]))
    return result


def scale(x, center=True, scale_=True):
    """Centre and/or scale x, like R's scale()."""
    if center:
        m = mean(x)
        x = [v - m for v in x]
    if scale_:
        s = sd(x)
        x = [v / s for v in x]
    return x


def round(x, digits=0):
    """
    Round x to digits decimal places, like R's round().
    Note: uses round-half-to-even (banker's rounding), same as Python's built-in.
    R also uses this by default (IEC 60559 standard).
    """
    import builtins

    if isinstance(x, (list, tuple)):
        return [builtins.round(v, digits) for v in x]
    return builtins.round(x, digits)
