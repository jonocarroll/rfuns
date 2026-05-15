import os

from rfuns import list_files, basename, dirname, dir_exists, file_exists


def test_list_files_includes_directories(tmp_path):
    dir_a = tmp_path / "a"
    dir_a.mkdir()
    file_b = tmp_path / "b.txt"
    file_b.write_text("x")
    hidden = tmp_path / ".hidden"
    hidden.write_text("z")

    assert sorted(list_files(str(tmp_path))) == ["a", "b.txt"]
    assert sorted(list_files(str(tmp_path), full_names=True)) == [
        str(dir_a),
        str(file_b),
    ]
    assert sorted(list_files(str(tmp_path), all_files=True)) == [
        ".hidden",
        "a",
        "b.txt",
    ]

    assert file_exists([str(dir_a), str(file_b)]) == [False, True]
    assert dir_exists([str(dir_a), str(file_b)]) == [True, False]
    assert basename([str(dir_a), str(file_b)]) == ["a", "b.txt"]
    assert dirname([str(dir_a), str(file_b)]) == [str(tmp_path), str(tmp_path)]


def test_list_files_recursive_includes_directories(tmp_path):
    dir_a = tmp_path / "a"
    dir_a.mkdir()
    file_c = dir_a / "c.txt"
    file_c.write_text("y")

    assert sorted(list_files(str(tmp_path), recursive=True)) == [
        "a",
        os.path.join("a", "c.txt"),
    ]
    assert sorted(list_files(str(tmp_path), recursive=True, full_names=True)) == [
        str(dir_a),
        str(file_c),
    ]
