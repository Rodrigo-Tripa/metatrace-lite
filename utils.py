import os

def validate_input_path(path):
    allowed_extensions = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp")

    if not os.path.exists(path):
        raise FileNotFoundError(f"Path does not exist: {path}")

    if not os.path.isfile(path):
        raise ValueError(f"Path is not a file: {path}")

    if not path.lower().endswith(allowed_extensions):
        raise ValueError(f"Unsupported file type: {path}")

    return path