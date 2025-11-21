# 🔗 Entregable 3 – Integración parcial y plan de IA

> Este entregable forma parte del repositorio único del proyecto PIA. La propuesta técnica se encuentra en \[`/proposals/proposal.md`].

---

## 🧪 Tareas integradas

- **Acquisition**: Sebastián Alighieri Ramirez
- **Analysis**: Julio Abraham Puente Guerrero
- **Descripción de la integración**: Para esta fase, se implementó un menú para dar la oportunidad al usuario de customizar los datos que desea extraer dadas las opciones que podamos ofrecer, al final de configuración, se obtiene un json con los datos que cumplan con los requisitos. Esto ayudara a que en la siguiente tarea sea mas fácil de interpretar las instrucciones que debe realizar la siguiente tarea sobre los equipos que se esten analizando.

---

## 🧬 Uso de dos lenguajes de programación

- **Lenguajes utilizados**: Python
- **Forma de integración**: Por el momento el proyecto se centra en extraer información de los dispositivos conectados a una red y determinar que acciones y recomendaciones se daría a cada dispositivo localizado a través de un json. Como tarea final se propondrá la posibilidad de poder modificar configuraciones del equipo de acuerdo a los resultados obtenidos utilizando otro lenguaje como bash en el caso de Linux.

---

## 🧠 Plan de uso de IA

- **Propósito del uso de IA**:
  > La IA se utilizara para la creación del reporte sobres los hallazgos realizados durante el análisis del escaneo, también se planea utilizarla para dar a conocer los cambios realizados y recomendaciones dadas una vez se realice la ultima tarea correspondiente a la respuesta del análisis.

- **Punto de integración en el flujo**:
  > La IA se invocara al momento de terminar el análisis de la red, para dar los a conocer los primeros hallazgos relacionados con los dispositivos. Asi también se planea utilizarla al finalizar la tarea de respuesta, para hacer saber al usuario lo que se ha modificado y/o las recomendaciones.

- **Modelo/API previsto**: GPT-4.1

- **Archivo del plan**: [`/docs/ai_plan.md`]

---

## 📝 Prompt inicial

- **Archivo de plantilla**: 

[`/prompts/prompt\_v1.json`]
- **Campos incluidos**:
  - `Versión: GPT-4.1`
  - `Tarea: Elaboración del informe sobre el resultado del análisis de los equipos analizados en una red interna que arroja como resultado las debilidades encontradas en los puertos donde se encuentran conectados estos dispositivos`
  - `La ruta del template es la siguiente: /prompts/prompt_v1.json`
  - `Instrucciones: Del resultado del análisis realizado por el programa hecho en Python, analiza y despliega cuales son los puertos ordenados de mayor a menor vulnerabilidad que detectas que pueden ser susceptibles a un ataque y pone en riesgo la integridad de la información que contiene cada uno de los equipos que conforman la red para de esta manera realizar las correcciones necesarias para fortalecer la seguridad de la red`

---

## 🤝 Colaboración
- **Sebastián Alighieri Ramirez:** Creacion de el menú para adaptar los resultados de acuerdo a la petición del usuario (Direccionamiento IP, Sistemas operativos, servicios, numero de dispositivos, numero de puertos)
- **Julio Abraham Puente Guerrero:** Tomar del informe los datos como puertos, sistema operativo y servicios (de acuerdo a lo que solicito el usuario) con lo que se ira armando el json. Y documentación de ia_plan.md y creación de la primera versión del prompt.
- **Alberto Jessier Lucio Sital:** Documentación de los avances realizados, asi como de la subida de las evidencias a Teams
---

## 🧭 Observaciones

> Se decidio utilizar la version de IA GPT-4.1 al considerarse la versión mas estable de las que hemos utilizado y para los fines que se están usando, nos parece la mas indicada. Primeramente ejecutaremos esta primera versión del prompt y obtendremos los resultados del mismo, para posteriormente realizar los ajustes en el prompt necesarios hasta obtener los resultados deseados.
