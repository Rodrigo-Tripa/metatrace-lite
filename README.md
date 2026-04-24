# MetaTrace Lite

![Version](https://img.shields.io/badge/version-0.2.0--alpha-orange)
![Status](https://img.shields.io/badge/status-active%20development-yellow)
![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.x-green)

Lightweight forensic tool focused on image metadata extraction, EXIF analysis, and forensic indicator detection.

Designed to support evidence inspection through structured metadata parsing, suspicious pattern detection, and clean JSON reporting.

---

## Overview

MetaTrace Lite is a modular Python-based forensic tool created for the inspection and preliminary analysis of image metadata.

The project focuses on:

- EXIF metadata extraction
- GPS metadata detection
- Editing software identification
- Missing EXIF detection
- Structured JSON forensic reporting

The objective is not attribution, but forensic visibility.

Metadata is evidence support — never final proof.

---

## Core Workflow

```text
Input Validation
        ↓
Metadata Extraction
        ↓
Forensic Analysis
        ↓
Structured JSON Output
```

Modules are separated for integrity, maintainability, and forensic consistency.

---

## Current Features

---

### 1. EXIF Metadata Extraction

Uses `ExifRead` to extract available metadata from image files.

Examples:

- Camera manufacturer
- Camera model
- Original timestamp
- Editing software
- GPS metadata
- EXIF internal structures

---

### 2. Metadata Normalization

Ensures all extracted values are safely converted into JSON-compatible strings.

This avoids:

- serialization failures
- parser inconsistencies
- unsupported object output

---

### 3. Noise Filtering

Automatically ignores irrelevant or noisy EXIF tags such as:

- `Thumbnail`
- `Padding`

This improves readability and forensic focus.

---

### 4. Forensic Analysis Engine

Basic analysis currently includes:

#### GPS Presence Detection

Checks for:

- `GPS GPSLatitude`
- `GPS GPSLongitude`

Used to identify potential location exposure.

---

#### Editing Software Detection

Detects common editing tools such as:

- Adobe Photoshop
- GIMP
- Lightroom
- Canva
- Snapseed

Used as a forensic indicator of possible image processing.

---

#### Missing EXIF Detection

Detects absence of metadata.

Important for:

- screenshots
- exported images
- sanitized files
- possible metadata stripping

Absence of EXIF is not proof of tampering.

---

### 5. Structured JSON Reporting

Example output:

```json
{
    "filename": "samples/example.jpg",
    "metadata": {
        "Image Software": "Adobe Photoshop",
        "EXIF DateTimeOriginal": "2026:04:23 21:31:43"
    },
    "analysis": {
        "gps_present": false,
        "editing_software_detected": true,
        "exif_missing": false
    }
}
```

---

## Project Structure

```text
metatrace-lite/
│
├── main.py
├── extractor.py
├── analyzer.py
├── utils.py
├── requirements.txt
├── README.md
├── LICENSE
└── samples/
```

---

## Module Responsibilities

| File | Responsibility |
|---|---|
| `main.py` | CLI execution flow |
| `utils.py` | Input validation |
| `extractor.py` | EXIF metadata extraction |
| `analyzer.py` | Forensic analysis engine |
| `samples/` | Test images |

This separation preserves evidence integrity and simplifies expansion.

---

## Installation

```bash
git clone https://github.com/rodrigo-tripa/metatrace-lite.git
cd metatrace-lite

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

---

## Usage

### Single Image Analysis

```bash
python3 main.py <image_path>
```

### Example

```bash
python3 main.py samples/example.jpg
```

---

## Requirements

| Component | Required | Notes |
|---|---:|---|
| Python 3 | ✅ | Tested on Python 3.x |
| ExifRead | ✅ | Metadata extraction engine |

---

## Known Limitations

---

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

This requires deeper parsing in future versions.

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

### v0.2.x

- [ ] suspicious flags system
- [ ] partial GPS detection
- [ ] timestamp consistency analysis
- [ ] better error handling

### v0.3.x

- [ ] directory analysis support
- [ ] recursive scan mode
- [ ] output export (`--output report.json`)
- [ ] CLI flags (`--pretty`, `--json`, `--recursive`)

### Future

- [ ] GPS coordinate parsing
- [ ] forensic report generator
- [ ] metadata classification engine
- [ ] timeline correlation support

---

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
