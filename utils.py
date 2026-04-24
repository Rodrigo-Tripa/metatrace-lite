import os

def validate_input_path(path):
    # Define the list of supported image file extensions
    allowed_extensions = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp")

    # Check if the provided path exists on the system
    if not os.path.exists(path):
        raise FileNotFoundError(f"Path does not exist: {path}")

    # Ensure the path points to a file and not a directory
    if not os.path.isfile(path):
        raise ValueError(f"Path is not a file: {path}")

    # Verify that the file extension is supported
    if not path.lower().endswith(allowed_extensions):
        raise ValueError(f"Unsupported file type: {path}")

    return path