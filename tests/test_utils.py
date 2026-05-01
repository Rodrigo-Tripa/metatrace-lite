import pytest
from utils import validate_input_path

def test_accepts_jpg():
    result = validate_input_path("samples/test.jpg")
    assert result is not None


def test_rejects_txt():
    with pytest.raises(ValueError):
        validate_input_path("samples/test.txt")

def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        validate_input_path("samples/none.jpg")

def test_rejects_directory():
    with pytest.raises(ValueError):
        validate_input_path("samples")