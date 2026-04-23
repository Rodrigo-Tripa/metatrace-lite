# MetaTrace

![Version](https://img.shields.io/badge/version-0.1--alpha-orange)
![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.x-green)

Lightweight forensic tool for extracting and analyzing image metadata (EXIF).

---

## Objective

Provide a simple and modular tool for:

* Extracting EXIF metadata from images
* Structuring metadata into JSON format
* Preparing data for forensic analysis

---

## Features

### 1. **EXIF Extraction**

Reads metadata using `exifread`:

* Camera information
* Timestamps (`DateTimeOriginal`)
* Software used
* GPS structures (if present)

---

### 2. **Data Normalization**

* Converts all metadata to string format
* Ensures compatibility with JSON output
* Removes non-serializable objects

---

### 3. **Noise Filtering**

Ignores non-relevant tags:

* `Thumbnail`
* `Padding`

---

### 4. **JSON Output**

Structured output:

```json
{
  "filename": "image.jpg",
  "metadata": {
    "EXIF DateTimeOriginal": "...",
    "Image Software": "..."
  }
}
```

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

```bash
python3 main.py <image_path>
```

### Example

```bash
python3 main.py samples/exp.jpg
```

---

## Requirements

| Component | Required | Notes               |
| --------- | -------- | ------------------- |
| Python 3  | ✅        | Tested on 3.x       |
| exifread  | ✅        | Metadata extraction |

---

## Known Limitations

### File Format

* PNG images may not contain full EXIF data
* Some metadata fields may be missing

### Data Integrity

* EXIF metadata can be modified or removed
* No authenticity validation implemented

### Parsing

* Output depends on image source and encoding
* Some tags may appear inconsistent

---

## Roadmap

* [ ] Directory support (multiple images)
* [ ] CLI flags (`--json`, `--pretty`)
* [ ] Basic forensic analysis module
* [ ] Metadata filtering and classification
* [ ] GPS parsing (coordinates)

---

## Tool Security

### Metadata Trust

* EXIF data is **not trustworthy**
* Can be modified or stripped (MITRE ATT&CK T1565)

### Recommendations

* Do not rely solely on metadata for attribution
* Cross-check with additional forensic sources
* Avoid exposing sensitive metadata (e.g. GPS)

---

## Contributing

Pull requests are welcome.

* Keep code modular
* Follow current structure
* Avoid unnecessary dependencies

---

## License

MIT License - see [LICENSE](LICENSE)

---

## Disclaimer

This tool is intended for forensic analysis on systems and files you are authorized to inspect.

---

## Contact

GitHub: https://github.com/rodrigo-tripa
