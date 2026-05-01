# MetaTrace Lite

![Version](https://img.shields.io/badge/version-0.4.0-blue)
![Status](https://img.shields.io/badge/status-stable-green)
![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.x-green)

Lightweight forensic tool focused on image metadata extraction, EXIF analysis, and forensic indicator detection.

Designed to support evidence inspection through structured metadata parsing, suspicious pattern detection, and clean JSON reporting.

---

## Overview

MetaTrace Lite is a modular Python-based forensic tool created for the inspection and preliminary analysis of image metadata.

The project focuses on:

- EXIF metadata extraction and categorization
- GPS metadata detection and coordinate conversion
- Editing software identification
- Device type detection (phone vs camera)
- DateTime validation and parsing
- GPS accuracy assessment
- Structured JSON forensic reporting with summaries

The objective is not attribution, but forensic visibility.

Metadata is evidence support — never final proof.

---

## Core Workflow

```text
Input Validation
        ↓
Metadata Extraction & Structuring
        ↓
Forensic Analysis
        ↓
Structured JSON Output with Summary
```

Modules are separated for integrity, maintainability, and forensic consistency.

---

## Usage

To run a forensic analysis on an image, use the following command:

```bash
python main.py [IMAGE_PATH] [OPTIONS]
```

### Available Arguments:

- `IMAGE_PATH`: The relative or absolute path to the image file (e.g., `.jpg`, `.tiff`).
- `-o OUTPUT_DIR, --output-dir OUTPUT_DIR`: Directory to save the report file (default: `reports`).
- `-v, --verbose`: Enable debug logging.
- `-h, --help`: Show the help message and list all available options.

---

## Testing

The project includes automated tests to ensure reliability and correctness. To run the tests:

```bash
pytest
```

Tests cover the core modules: `utils`, `analyzer`, and `extractor`.

---

## Project Cleanup

A cleanup script is provided to remove generated reports and sample files:

```bash
./cleanup.sh
```

This script will clean the `reports/` and `samples/` directories and optionally remove the `tests/` folder.

---

## Current Features

---

### 1. EXIF Metadata Extraction & Structuring

Uses `ExifRead` to extract available metadata from image files and organizes it into logical categories:

- **Camera**: Make, model, software
- **DateTime**: Original, digitized timestamps (parsed to ISO format)
- **GPS**: Coordinates (converted to decimal degrees), altitude, DOP
- **Image**: Resolution, orientation, exposure settings
- **Other**: Miscellaneous tags

---

### 2. Enhanced Data Parsing

- GPS coordinates converted to decimal degrees for better usability
- DateTime fields parsed into ISO 8601 format
- Automatic filtering of noisy tags (thumbnails, padding)
- JSON-compatible value conversion

---

### 3. Forensic Analysis Engine

Comprehensive analysis includes:

#### GPS Presence Detection

Checks for valid GPS coordinates and provides decimal conversion.

#### Editing Software Detection

Detects common editing tools such as:

- Adobe Photoshop
- GIMP
- Lightroom
- Canva
- Snapseed
- Affinity
- PicsArt

#### Device Type Detection

Classifies capture device as:

- Phone (Apple, Samsung, Huawei, Xiaomi, Google, OnePlus)
- Camera (other manufacturers)
- Unknown

#### DateTime Validation

Verifies presence of valid timestamp information.

#### GPS Accuracy Assessment

Evaluates GPS precision based on Dilution of Precision (DOP):

- High (< 2)
- Medium (2-5)
- Low (> 5)
- Unknown/No GPS

#### Missing EXIF Detection

Identifies files with no metadata (screenshots, exports, sanitized files).

---

### 4. Readable JSON Output with Summary

Every execution generates a detailed report with:

- **Filename**: Source file path
- **Metadata**: Categorized EXIF data
- **Analysis**: Forensic indicators
- **Summary**: Human-readable highlights (device, date, location, key findings)

---

### 5. Automatic JSON Reporting

Reports are automatically saved to the specified output directory.
The report filename is derived from the original image name (e.g., `image_report.json`).

---

### 6. Structured JSON Reporting

Example output:

```json
{
    "filename": "samples/example.jpg",
    "metadata": {
        "camera": {
            "make": "Apple",
            "model": "iPhone 12",
            "software": "12.1.2"
        },
        "datetime": {
            "datetime_original": "2021-05-15T14:30:45"
        },
        "gps": {
            "decimal_latitude": 40.7128,
            "decimal_longitude": -74.0060,
            "gpsaltitude": "10",
            "gpsdop": "3.5"
        }
    },
    "analysis": {
        "gps_present": true,
        "editing_software_detected": false,
        "exif_missing": false,
        "device_type": "phone",
        "datetime_valid": true,
        "gps_accuracy": "medium"
    },
    "summary": {
        "device": "Apple iPhone 12",
        "capture_date": "2021-05-15T14:30:45",
        "location": "Lat: 40.7128, Lon: -74.0060",
        "highlights": "Captured on mobile device; Contains GPS data"
    }
}
```

## Known Limitations

### Metadata Trust

EXIF metadata is not inherently trustworthy.

It can be:

- modified
- removed
- rewritten
- sanitized
- forged

Never rely exclusively on metadata for attribution.

---

### GPS Reliability

GPS structures may exist without usable coordinates.

Some files contain partial GPS tags only.

Coordinate conversion assumes standard formats.

---

### File Format Limitations

Some formats (especially PNG) may contain limited or no EXIF information.

This is expected behavior.

---

## Security Considerations

### Principle of Evidence Integrity

Original metadata must never be altered during analysis.

The tool separates:

- raw evidence (`metadata`)
- interpretation (`analysis`)
- summary (`summary`)

This is mandatory for forensic reliability.

---

### Sensitive Metadata Exposure

GPS coordinates may expose:

- exact locations
- home addresses
- operational sites

Do not disclose sensitive metadata without operational necessity.

Follow the Principle of Least Privilege.

---

## Roadmap

- [x] Refactor to `pathlib` and `argparse`.
- [x] Structured metadata extraction with categorization.
- [x] GPS coordinate conversion to decimal degrees.
- [x] Enhanced forensic analysis (device type, datetime, GPS accuracy).
- [x] Readable JSON output with summary section.
- [ ] Batch processing support (directories).
- [ ] XMP and ICC Profile data extraction.
- [ ] Simplified Web Interface for evidence upload.

## Contributing

Pull requests are welcome.

Guidelines:

- keep code modular
- preserve forensic consistency
- avoid unnecessary dependencies
- prioritize reliability over features

In forensic tooling:

correctness > complexity

always.

---

## License

MIT License

See:

```text
LICENSE
```

---

## Disclaimer

This tool is intended for authorized forensic inspection and security analysis only.

Do not use against systems, files, or evidence you are not legally authorized to inspect.

Unauthorized forensic collection may violate local law and operational policy.

---

## Author

Developed by Rodrigo-Tripa

GitHub:

https://github.com/rodrigo-tripa
