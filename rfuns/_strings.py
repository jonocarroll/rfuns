import re as _re
from builtins import format as _pyformat
from itertools import zip_longest
from ._utils import _vec


def _expand_chartr_spec(spec):
    chars = []
    i = 0
    while i < len(spec):
        if (
            i + 2 < len(spec)
            and spec[i + 1] == "-"
            and spec[i] != "-"
            and spec[i + 2] != "-"
        ):
            start, end = ord(spec[i]), ord(spec[i + 2])
            step = 1 if start <= end else -1
            chars.extend(chr(c) for c in range(start, end + step, step))
            i += 3
        else:
            chars.append(spec[i])
            i += 1
    return "".join(chars)


@_vec(arg=0)
def nchar(x):
    """Return the number of characters in a string. Vectorised."""
    return len(x)


@_vec(arg=1)
def grepl(pattern, x, ignore_case=False, fixed=False):
    """Return True/False for each element of x matching pattern. Vectorised."""
    if fixed:
        return (pattern.lower() in x.lower()) if ignore_case else (pattern in x)
    flags = _re.IGNORECASE if ignore_case else 0
    return bool(_re.search(pattern, x, flags))


def grep(pattern, x, ignore_case=False, fixed=False, value=False, invert=False):
    """
    Return indices (0-based) of elements in x matching pattern.
    If value=True, return the matching values instead.
    """
    flags = _re.IGNORECASE if ignore_case else 0

    def matches(s):
        if fixed:
            return (pattern.lower() in s.lower()) if ignore_case else (pattern in s)
        return bool(_re.search(pattern, s, flags))

    if value:
        if invert:
            return [s for s in x if not matches(s)]
        return [s for s in x if matches(s)]
    if invert:
        return [i for i, s in enumerate(x) if not matches(s)]
    return [i for i, s in enumerate(x) if matches(s)]


@_vec(arg=2)
def gsub(pattern, replacement, x, ignore_case=False, fixed=False):
    """Replace all matches of pattern in x with replacement. Vectorised."""
    if fixed:
        if ignore_case:
            return _re.sub(_re.escape(pattern), replacement, x, flags=_re.IGNORECASE)
        return x.replace(pattern, replacement)
    flags = _re.IGNORECASE if ignore_case else 0
    return _re.sub(pattern, replacement, x, flags=flags)


@_vec(arg=2)
def sub(pattern, replacement, x, ignore_case=False, fixed=False):
    """Replace the first match of pattern in x with replacement. Vectorised."""
    if fixed:
        if ignore_case:
            return _re.sub(
                _re.escape(pattern), replacement, x, count=1, flags=_re.IGNORECASE
            )
        return x.replace(pattern, replacement, 1)
    flags = _re.IGNORECASE if ignore_case else 0
    return _re.sub(pattern, replacement, x, count=1, flags=flags)


@_vec(arg=0)
def trimws(x, which="both", whitespace=r"[ \t\r\n]"):
    """Strip whitespace from strings. which: 'both', 'left', 'right'. Vectorised."""
    which = which.lower()
    if which.startswith("l"):
        return _re.sub(rf"^{whitespace}+", "", x)
    if which.startswith("r"):
        return _re.sub(rf"{whitespace}+$", "", x)
    if which.startswith("b"):
        return _re.sub(rf"^{whitespace}+|{whitespace}+$", "", x)
    raise ValueError("which must be 'both', 'left', or 'right'")


@_vec(arg=0)
def toupper(x):
    """Convert string to uppercase. Vectorised."""
    return x.upper()


@_vec(arg=0)
def tolower(x):
    """Convert string to lowercase. Vectorised."""
    return x.lower()


@_vec(arg=0)
def startsWith(x, prefix):
    """Return True if x starts with prefix. Vectorised."""
    return x.startswith(prefix)


@_vec(arg=0)
def endsWith(x, suffix):
    """Return True if x ends with suffix. Vectorised."""
    return x.endswith(suffix)


@_vec(arg=0)
def strsplit(x, split, fixed=False):
    """Split string x by split pattern. Returns list of lists. Vectorised."""
    if split == "":
        return list(x) if x else []
    if x == "":
        return []
    if fixed:
        parts = x.split(split)
        if split and x.endswith(split):
            parts = parts[:-1]
        return parts
    parts = _re.split(split, x)
    if parts and parts[-1] == "" and _re.search(rf"(?:{split})$", x):
        parts = parts[:-1]
    return parts


def _recycle_args(*args):
    lengths = [len(arg) if isinstance(arg, (list, tuple)) else 1 for arg in args]
    if 0 in lengths:
        return []
    maxlen = max(lengths)
    expanded = []
    for arg in args:
        if isinstance(arg, (list, tuple)):
            expanded.append([arg[i % len(arg)] for i in range(maxlen)])
        else:
            expanded.append([arg] * maxlen)
    return list(zip_longest(*expanded))


def substr(x, start, stop):
    """Extract substring from start to stop (0-based, inclusive). Vectorised."""
    if (
        isinstance(x, (list, tuple))
        or isinstance(start, (list, tuple))
        or isinstance(stop, (list, tuple))
    ):
        pairs = _recycle_args(x, start, stop)
        return [substr(xi, si, so) for xi, si, so in pairs]
    if start < 0:
        start = 0
    if stop is None or stop >= len(x):
        stop = len(x) - 1
    if start >= len(x) or stop < start:
        return ""
    return x[start : stop + 1]


def paste(*args, sep=" ", collapse=None):
    """
    Concatenate vectors element-wise with sep, like R's paste().
    If collapse is given, further joins the result into a single string.
    """
    lists = [a if isinstance(a, (list, tuple)) else [a] for a in args]
    if not lists:
        return "" if collapse is not None else []

    maxlen = max(len(lst) for lst in lists)
    if maxlen == 0:
        return "" if collapse is not None else []

    expanded = []
    for lst in lists:
        if len(lst) == 0:
            expanded.append([""] * maxlen)
        elif len(lst) == maxlen:
            expanded.append(lst)
        else:
            repeat = (maxlen + len(lst) - 1) // len(lst)
            expanded.append((lst * repeat)[:maxlen])

    result = [sep.join(str(items[i]) for items in expanded) for i in range(maxlen)]
    if collapse is not None:
        return collapse.join(result)
    if len(result) == 1:
        return result[0]  # scalar in, scalar out
    return result


def paste0(*args, collapse=None):
    """paste() with sep=''. Equivalent to R's paste0()."""
    return paste(*args, sep="", collapse=collapse)


@_vec(arg=2)
def chartr(old, new, x):
    """Replace characters in old with corresponding characters in new. Vectorised."""
    if isinstance(old, (list, tuple)):
        old = old[0]
    if isinstance(new, (list, tuple)):
        new = new[0]
    old_chars = _expand_chartr_spec(old)
    new_chars = _expand_chartr_spec(new)
    if len(old_chars) > len(new_chars):
        raise ValueError("old contains more characters than new")
    mapping = {ord(o): n for o, n in zip(old_chars, new_chars)}
    return x.translate(mapping)


@_vec(arg=0)
def nzchar(x):
    """Return True if string is non-empty. Vectorised."""
    return len(str(x)) > 0


@_vec(arg=0)
def formatC(x, digits=6, format="g", width=None):
    """Format numbers as strings. Vectorised."""
    fmt = f"{width if width else ''}.{digits}{format}"
    return _pyformat(x, fmt)
