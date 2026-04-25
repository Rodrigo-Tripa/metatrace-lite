# Part of the MetaTrace Lite forensic framework, developed by Rodrigo-Tripa (GitHub).
# Module responsible for metadata processing, forensic analysis, and structured output handling.

import os
import json

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

def export_metadata_to_file(data, original_path, folder_name="reports"):
    # Cria a pasta automaticamente se não existir
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Gera o nome do relatório baseado no ficheiro original
    base_name = os.path.basename(original_path)
    file_name_no_ext = os.path.splitext(base_name)[0]
    report_path = os.path.join(folder_name, f"{file_name_no_ext}_report.json")

    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

    return report_path