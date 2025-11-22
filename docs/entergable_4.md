# 🧩 Entregable 4 – Proyecto casi completo

> Este entregable forma parte del repositorio único del proyecto PIA. La propuesta técnica se encuentra en [`/proposals/propuesta.md`](../proposals/propuesta.md).

---

## 🔗 Flujo técnico consolidado

> Descripción del flujo completo entre tareas: Al ejecutar el programa se despliega un menu que permite al usuario establecer la configuración inicial de la red (IP de la red, OS esperados, servicios a monitorear, límite de dispositivos, número de puertos), esta configuración se utiliza como argumentos para los procesos posteriores. Posteriormente se ejecuta la tarea de Acquisition, obteniendo un json con los datos que cumplan con los requisitos. Este archivo json es empleado como entrada de la siguiente tarea Analysis, encargada de identificar discrepancias en el comportamiento esperado de la red, generando un archivo JSON acciones a implementar por la tarea Response. Al momento de finalizar el análisis se invocara la IA, que genera un resumen técnico y hallazgos relevantes, asi como las recomendaciones y posibles acciones que se tomaran para asegurar el equipo que lo ejecute, en dado caso que sea el mismo.

---

## 🧠 IA integrada funcionalmente

- **Modelo/API utilizado**: GPT-4.1
- **Punto de integración**:  Luego del análisis de red, se emplea la IA para generar un reporte de los hallazgos realizados en el escaneo.

- **Ejemplo de entrada/salida**:  
  > Entrada:
  >
{
  "targets": "192.168.100.45",
  "hosts_num": 1,
  "host_families": [
    "Windows"
    ],
    "ports": [
      80,
      22
    ],
  "services": [
      "Apache HTTP server",
      "SSH"
    ]
 }
  
  > Salida:
  > 
    1. Resumen general
    
    Se realizó un análisis de la red sobre un dispositivo basado en Windows (IP: 192.168.100.45). Se detectaron dos puertos abiertos asociados a los servicios Apache HTTP Server (puerto 80) y SSH (puerto 22). A continuación, se detalla el nivel de riesgo y las recomendaciones para cada uno.
    
    2. Lista de dispositivos
    
    - 192.168.100.45 (Windows)
    
    3. Análisis de cada dispositivo
    
    - Nombre e IP: 192.168.100.45 (Windows)
      - Puertos abiertos:
        - Puerto 80 (Apache HTTP server)
          - Riesgo: Alto
            - Explicación: El puerto 80 (HTTP) transmite información sin cifrado, lo que permite que los datos sean interceptados fácilmente. Adicionalmente, servicios HTTP expuestos pueden ser objetivo de vulnerabilidades conocidas en Apache o en aplicaciones web instaladas.
          - Acciones recomendadas:
            - Si no es necesario el acceso externo, cerrar el puerto 80.
            - Si el servicio es imprescindible, migrar a HTTPS (puerto 443) utilizando certificados válidos.
            - Mantener Apache actualizado y eliminar módulos innecesarios.
            - Limitar el acceso mediante filtrado de IPs o segmentación de red.
        - Puerto 22 (SSH)
          - Riesgo: Medio
            - Explicación: Aunque SSH proporciona acceso seguro, mantener este puerto abierto en todas las interfaces puede exponer el sistema a ataques de fuerza bruta, intentos de explotación de vulnerabilidades o accesos no autorizados.
          - Acciones recomendadas:
            - Restringir el acceso SSH únicamente a las IPs autorizadas.
            - Considerar cambiar el puerto estándar por uno personalizado si es posible.
            - Implementar autenticación por clave en vez de contraseñas.
            - Revisar periódicamente los intentos de acceso y los logs del sistema.
    
    4. Conclusión final
    
    El dispositivo 192.168.100.45 expone servicios que pueden representar vectores de ataque si no se gestionan apropiadamente. Se recomienda cerrar o restringir el acceso a los puertos identificados si no son estrictamente necesarios y adoptar medidas de protección adicionales para reducir riesgos de exposición y compromiso del sistema. Mantener actualizados los servicios y aplicar segmentación y filtrado de red contribuirán significativamente a la seguridad de la infraestructura analizada.

---

## 📚 Documentación técnica

> Para la utilización de la API de chat-GPT se requirió tanto de su librería como de la API key que nos permite utilizarla, de forma que, ya teniendo el prompt creado, la api key en el proyecto y el archivo salido del análisis creado, la IA comenzara a analizar el archivo para dar su reporte al respecto de los aspectos que podrían mejorarse o ser mas urgentes.

---

## 🤝 Colaboración

- **Sebastián Alighieri Ramirez:** Creación del menú dinámico para definir configuración del usuario (IP, SO, servicios, límites). Integración del objeto resultante hacia la rama Acquisition.
- **Julio Abraham Puente Guerrero:** Diseño del prompt y script para la utilización de la IA basado en la salida JSON. Extracción de puertos, SO y servicios según filtros del usuario.
- **Alberto Jessier Lucio Sital:** Documentación global del proyecto, redacción de avances técnicos y consolidación del flujo completo entre tareas.

---

## 🧭 Observaciones

Falta por concluir la Depuración final del módulo Response, crear los ejemplos reproducibles y documentación final, ajustar manejo de errores y logs enriquecidos.
