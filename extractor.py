import exifread

def extract_metadata(path):
    # Open the image file in binary mode and process EXIF tags
    with open(path, 'rb') as file:
        dados_limpo = exifread.process_file(file)

    metadata = {}

    for key, value in dados_limpo.items():
        # Filter out noise tags like Thumbnails or Padding to keep data clean
        if "Thumbnail" in key or "Padding" in key:
            continue

        # Convert tags and values to strings to ensure JSON serializability
        key_str = str(key)
        value_str = str(value)
        metadata[key_str] = value_str

    # Structure the final result including the source filename
    result = {
        "filename": path,
        "metadata": metadata
    }

    return result