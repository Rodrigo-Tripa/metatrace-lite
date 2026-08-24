# MetaTrace Lite

![Version](https://img.shields.io/badge/version-0.4.2-blue)
![Status](https://img.shields.io/badge/status-stable-green)
![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.x-green)

Lightweight forensic tool focused on image metadata extraction, EXIF analysis, and forensic indicator detection.

Designed to support evidence inspection through structured metadata parsing, suspicious pattern detection, and clean JSON reporting.

---

## Overview

MetaTrace Lite is a modular Python-based forensic tool created for the inspection and preliminary analysis of image metadata.

**Important**: This tool is designed for **rapid triage and initial investigation** of metadata. It is not a complete forensic analysis platform. Use it to quickly identify candidates for deeper investigation, not as the sole basis for conclusions.

The project focuses on:

- EXIF metadata extraction and categorization
- GPS metadata detection and coordinate conversion with range validation
- Editing software identification
- Device type detection (phone vs camera)
- DateTime validation and parsing (with timezone awareness)
- GPS accuracy assessment (Dilution of Precision)
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

To run a forensic analysis on an image or a folder of images, use the following command:

```bash
python main.py [PATH] [OPTIONS]
```

### Available Arguments:

- `PATH`: The relative or absolute path to an image file or a directory containing images.
- `-o OUTPUT_DIR, --output-dir OUTPUT_DIR`: Directory to save the report file(s) (default: `reports`).
- `-v, --verbose`: Enable debug logging.
- `-h, --help`: Show the help message and list all available options.

### Examples

#### Single file analysis
```bash
python main.py samples/photo.jpg
```

Output: Single JSON object to stdout + report saved to `reports/photo_report.json`

#### Batch processing directory
```bash
python main.py samples/ -o my_reports/
```

Output: Summary with list of results + individual reports in `my_reports/`

#### With verbose logging
```bash
python main.py samples/photo.jpg -v
```

Output: Debug logs to console + JSON output + saved report

#### Process all images in nested directories
```bash
python main.py /path/to/evidence/ -o forensic_reports/
```

The tool recursively finds all supported image files.

---

## Testing

The project includes automated tests to ensure reliability and correctness. To run the tests:

```bash
pytest
```

Run with verbose output:

```bash
pytest -v
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
- **DateTime**: Original, digitized timestamps (parsed to ISO 8601 format)
- **GPS**: Coordinates (converted to decimal degrees with range validation), altitude, DOP
- **Image**: Resolution, orientation, exposure settings, sensor data
- **Other**: Miscellaneous tags

---

### 2. Enhanced Data Parsing

- GPS coordinates converted to decimal degrees for better usability
- DateTime fields parsed into ISO 8601 format (note: timezone information is not stored in EXIF)
- Automatic filtering of noisy tags (thumbnails, padding)
- JSON-compatible value conversion
- **NEW**: GPS coordinate range validation (latitude -90 to 90, longitude -180 to 180)

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
- Paint.NET
- Krita
- Inkscape
- Darktable
- Capture One
- Luminar
- RAW Therapee

#### Device Type Detection

Classifies capture device as:

- Phone (Apple, Samsung, Huawei, Xiaomi, Google, OnePlus)
- Camera (other manufacturers)
- Unknown

#### DateTime Validation

Verifies presence of valid timestamp information.

**Important**: EXIF timestamps do not include timezone information. A timestamp like `2021-05-15T14:30:45` could represent any timezone. When analyzing events, always cross-reference with other evidence (GPS, network logs, etc.).

#### GPS Accuracy Assessment

Evaluates GPS precision based on Dilution of Precision (DOP):

- High (< 2)
- Medium (2-5)
- Low (> 5)
- Unknown/No GPS

Lower DOP values indicate better accuracy. However, even high accuracy GPS can be spoofed or incorrect due to device issues.

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
        },
        "image": {
            "exif_image_width": "4032",
            "exif_image_height": "3024"
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
        "highlights": "Captured on mobile device; Contains GPS data (medium accuracy)"
    }
}
```

---

## Batch Processing Output

When processing multiple files, the output includes a summary:

```json
{
    "summary": {
        "total_processed": 15,
        "total_failed": 0
    },
    "results": [
        { ... },
        { ... }
    ]
}
```

If any files fail to process, a `failed` array is included:

```json
{
    "summary": {
        "total_processed": 14,
        "total_failed": 1
    },
    "results": [ ... ],
    "failed": [
        {
            "filename": "corrupt_image.jpg",
            "error": "Failed to extract metadata: ..."
        }
    ]
}
```

---

## Known Limitations

### Metadata Trust

EXIF metadata is not inherently trustworthy.

It can be:

- modified
- removed
- rewritten
- sanitized
- forged

Never rely exclusively on metadata for attribution. Always cross-reference with other evidence sources (network logs, device forensics, witness testimony, etc.).

---

### GPS Reliability

GPS structures may exist without usable coordinates. Some files contain partial GPS tags only.

Coordinate conversion assumes standard formats. Invalid coordinates (outside valid ranges) are rejected.

**Important**: GPS coordinates can be spoofed. High accuracy DOP values do not guarantee authentic location data. Always verify GPS evidence with other sources.

---

### DateTime Reliability

EXIF timestamps do not include timezone information. A device with incorrect time settings will produce inaccurate timestamps.

**Important**: Use timestamps as starting points for investigation, not definitive proof. Cross-reference with:
- System logs
- Network traffic timestamps
- Other device logs
- Witness statements

---

### File Format Limitations

Some formats (especially PNG and WebP) may contain limited or no EXIF information.

This is expected behavior and reflects the design of these formats.

Format support:
- JPG/JPEG: Full EXIF support
- TIFF: Full EXIF support
- PNG: Limited EXIF support (metadata stored differently)
- GIF: Limited support
- BMP: Limited support
- WebP: Limited support

---

## Out of Scope

MetaTrace Lite is **metadata-focused only**. It does **NOT**:

- Analyze pixel data or detect image manipulation/splicing
- Perform reverse image search or attribution
- Detect steganography (hidden data in images)
- Recover deleted EXIF data or metadata shadows
- Analyze image hashes or verify digital signatures
- Perform deep forensic analysis (carving, recovery, etc.)
- Support video file metadata extraction

For these capabilities, use specialized tools like:
- **Pixel Analysis**: PhotoDNA, Reverse Image Search
- **Steganography Detection**: OutGuess, Stegdetect
- **Deep Forensics**: Autopsy, EnCase, FTK
- **Hash Analysis**: NIST NSRL, DuplicateImageDetector

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
- sensitive facilities

**Do not disclose sensitive metadata without operational necessity.**

Follow the Principle of Least Privilege:
- Only share metadata relevant to the investigation
- Redact sensitive information before sharing reports
- Document data handling and access logs

---

### Proper Evidence Handling

When using this tool in forensic investigations:

1. Work on forensic images/copies, not original media
2. Maintain chain of custody documentation
3. Document all tools and versions used
4. Preserve report integrity (use checksums)
5. Follow local legal and regulatory requirements

---

## Roadmap

- [x] Refactor to `pathlib` and `argparse`.
- [x] Structured metadata extraction with categorization.
- [x] GPS coordinate conversion to decimal degrees.
- [x] GPS coordinate range validation.
- [x] Enhanced forensic analysis (device type, datetime, GPS accuracy).
- [x] Readable JSON output with summary section.
- [x] Batch processing support (directories).
- [x] Improved error handling and logging.
- [ ] XMP and ICC Profile data extraction.
- [ ] HTML report generation.
- [ ] Simplified Web Interface for evidence upload.
- [ ] Support for image manipulation detection (preliminary).
- [ ] Video file metadata extraction.

## Contributing

Pull requests are welcome.

Guidelines:

- keep code modular
- preserve forensic consistency
- avoid unnecessary dependencies
- prioritize reliability over features
- include tests for new features
- document limitations clearly

In forensic tooling:

**correctness > complexity**

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

**Do not use against systems, files, or evidence you are not legally authorized to inspect.**

Unauthorized forensic collection may violate local law and operational policy.

Users are responsible for ensuring compliance with applicable laws and regulations in their jurisdiction.

---

## Author

Developed by Rodrigo-Tripa

---

## Changelog

### Version 0.4.2 (Current)
- **Fixed**: DateTime validation now correctly checks for `datetime_original` and `datetime_digitized` keys
- **Fixed**: GPS DOP parsing now uses robust float conversion instead of fragile `.isdigit()` check
- **Fixed**: EXIF tag categorization now correctly places "Image *" tags in image category instead of camera
- **Added**: GPS coordinate range validation (latitude -90/90, longitude -180/180)
- **Added**: Comprehensive logging in analyzer and extractor
- **Added**: Batch processing summary with success/failure counts
- **Improved**: DateTime parser documentation with timezone limitations
- **Improved**: GPS coordinate parser documentation with validation notes
- **Expanded**: Software detection list (added Paint.NET, Krita, Inkscape, etc.)

### Version 0.4.1
- Initial stable release
- Core EXIF extraction functionality
- Basic forensic analysis
