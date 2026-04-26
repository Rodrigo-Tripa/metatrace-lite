# Name: MetaTrace Lite
# Author: Rodrigo-Tripa (GitHub)
# Description: Lightweight forensic tool for extracting and analyzing image metadata (EXIF).
# Version: 0.2.8.1

from utils import validate_input_path, export_metadata_to_file
from extractor import extract_metadata
from analyzer import analyze_metadata
import argparse
import json
import sys
import logging

# Configure logging: levels and format
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def main():
    # 1. Setup Argument Parser for better CLI experience
    parser = argparse.ArgumentParser(
        description="MetaTrace Lite: Lightweight forensic tool for image metadata analysis."
    )
    parser.add_argument("path", help="Path to the image file to analyze.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable debug logging.")
    
    args = parser.parse_args()
    
    # Adjust log level based on verbosity flag
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    path = args.path

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

        # 6. Export metadata to a JSON file
        report_file = export_metadata_to_file(result, validated_path)
        logger.info(f"Report successfully exported to: {report_file}")

    except FileNotFoundError:
        logger.error(f"File not found: {path}")
        sys.exit(1)
    except PermissionError:
        logger.error(f"Permission denied: {path}")
        sys.exit(1)
    except ValueError as ve:
        logger.error(f"Input validation error: {ve}")
        sys.exit(1)
    except (IOError, EOFError) as e:
        logger.error(f"Failed to process image file: {e}")
        sys.exit(1)
    except Exception as e:
        logger.critical(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()