import pytest
from pathlib import Path
from utils import validate_input_path, collect_input_paths


def test_accepts_supported_file(tmp_path: Path):
    image_file = tmp_path / "test.jpg"
    image_file.write_text("dummy")

    result = validate_input_path(str(image_file))
    assert result == image_file


def test_rejects_unsupported_extension(tmp_path: Path):
    text_file = tmp_path / "test.txt"
    text_file.write_text("dummy")

    with pytest.raises(ValueError):
        validate_input_path(str(text_file))


def test_accepts_directory(tmp_path: Path):
    directory = tmp_path / "images"
    directory.mkdir()

    result = validate_input_path(str(directory))
    assert result == directory


def test_collects_image_files_from_directory(tmp_path: Path):
    directory = tmp_path / "batch"
    directory.mkdir()
    (directory / "image1.jpg").write_text("dummy")
    (directory / "image2.png").write_text("dummy")
    (directory / "ignore.txt").write_text("dummy")
    nested = directory / "nested"
    nested.mkdir()
    (nested / "image3.jpeg").write_text("dummy")

    image_paths = collect_input_paths(directory)
    assert len(image_paths) == 3
    assert all(path.suffix.lower() in {".jpg", ".jpeg", ".png"} for path in image_paths)


def test_collect_input_paths_raises_when_directory_empty(tmp_path: Path):
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()

    with pytest.raises(ValueError):
        collect_input_paths(empty_dir)
