# Network Analyzer

## Herramienta de análisis de red para detección de anomalías y ejecución de acciones de contención automatizada.


Este repositorio contiene el desarrollo de un sistema modular de ciberseguridad dividido en **tres herramientas cooperativas**, cuyo objetivo es **mapear una red**, **detectar actividad sospechosa** y **ejecutar acciones de contención de forma controlada y auditable**.  
Actualmente el proyecto se encuentra **a la mitad de su implementación**, con integración parcial de los módulos A y B.

---

## 📌 Objetivo General  
Diseñar e implementar un analizador de red que permita:  
1. Realizar inventarios y escaneos estructurados del entorno.  
2. Detectar anomalías, cambios inesperados o comportamientos no autorizados.  
3. Ejecutar acciones de contención sobre dispositivos o servicios comprometidos.

La arquitectura del proyecto se basa en **módulos independientes pero interoperables**, estructurados para operar como una cadena de seguridad preventiva y reactiva.

---

## 🧩 Módulos del Proyecto

### 🔍 Módulo A — Inventario y Recolección de Actividad (Acquisition)

Responsable de obtener un **mapeo completo del entorno de red**, incluyendo:

- Descubrimiento de hosts activos (ping/ARP).  
- Escaneo de puertos.  
- Identificación de servicios y versiones.  
- Detección opcional del sistema operativo.  
- Registro temporal para comparación histórica.

#### **Estado actual**
- ✔ Menú interactivo implementado  
- ✔ Configuración personalizable (rango, puertos, SO, servicios, número de dispositivos)  
- ✔ Generación de archivo JSON estructurado  
- ✔ Preparado para integrarse al módulo B

---

### 🧠 Módulo B — Análisis y Detección de Actividad Sospechosa (Analysis)

Identifica **diferencias significativas** entre el escaneo actual y la línea base esperada:

- Comparación con escaneos previos.  
- Identificación de nuevos hosts, puertos inusuales o servicios modificados.  
- Clasificación de riesgo (bajo/medio/alto).  
- Generación de acciones recomendadas para el módulo C.

#### **Estado actual**
- ✔ Integración parcial con datos del módulo A  
- ✔ Procesamiento de puertos, SO y servicios según filtros del usuario  
- ✔ Generación del JSON base para el módulo C  
- ✔ Primera versión del prompt de IA completada

---

### 🛡️ Módulo C — Respuesta y Contención (Response)

> *En planeación — por implementarse en la segunda mitad del proyecto.*

Su función será:

- Interpretar acciones del módulo B.  
- Ejecutar o recomendar contención automática.  
- Modificar reglas de firewall (`iptables`, `ufw`, `netsh`).  
- Deshabilitar interfaces o generar registros.  

#### **Estado actual**
- ⏳ Aún no implementado  
- 🔧 Scripts base en `/scripts/` para Linux y Windows

---

## 🤖 Integración de Inteligencia Artificial

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
- `/prompts/summary_prompt.txt`
- `/prompts/context_template.md`

---

## 🛠️ Instalación y Uso

### Requisitos del Sistema
- Python 3.8+
- Permisos de administrador para escaneo de red
- Acceso a entorno de red autorizado

### Instalación Rápida
```bash
git clone https://github.com/sar-05/network-analyzer
cd network-analyzer
pip install -e .
```

---

## ⚠️ Consideraciones Éticas y de Seguridad

### Controles Implementados
- ✅ Escaneo exclusivo en redes autorizadas
- ✅ Recolección limitada a información técnica
- ✅ Exclusión de contenido personal o sensible
- ✅ Auditoría completa de acciones ejecutadas

### Advertencias de Uso
Este software debe utilizarse únicamente en:
- Entornos de red propios o con autorización explícita
- Propósitos legítimos de seguridad y administración
- Ambientes controlados y de prueba

---

## 🔄 Próximos Pasos

1. **Integración completa del Módulo B** - Análisis de anomalías
2. **Desarrollo del Módulo C** - Sistema de respuesta automatizada  
3. **Implementación de IA** para generación de reportes
4. **Pruebas de integración** en entornos controlados
5. **Documentación avanzada** y casos de uso

---

*Última actualización: 20 Noviembre 2025*  
*Estado del proyecto: Desarrollo activo - Fase de integración*
