# Name: MetaTrace Lite
# Author: Rodrigo-Tripa (GitHub)
# Description: Lightweight forensic tool for extracting and analyzing image metadata (EXIF).
# Version: 0.2.0-alpha

from utils import validate_input_path
from extractor import extract_metadata
from analyzer import analyze_metadata
import json
import sys
import logging

# Configure logging: levels and format
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def main():
    # 1. Verify command line arguments
    if len(sys.argv) < 2:
        logger.warning("Usage: python3 main.py <image_path>")
        return

    # 2. Retrieve the input file path
    path = sys.argv[1]

    try:
        # 3. Validate the input path and file type
        validated_path = validate_input_path(path)

        # 4. Extract metadata from the validated path
        result = extract_metadata(validated_path)
        analysis = analyze_metadata(result["metadata"])
        result["analysis"] = analysis

        # 5. Print the structured result as JSON
        # (Note: standard print is kept here as it is the tool's intended data output)
        print(json.dumps(result, indent=4))

    except FileNotFoundError:
        logger.error(f"File not found: {path}")
    except PermissionError:
        logger.error(f"Permission denied: {path}")
    except ValueError as ve:
        logger.error(f"Input validation error: {ve}")
    except (IOError, EOFError) as e:
        logger.error(f"Failed to process image file: {e}")


if __name__ == "__main__":
    main()