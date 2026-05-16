import functools

from tests.r_compare import assert_matches_r, r_available


def pytest_addoption(parser):
    parser.addoption(
        "--r-check",
        action="store_true",
        default=False,
        help="Compare rfuns outputs against R via rpy2 for calls made in tests.",
    )


def _is_rfun_callable(value):
    if hasattr(value, "__wrapped__"):
        return False
    module = getattr(value, "__module__", "") or ""
    return callable(value) and module.startswith("rfuns")


def _wrap_rfun(value, name):
    @functools.wraps(value)
    def wrapper(*args, **kwargs):
        result = value(*args, **kwargs)
        if r_available():
            assert_matches_r(name, result, *args, **kwargs)
        return result

    wrapper.__wrapped__ = value
    return wrapper


def pytest_runtest_setup(item):
    if not item.config.getoption("--r-check"):
        return

    module = getattr(item, "module", None)
    if module is None or getattr(module, "_r_check_wrapped", False):
        return

    for name, value in list(vars(module).items()):
        if _is_rfun_callable(value):
            setattr(module, name, _wrap_rfun(value, name))

    setattr(module, "_r_check_wrapped", True)
