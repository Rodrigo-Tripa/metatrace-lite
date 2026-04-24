from utils import validate_input_path
from extractor import extract_metadata
import json, sys

def main():
    # 1. Verify command line arguments
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <image_path>")
        return

    # 2. Retrieve the input file path
    path = sys.argv[1]

    try:
        # 3. Validate the input path and file type
        path_validado = validate_input_path(path)

        # 4. Extract metadata from the validated path
        resultado = extract_metadata(path_validado)

        # 5. Print the structured result as JSON
        print(json.dumps(resultado, indent=4))

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()