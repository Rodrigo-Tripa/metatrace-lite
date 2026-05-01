from pathlib import Path
from extractor import extract_metadata

def test_image_without_exif():
    result = extract_metadata(Path("samples/test.jpg"))

    assert "filename" in result
    assert "metadata" in result

def test_returns_metadata_when_exif_exists():
    result = extract_metadata(Path("samples/test.jpg"))

    assert result["metadata"] != {}

