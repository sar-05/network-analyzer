# Network Analyzer

## Herramienta de análisis de red para detección de anomalías y ejecución de acciones de contención automatizada.


Este repositorio contiene el desarrollo de un sistema modular de ciberseguridad dividido en **tres herramientas cooperativas**, cuyo objetivo es **mapear una red**, **detectar actividad sospechosa en los puertos** y **ejecutar acciones de contención de forma controlada** dentro de un sistema operativo Linux.  
El proyecto incluye un **menú interactivo**, un **flujo técnico documentado** y una **integración de IA** para generar reportes explicativos, resúmenes inteligentes y sugerencias de contención.
---

## 📌 Objetivo General  
El propósito principal del proyecto es analizar el entorno de red, generar una radiografía completa del estado actual, detectar comportamientos fuera de lo esperado y permitir acciones automatizadas de seguridad.

El sistema está compuesto por tres módulos interoperables:
Módulo A — Acquisition: inventario y recolección de actividad.
Módulo B — Analysis: análisis de anomalías usando comparación histórica.
Módulo C — Response: ejecución de contención en puertos o servicios sospechosos.

El diseño final ofrece:
Un flujo técnico completo de detección → análisis → respuesta.
Integración con IA para análisis contextual y decisiones asistidas.
Ejecución segura y controlada de acciones en el firewall del sistema.

---

# 👥 Integrantes y Roles

| Integrante                        | Rol y Contribuciones                                                                                                                                                                   |
| --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Sebastián Alighieri Ramírez**   | Creación del menú dinámico, configuración de parámetros (IP, SO, servicios, límites). Implementación del módulo A (Acquisition). Ajuste del flujo técnico.                           |
| **Julio Abraham Puente Guerrero** | Diseño del prompt y script para la IA. Extracción de puertos, sistemas operativos y servicios según filtros. Documentación del plan de IA.                                             |
| **Alberto Jessier Lucio Sital**   | Documentación global del proyecto y redacción técnica. Integración completa del flujo entre módulos. Implementación del módulo C (Response) con acciones reales en puertos y firewall. |

---

# 🧩 Estado Final del Proyecto

### ✔ Módulo A — Acquisition

* Menú interactivo funcional.
* Escaneo según parámetros definidos por el usuario.
* Identificación de puertos, servicios y sistema operativo.
* Exportación a JSON estructurado.

### ✔ Módulo B — Analysis

* Comparación entre escaneos actuales y anteriores.
* Identificación de anomalías: nuevos hosts, puertos inesperados, cambios en servicios.
* Generación de recomendaciones y análisis contextual mediante IA.

### ✔ Módulo C — Response

* Interpretación de acciones recomendadas.
* Aplicación real del firewall (creación y modificación de cadenas).
* Ejecución de bloqueos, aperturas o modificaciones en puertos.
* Registro final de acciones ejecutadas.

### ## 🤖 Integración de Inteligencia Artificial

### Propósito del uso de IA
La IA se utiliza para:

- Generar reportes explicativos de hallazgos  
- Identificar vulnerabilidades relevantes  
- Informar al usuario sobre acciones tomadas y recomendaciones futuras  

### Punto de integración en el flujo
- Después del análisis (Módulo B)  
- Después de la respuesta (Módulo C)

### Modelo seleccionado
- **GPT-4.1**

### Archivos relacionados
- `/docs/ai_plan.md`
- `/prompts/prompt_v1.json`

### Estado general

* **Proyecto completado (100%)**

---

# 🛡️ Declaración Ética y Consideraciones de Seguridad

### Controles implementados

* Uso exclusivo en **redes autorizadas**.
* Recolección de información **solo técnica** (no personal).
* Auditoría completa de todas las acciones ejecutadas.
* Ejecución controlada de modificaciones al firewall.

### Advertencias de uso

Este software **solo debe utilizarse en**:

* Sistemas propios o con autorización explícita.
* Ambientes de prueba, auditoría y prácticas de ciberseguridad.
* Escenarios educativos o profesionales con fines legítimos.

El uso indebido del software **es responsabilidad de quien lo ejecuta**.

---

# 🔗 Enlaces Internos a Entregables

* 📄 **Entregable 3 — Implementación de análisis y base para IA**
  → `/docs/entregable_3.md`

* 📄 **Entregable 4 — Proyecto casi completo (90%)**
  → `/docs/entregable_4.md`

* 🤖 **Plan de IA**
  → `/docs/ai_plan.md`

---

# 🛠️ Instalación y Ejecución

### Requisitos

* Python **3.13+**
* Permisos de administrador (para escaneo y firewall)
* Acceso a red autorizado

### Instalación rápida

```bash
git clone https://github.com/sar-05/network-analyzer
cd network-analyzer
pip install -e .
```

---

# 📅 Información Final

**Última actualización:** 26 Noviembre 2025
**Estado del proyecto:** ✔ Proyecto Completado
