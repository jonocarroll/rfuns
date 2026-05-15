import functools


class Vec(list):
    """A lightweight vector wrapper for elementwise operations."""

    @staticmethod
    def _is_vector(obj):
        return isinstance(obj, (list, tuple, Vec)) and not isinstance(obj, (str, bytes))

    def __getitem__(self, key):
        value = super().__getitem__(key)
        return self.__class__(value) if isinstance(key, slice) else value

    def __repr__(self):
        return f"Vec({list(self)})"

    def _binary(self, other, op):
        if self._is_vector(other):
            return Vec(op(a, b) for a, b in zip(self, other))
        return Vec(op(a, other) for a in self)

    def _rbinary(self, other, op):
        if self._is_vector(other):
            return Vec(op(b, a) for a, b in zip(self, other))
        return Vec(op(other, a) for a in self)

    def __eq__(self, other):  # type: ignore[override]
        return self._binary(other, lambda a, b: a == b)

    def __ne__(self, other):  # type: ignore[override]
        return self._binary(other, lambda a, b: a != b)

    def __lt__(self, other):  # type: ignore[override]
        return self._binary(other, lambda a, b: a < b)

    def __le__(self, other):  # type: ignore[override]
        return self._binary(other, lambda a, b: a <= b)

    def __gt__(self, other):  # type: ignore[override]
        return self._binary(other, lambda a, b: a > b)

    def __ge__(self, other):  # type: ignore[override]
        return self._binary(other, lambda a, b: a >= b)

    def __add__(self, other):  # type: ignore[override]
        return self._binary(other, lambda a, b: a + b)

    def __sub__(self, other):  # type: ignore[override]
        return self._binary(other, lambda a, b: a - b)

    def __mul__(self, other):  # type: ignore[override]
        return self._binary(other, lambda a, b: a * b)

    def __truediv__(self, other):  # type: ignore[override]
        return self._binary(other, lambda a, b: a / b)

    def __floordiv__(self, other):  # type: ignore[override]
        return self._binary(other, lambda a, b: a // b)

    def __mod__(self, other):  # type: ignore[override]
        return self._binary(other, lambda a, b: a % b)

    def __pow__(self, other):  # type: ignore[override]
        return self._binary(other, lambda a, b: a**b)

    def __and__(self, other):  # type: ignore[override]
        return self._binary(other, lambda a, b: a & b)

    def __or__(self, other):  # type: ignore[override]
        return self._binary(other, lambda a, b: a | b)

    def __xor__(self, other):  # type: ignore[override]
        return self._binary(other, lambda a, b: a ^ b)

    def __radd__(self, other):  # type: ignore[override]
        return self._rbinary(other, lambda a, b: a + b)

    def __rsub__(self, other):  # type: ignore[override]
        return self._rbinary(other, lambda a, b: a - b)

    def __rmul__(self, other):  # type: ignore[override]
        return self._rbinary(other, lambda a, b: a * b)

    def __rtruediv__(self, other):  # type: ignore[override]
        return self._rbinary(other, lambda a, b: a / b)

    def __rfloordiv__(self, other):  # type: ignore[override]
        return self._rbinary(other, lambda a, b: a // b)

    def __rmod__(self, other):  # type: ignore[override]
        return self._rbinary(other, lambda a, b: a % b)

    def __rpow__(self, other):  # type: ignore[override]
        return self._rbinary(other, lambda a, b: a**b)


def vec(x):
    """Wrap a list or tuple in a vectorised Vec object."""
    if isinstance(x, Vec):
        return x
    if isinstance(x, (list, tuple)):
        return Vec(x)
    return x


def _vec(arg=0, kwarg=None):
    """
    Decorator that vectorises a scalar function over a list or tuple.

    Parameters
    ----------
    arg : int
        Positional index of the argument to vectorise over (default 0).
    kwarg : str, optional
        Keyword argument name to vectorise over. Takes precedence over arg
        if the caller passes that argument by name.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if kwarg and kwarg in kwargs:
                target = kwargs[kwarg]
                if isinstance(target, (list, tuple)):
                    return [func(*args, **{**kwargs, kwarg: xi}) for xi in target]
            elif arg < len(args):
                target = args[arg]
                if isinstance(target, (list, tuple)):
                    return [
                        func(*args[:arg], xi, *args[arg + 1 :], **kwargs)
                        for xi in target
                    ]
            return func(*args, **kwargs)

        return wrapper

    return decorator
