from analyzer import analyze_metadata

def test_detects_gps():
    metadata = {
        "gps": {
            "decimal_latitude": 10.0,
            "decimal_longitude": 20.0
        }
    }

    result = analyze_metadata(metadata)

    assert result["gps_present"] is True

def test_detects_editing_software():
    metadata = {
        "camera": {
            "software": "Adobe Photoshop"
        }
    }

    result = analyze_metadata(metadata)

    assert result["editing_software_detected"] is True

def test_detects_phone_device():
    metadata = {
        "camera": {
            "make": "Apple"
        }
    }

    result = analyze_metadata(metadata)

    assert result["device_type"] == "phone"

def test_detects_missing_exif():
    metadata = {}

    result = analyze_metadata(metadata)

    assert result["exif_missing"] is True

def test_detects_valid_datetime():
    metadata = {
        "datetime": {
            "datetimeoriginal": "2024-05-01T10:00:00"
        }
    }

    result = analyze_metadata(metadata)

    assert result["datetime_valid"] is True