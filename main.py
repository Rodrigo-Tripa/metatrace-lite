from utils import validate_input_path
from extractor import extract_metadata
import json, sys

def main():
    # 1. verificar argumento
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <image_path>")
        return   # ⬅️ para aqui

    # 2. obter path
    path = sys.argv[1]

    try:
        # 3. validar
        path_validado = validate_input_path(path)

        # 4. extrair
        resultado = extract_metadata(path_validado)

        # 5. output
        print(json.dumps(resultado, indent=4))

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()