"""Functions and clases to configure paths and pre-logging configurations."""

from pathlib import Path

from pydantic import BaseModel, field_validator, model_validator
from yaml import YAMLError, safe_load


class PathsConfig(BaseModel):
    """Modelo para validar las rutas de configuración."""

    data: Path
    states: Path
    outputs: Path
    logs: Path
    messages: Path
    project_root: Path | None = None

    @classmethod
    def set_project_root(cls, root: Path) -> None:
        """Establece la raíz del proyecto para resolver rutas relativas."""
        cls.project_root = root

    @field_validator("data", "states", "outputs", "logs", "messages", mode="before")
    @classmethod
    def resolve_path(cls, v: str) -> Path:
        if cls.project_root is None:
            msg = "Project root not set. Call PathsConfig.set_project_root() first."
            raise ValueError(msg)

        # Parse strings to paths
        path = Path(v)

        # Si es relativa, la resuelve respecto al project root
        if not path.is_absolute():
            path = cls.project_root / path

        return path.resolve()

    def initialize_directories(self) -> None:
        """Create required directories if missing."""
        for field_name in ["data", "states", "outputs", "logs", "messages"]:
            path = getattr(self, field_name)

            if not path.exists():
                path.mkdir(parents=True, exist_ok=True)
                print(f"Directorio creado: {path}")
            elif not path.is_dir():
                msg = f"'{path}' existe pero no es un directorio"
                raise NotADirectoryError(msg)


class Config(BaseModel):
    """Modelo principal de configuración."""

    paths: PathsConfig

    @model_validator(mode="after")
    def validate_logs_in_outputs(self):
        """Valida que logs esté dentro de outputs."""
        logs = Path(self.paths.logs)
        outputs_path = Path(self.paths.outputs)

        try:
            # Verifica si logs es relativo a outputs
            logs.resolve().relative_to(outputs_path.resolve())
        except ValueError as e:
            msg = f"logs '{self.paths.logs}' isn't in '{self.paths.outputs}'"
            raise ValueError(msg) from e

        return self

    def initialize_paths(self) -> None:
        """Inicializa todos los directorios necesarios."""
        self.paths.initialize_directories()


def load_config(project_root: Path, config_path: Path | None = None) -> Config:
    """Load configuration for network analyzer."""
    if config_path is None:
        config_path = project_root / "config" / "config.yaml"

    PathsConfig.set_project_root(project_root)

    try:
        with config_path.open("r") as f:
            config_dict = safe_load(f)
    except FileNotFoundError:
        print(f"Archivo de configuración no encontrado: {config_path}")
        raise
    except YAMLError as e:
        print(f"Error al parsear YAML: {e}")
        raise

    config = Config(**config_dict)
    config.initialize_paths()
    return config
