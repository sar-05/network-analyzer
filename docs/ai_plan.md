# 🧠 Plan de uso de inteligencia artificial (IA)

> Este documento forma parte del tercer entregable del proyecto PIA. Describe cómo se integrará IA en el flujo técnico del proyecto, con fines éticos, funcionales y reproducibles.

---

## 🎯 Propósito del uso de IA
  
> La IA se utilizara para la creación del reporte sobres los hallazgos realizados durante el análisis del escaneo, también se planea utilizarla para dar a conocer los cambios realizados y recomendaciones dadas una vez se realice la ultima tarea correspondiente a la respuesta del análisis.

---

## 🔗 Punto de integración en el flujo
  
> La IA se invocara al momento de terminar el análisis de la red, para dar los a conocer los primeros hallazgos relacionados con los dispositivos. Asi también se planea utilizarla al finalizar la tarea de respuesta, para hacer saber al usuario lo que se ha modificado y/o las recomendaciones.

---

## 🧰 Modelo o API previsto

- **Nombre del modelo/API**: GPT-4.1
- **Tipo de acceso**: API KEY
- **Dependencias técnicas**: Por definir

---

## 📝 Diseño inicial del prompt

> Breve descripción del tipo de instrucciones que se usarán para interactuar con el modelo.

- **Archivo de plantilla**: [`/prompts/prompt_v1.json`]
- **Campos incluidos**:
  - `GPT-4.1`
  - `Tarea: Elaboración del informe sobre el resultado del análisis de los equipos analizados en una red interna que arroja como resultado las debilidades encontradas en los puertos donde se encuentran conectados estos dispositivos`
  - `La ruta del template es la siguiente: /prompts/prompt_v1.json`
  - `Instrucciones: Del resultado del análisis realizado por el programa hecho en Python, analiza y despliega cuales son los puertos ordenados de mayor a menor vulnerabilidad que detectas que pueden ser susceptibles a un ataque y pone en riesgo la integridad de la información que contiene cada uno de los equipos que conforman la red para de esta manera realizar las correcciones necesarias para fortalecer la seguridad de la red`

---

## 🔐 Consideraciones éticas

> ¿Qué medidas se tomarán para evitar sesgos, asegurar transparencia y proteger la privacidad?
> Se le ha indica que la información sea totalmente verídica, que evite dar datos alarmistas, que indique no de recomendaciones genéricas y que muestre los resultados en idioma español

---

## 🧭 Observaciones

> Al no tener la información completa de como funciona la API, se considera indicarle a la IA no contemple resultados anteriores en caso de que guarde los prompts anteriores
