from typing import Any, Callable, Dict, Tuple

try:
    import rpy2.robjects as ro  # type: ignore
    import rpy2.robjects.vectors as rvec  # type: ignore
except ImportError:  # pragma: no cover
    ro = None
    rvec = None

R_NAME_MAP = {
    "file_exists": "file.exists",
    "dir_exists": "dir.exists",
    "file_path": "file.path",
    "r_range": "range",
    "prop_table": "prop.table",
    "margin_table": "margin.table",
    "which_min": "which.min",
    "which_max": "which.max",
}

# R comparison not meaningful or possible for these
R_SKIP_FUNCTIONS = frozenset(
    {
        # Python-specific construct
        "vec",
        "rstr",
        # Functional helpers — can't serialise Python callables to R
        "lapply",
        "sapply",
        "vapply",
        "tapply",
        "rapply",
        "Filter",
        "Map",
        "Reduce",
        # File ops: tests use tmp_path; filesystem paths differ
        "list_files",
        "file_exists",
        "dir_exists",
        "basename",
        "dirname",
        "file_path",
        # Intentionally different semantics
        "prop_table",
        "margin_table",
        "scale",  # R returns a matrix with attributes
        "summary",  # R returns named vector, Python returns dict
        "quantile",  # different return structure
        "formatC",  # printf formatting may differ by platform
        "round",  # both use round-half-to-even, but edge cases differ
        "nrow",
        "ncol",
        "dim",  # Python only handles list-of-lists
    }
)

# Skip a specific *call* (not all calls) when the predicate returns True
R_SKIP_PREDICATES: Dict[str, Callable[[list, dict], bool]] = {
    # Empty-list args hit Python-specific recycling behaviour that R doesn't have
    "paste": lambda args, kwargs: any(a == [] for a in args),
    "paste0": lambda args, kwargs: any(a == [] for a in args),
}

# Rename Python kwargs → R kwargs (Python uses underscores; R uses dots)
R_KWARG_RENAMES: Dict[str, Dict[str, str]] = {
    "grepl": {"ignore_case": "ignore.case"},
    "grep": {"ignore_case": "ignore.case"},
    "gsub": {"ignore_case": "ignore.case"},
    "sub": {"ignore_case": "ignore.case"},
    "mean": {"na_rm": "na.rm"},
    "var": {"na_rm": "na.rm"},
    "sd": {"na_rm": "na.rm"},
    "median": {"na_rm": "na.rm"},
    "seq": {"length_out": "length.out"},
}


def _rename_kwargs(name: str, kwargs: dict) -> dict:
    renames = R_KWARG_RENAMES.get(name, {})
    return {renames.get(k, k): v for k, v in kwargs.items()}


# ---------------------------------------------------------------------------
# Arg transforms: name → (args: list, kwargs: dict) → (args, kwargs)
# Applied to args *before* calling R.
# ---------------------------------------------------------------------------


def _substr_args(args: list, kwargs: dict) -> Tuple[list, dict]:
    """Python substr uses 0-based inclusive indices; R uses 1-based inclusive."""
    args = list(args)
    for i in (1, 2):
        if i < len(args):
            v = args[i]
            args[i] = [x + 1 for x in v] if isinstance(v, list) else v + 1
    return args, kwargs


def _trimws_args(args: list, kwargs: dict) -> Tuple[list, dict]:
    """Python trimws uses 'l'/'r'; R uses 'left'/'right'."""
    _map = {"l": "left", "r": "right", "both": "both"}
    kwargs = dict(kwargs)
    if "which" in kwargs:
        kwargs["which"] = _map.get(kwargs["which"], kwargs["which"])
    if len(args) > 1:
        args = list(args)
        args[1] = _map.get(args[1], args[1])
    return args, kwargs


def _log_args(args: list, kwargs: dict) -> Tuple[list, dict]:
    """Drop base=None so R uses its default (natural log)."""
    kwargs = {k: v for k, v in kwargs.items() if not (k == "base" and v is None)}
    return args, kwargs


R_ARG_TRANSFORMS: Dict[str, Callable] = {
    "substr": _substr_args,
    "trimws": _trimws_args,
    "log": _log_args,
}


# ---------------------------------------------------------------------------
# Result transforms: name → (py_result, orig_args, orig_kwargs) → comparable
# Applied to the Python result before comparing to the R result.
# ---------------------------------------------------------------------------


def _to_1based(result: Any, args: tuple, kwargs: dict) -> Any:
    """Convert 0-based index(es) to 1-based to match R."""
    if isinstance(result, list):
        return [x + 1 for x in result]
    return result + 1


def _grep_result(result: Any, args: tuple, kwargs: dict) -> Any:
    if kwargs.get("value", False):
        return result
    return [x + 1 for x in result]


def _strsplit_result(result: Any, args: tuple, kwargs: dict) -> Any:
    """R always returns list-of-vectors; Python returns a flat list for scalar input."""
    if isinstance(result, list) and (not result or not isinstance(result[0], list)):
        return [result]
    return result


def _table_result(result: Any, args: tuple, kwargs: dict) -> Any:
    """Extract counts in sorted-key order from Python dict to match R's named vector."""
    if isinstance(result, dict):
        return [result[k] for k in sorted(result.keys())]
    return result


def _seq_result(result: Any, args: tuple, kwargs: dict) -> Any:
    """seq(n) and seq(length_out=n) are 0-based in Python, 1-based in R; add 1."""
    has_explicit_to = len(args) >= 2 or "to" in kwargs
    return result if has_explicit_to else [x + 1 for x in result]


R_RESULT_TRANSFORMS: Dict[str, Callable] = {
    "which": _to_1based,
    "which_min": _to_1based,
    "which_max": _to_1based,
    "seq_along": _to_1based,
    "seq_len": _to_1based,
    "table": _table_result,
    "seq": _seq_result,
    "grep": _grep_result,
    "strsplit": _strsplit_result,
}


# ---------------------------------------------------------------------------
# Core utilities
# ---------------------------------------------------------------------------


def r_status() -> str:
    if ro is None or rvec is None:
        return "rpy2 is not installed"
    try:
        ro.r("NULL")
        return "ok"
    except Exception as exc:
        return f"R is not available: {exc}"


def r_available() -> bool:
    return r_status() == "ok"


def _py2r(value: Any):
    if ro is None or rvec is None:
        raise RuntimeError("rpy2 is not available")
    if isinstance(value, rvec.Vector):
        return value
    if isinstance(value, bool):
        return ro.BoolVector([value])
    if isinstance(value, int):
        return ro.IntVector([value])
    if isinstance(value, float):
        return ro.FloatVector([value])
    if isinstance(value, str):
        return ro.StrVector([value])
    if isinstance(value, (list, tuple)):
        if not value:
            return ro.StrVector([])
        if any(isinstance(item, (list, tuple)) for item in value):
            return ro.ListVector([_py2r(item) for item in value])
        first = next((v for v in value if v is not None), None)
        if isinstance(first, bool):
            return ro.BoolVector(list(value))
        if isinstance(first, int):
            return ro.IntVector(list(value))
        if isinstance(first, float):
            return ro.FloatVector(list(value))
        return ro.StrVector([str(v) for v in value])
    return ro.StrVector([str(value)])


def _normalise(value: Any) -> Any:
    """Convert rpy2 objects and Python containers to plain Python values."""
    if value is None or isinstance(value, (bool, int, float, str, bytes)):
        return value
    if rvec is not None:
        if isinstance(value, rvec.ListVector):
            return [_normalise(item) for item in value]
        if isinstance(value, rvec.Vector):
            return [_normalise(item) for item in value]
    if isinstance(value, dict):
        return {key: _normalise(val) for key, val in value.items()}
    if isinstance(value, (list, tuple)):
        return [_normalise(v) for v in value]
    return value


def _resolve_r_name(name: str) -> str:
    return R_NAME_MAP.get(name, name)


def call_r(name: str, *args: Any, **kwargs: Any) -> Any:
    if not r_available():
        raise EnvironmentError(r_status())
    assert ro is not None
    r_fn = ro.r[_resolve_r_name(name)]
    r_args = [_py2r(arg) for arg in args]
    r_kwargs = {key: _py2r(val) for key, val in kwargs.items()}
    result = r_fn(*r_args, **r_kwargs)
    return _normalise(result)


def _results_equal(py_val: Any, r_val: Any) -> bool:
    """Compare values accounting for R returning length-1 vectors where Python returns scalars."""
    if isinstance(r_val, list) and len(r_val) == 1 and not isinstance(py_val, list):
        return py_val == r_val[0]
    return py_val == r_val


def assert_matches_r(name: str, py_result: Any, *args: Any, **kwargs: Any) -> None:
    if not r_available():
        raise EnvironmentError(r_status())
    if name in R_SKIP_FUNCTIONS:
        return
    if name in R_SKIP_PREDICATES and R_SKIP_PREDICATES[name](list(args), kwargs):
        return

    r_args = list(args)
    r_kwargs = dict(kwargs)
    if name in R_ARG_TRANSFORMS:
        r_args, r_kwargs = R_ARG_TRANSFORMS[name](r_args, r_kwargs)
    r_kwargs = _rename_kwargs(name, r_kwargs)

    r_value = call_r(name, *r_args, **r_kwargs)

    py_value = py_result
    if name in R_RESULT_TRANSFORMS:
        py_value = R_RESULT_TRANSFORMS[name](py_result, args, kwargs)

    if not _results_equal(py_value, r_value):
        raise AssertionError(
            f"Python result did not match R for {name}(...).\n"
            f"Python: {py_value!r}\n"
            f"R:      {r_value!r}\n"
            f"R call: {_resolve_r_name(name)}({r_args}, {r_kwargs})"
        )
