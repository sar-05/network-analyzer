import json
from pathlib import Path

import openai

import logging

logger = logging.getLogger(__name__)


def reporte_analisis_ia(
    archivo_json: Path, archivo_prompt: Path, archivo_api_key: Path
):
    try:
        with archivo_api_key.open("r", encoding="utf-8") as f:
            api_key = f.read().strip()

        with archivo_prompt.open("r", encoding="utf-8") as f:
            archivo_prompt_texto = f.read()

        user_prompt_text = cargar_analisis_json(archivo_json)

        logger.info("Rutas para el prompt y api key validadas correctamente.")

        prompt_final = archivo_prompt_texto + "\n" + user_prompt_text

        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "user", "content": prompt_final},
            ],
        )
        return response.choices[0].message.content

    except Exception:
        logger.error("Unable to get AI analysis.")


def cargar_analisis_json(prompt_json_prueba_path: Path):
    with prompt_json_prueba_path.open("r", encoding="utf-8") as h:
        data = json.load(h)

    if isinstance(data, dict):
        analysis_text = json.dumps(data, ensure_ascii=False, indent=2)
    else:
        msg = "El analisis debe ser un objeto JSON válido (dict)."
        raise TypeError(msg)

    return analysis_text
