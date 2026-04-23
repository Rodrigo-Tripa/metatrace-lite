import exifread

def extract_metadata(path):
    with open(path, 'rb') as file:
        dados_limpo = exifread.process_file(file)

    metadata = {}

    for key, value in dados_limpo.items():
        if "Thumbnail" in key or "Padding" in key:
            continue

        key_str = str(key)
        value_str = str(value)
        metadata[key_str] = value_str

    result = {
        "filename": path,
        "metadata": metadata
    }

    return result