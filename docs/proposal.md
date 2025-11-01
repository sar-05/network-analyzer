# Network Analyzer

## Descripción General

Desarrollar una herramienta de análisis de red que detecte anomalías y realize
acciones de contención automatizadas. El proyecto está dividido en tres módulos
cooperativos:

## Módulo A: Inventario y Recolección de Actividad

- Objetivo:
- Obtener una **mapeo completo del entorno de red**: qué dispositivos están
  activos, cómo se comunican y qué servicios ofrecen.

- Entradas:
  - Rango de red (CIDR o lista de IPs) definido por el usuario.
  - Parámetros opcionales (profundidad del escaneo,  puertos de interés, etc.).

- Proceso:
  1. **Descubrimiento de hosts activos**: Identificar direcciones IP que
     responden a ping o a peticiones ARP.
  2. **Enumeración de puertos**: Escanear puertos abiertos en cada host.
  3. **Identificación de servicios**: Determinar servicios y versiones (HTTP,
     SSH, SMB, etc.).
  4. **(Opcional) Detección de sistema operativo**: Inferir tipo de dispositivo
     (router, cámara, servidor…).
  5. **Recolección temporal**: Registrar hora y duración del escaneo, para
     comparar con ejecuciones futuras.

- Salida

- Un **archivo estructurado (JSON)** con campos estructurados.
- Un archivo markdown con un resumen **orientado al usuario**.

## Módulo B: Análisis y Detección de Actividad Sospechosa

- Objetivo:
  - Identificar patrones o cambios que **no corresponden al comportamiento
    esperado de la red**.

- Entradas:
  - Archivo JSON generado por la Módulo A.
  - Plantilla con mapeo esperado de la red.
  - Historial de escaneos previos para comparar comportamiento histórico.

- Proceso:

1. **Comparación con una “línea base”**: Detectar nuevos hosts, puertos
   abiertos adicionales o servicios modificados.
2. **Aplicación de reglas de detección**
   2.1 Aparece un host nuevo en la red → posible dispositivo no autorizado.
   2.2 Se abre un puerto inusual en un host conocido → posible servicio no autorizado.
   2.3 Host realiza conexiones simultáneas a múltiples destinos → posible
       escaneo interno.
3. **Clasificación de riesgo**: Asignar niveles (bajo, medio, alto) en función
   del tipo de evento.
4. **Definición de medidas de contención**: Bloquear IP, aislar host, registrar
   evento, recomendar revisión manual.

- Salida
  - Archivo JSON acciones a implementar por la Módulo C.

## Módulo C: Respuesta y Contención

- Objetivo
  - Ejecutar las medidas determinadas por la Módulo B, de forma **controlada y auditable**.

- Entradas
  - Archivo JSON de alertas y acciones recomendadas.

- Proceso

1. **Interpretación de acciones**: Determinar si se trata de acción automática
   o recomendación manual.

2. **Ejecución de contención**
     2.1 Actualizar reglas del firewall (`ufw`, `iptables`, `netsh`).
     2.2 Deshabilitar interfaces de red específicas.
     2.3 Generar registro en un archivo de auditoría.
3. **Notificación al usuario**: Solicitar confirmación para aplicar acciones
   automatizadas. Mostrar recomendaciones manuales.

- Salida
  - Registro de acciones ejecutadas.
  - Resumen final con estado de la red post-contención.

## Estructura del repositorio

network-analyzer/
├── pyproject.toml                <- Configuración del paquete (build + dependencias)
├── README.md                     <- Descripción general, instalación y uso
├── SECURITY.md                   <- Políticas éticas y controles de seguridad
├── CHANGELOG.md                  <- Registro de cambios y versiones
├── CONTRIBUTORS.md               <- Créditos del equipo y roles
├── LICENSE                       <- Licencia del proyecto
├── /config/                      <- Configuración centralizada
│   └── config.yaml               <- Rutas, parámetros, límites, etc.
│
├── /src/                         <- Código fuente (paquete instalable)
│   └── cybersec_analyzer/        <- Paquete Python principal
│       ├── __init__.py
│       ├── cli.py                <- CLI Python unificado (entrypoint)
│       │
│       ├── acquisition/          <- Tarea A: Inventario y escaneo de red
│       │   ├── __init__.py
│       │   └── acquire.py
│       │
│       ├── analysis/             <- Tarea B: Análisis y detección de anomalías
│       │   ├── __init__.py
│       │   └── analyze.py
│       │
│       ├── response/             <- Tarea C: Contención y respuesta (según OS)
│       │   ├── __init__.py
│       │   └── reply.py          <- Llama y gestiona ejecución de scripts nativos
│       │
│       └── utils/                <- Código común y soporte
│           ├── __init__.py
│           ├── logger.py         <- Configuración de logging estructurado
│           ├── io.py             <- Lectura/escritura de JSON, YAML, etc.
│           └── config.py         <- Carga y validación de configuración
│
├── /scripts/                     <- Scripts nativos de orquestación y respuesta
│   ├── linux/
│   │   └── containment.sh        <- Acciones automatizadas en Linux
│   └── windows/
│       └── containment.ps1       <- Acciones automatizadas en Windows
│
├── /data/                        <- Datos intermedios y resultados procesables
│   ├── net_enum_2025-10-24.json  <- Salida de la Tarea A
│   └── sus_act_2025-10-24.json   <- Salida de la Tarea B
│
├── /outputs/                     <- Reportes finales para el usuario
│   ├── summary.md                <- Resumen humano (enriquecido con IA)
│   └── logs/                     <- Registros de ejecución
│       └── run_2025-10-24.log
│
├── /prompts/                     <- Prompts versionados para la API de IA
│   ├── summary_prompt.txt        <- Prompt para generar resumen
^ │   └── context_template.md       <- Plantilla de contexto o formato del resumen
│
├── /docs/                        <- Documentación
│   ├── proposal.md               <- Descripción técnica de módulos y flujo de datos
│   ├── usage.md                  <- Guía detallada de instalación y ejecución
│   └── schema.md                 <- Estructura esperada y formatos de salida
│
├── /tests/                       <- Pruebas unitarias e integraciones
│   ├── unit/
│   │   ├── test_acquisition.py
│   │   ├── test_analysis.py
│   │   └── test_reply.py
│   │
│   ├── integration/
│   │   └── test_pipeline.py
│   │
│   └── scripts/
│       ├── test_containment.py
│       └── test_containment.ps1
│
└─ .github/
   └── workflows/
       └── tests.yml             <- Pipeline CI/CD

<!-- markdownlint-disable-file MD050 -->
