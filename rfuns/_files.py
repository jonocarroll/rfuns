import os as _os
import re as _re
from ._utils import _vec


def list_files(
    path=".", pattern=None, recursive=False, full_names=False, all_files=False
):
    """
    List files in a directory, like R's list.files().

    Parameters
    ----------
    path : str
        Directory to list.
    pattern : str, optional
        Regex pattern to filter filenames.
    recursive : bool
        Whether to recurse into subdirectories.
    full_names : bool
        Whether to return full paths.
    all_files : bool
        Whether to include hidden files starting with a dot.
    """
    if recursive:
        names = []
        for root, dirs, filenames in _os.walk(path):
            rel_root = _os.path.relpath(root, path)
            if rel_root == ".":
                rel_root = ""
            for name in dirs + filenames:
                names.append(_os.path.join(rel_root, name) if rel_root else name)
    else:
        names = list(_os.listdir(path))

    if not all_files:
        names = [name for name in names if not _os.path.basename(name).startswith(".")]

    files = names

    if pattern:
        files = [f for f in files if _re.search(pattern, _os.path.basename(f))]

    if full_names:
        full_path = _os.path.abspath(path) if not _os.path.isabs(path) else path
        files = [
            f if _os.path.isabs(f) else _os.path.normpath(_os.path.join(full_path, f))
            for f in files
        ]
    elif not recursive:
        files = [_os.path.basename(f) for f in files]

    return sorted(files)


@_vec(arg=0)
def file_exists(path):
    """Return True if file exists. Like R's file.exists()."""
    return _os.path.isfile(path)


@_vec(arg=0)
def dir_exists(path):
    """Return True if directory exists. Like R's dir.exists()."""
    return _os.path.isdir(path)


@_vec(arg=0)
def basename(path):
    """Return filename component of path. Like R's basename()."""
    return _os.path.basename(path)


@_vec(arg=0)
def dirname(path):
    """Return directory component of path. Like R's dirname()."""
    return _os.path.dirname(path)


def file_path(*args):
    """Construct file paths, like R's file.path()."""
    return _os.path.join(*args)
