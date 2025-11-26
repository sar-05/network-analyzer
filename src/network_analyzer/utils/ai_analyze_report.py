import json  # noqa: D100
import os
from pathlib import Path

import openai


def reporte_analisis_ia(nombre_archivo):
    archivo_prompt = r"C:\Users\TTOCI\OneDrive\Documentos\GitHub\network-analyzer\prompts\prompt_v1.txt"
    archivo_api_key = r"C:\Users\TTOCI\OneDrive\Documentos\GitHub\network-analyzer\src\network_analyzer\utils\api_key_openai.txt"
    archivo_analisis = buscar_archivo(nombre_archivo, r"C:\Users\TTOCI\OneDrive\Documentos\GitHub\network-analyzer")

    try:
        validar_rutas(archivo_prompt, archivo_api_key)

        with Path.open(archivo_api_key, "r", encoding="utf-8") as f:
            api_key = f.read().strip()

        with Path.open(archivo_prompt, "r", encoding="utf-8") as f:
            archivo_prompt_texto = f.read()

        user_prompt_text = cargar_analisis_json(archivo_analisis)

        print("Rutas para el prompt y api key validadas correctamente.")

        prompt_final = archivo_prompt_texto + "\n" + user_prompt_text

        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "user", "content": prompt_final},
                ],
        )
        print(response.choices[0].message.content)

    except Exception as e:
        print(f"Error: {e}")



def validar_rutas(prompt_json_path: str, key_path: str):  # noqa: D103

    if not Path(prompt_json_path).is_file():
        msg = f"El archivo del prompt JSON no existe: {prompt_json_path}"
        raise FileNotFoundError(msg)

    if not Path(key_path).is_file():
        msg = f"El archivo que contiene la API KEY no existe: {key_path}"
        raise FileNotFoundError(msg)

    return True

def cargar_analisis_json(prompt_json_prueba_path: str):  # noqa: D103

    with Path.open(prompt_json_prueba_path, "r", encoding="utf-8") as h:
        data = json.load(h)

    if isinstance(data, dict):
        analysis_text = json.dumps(data, ensure_ascii=False, indent=2)
    else:
        msg = "El analisis debe ser un objeto JSON válido (dict)."
        raise TypeError(msg)

    return analysis_text


def buscar_archivo(nombre_archivo: str, carpeta_base: str):
    for root, dirs, files in os.walk(carpeta_base):
        if nombre_archivo in files:
            return os.path.join(root, nombre_archivo)
    return None
