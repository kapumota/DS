import logging
import sys


def _configurar_logger() -> logging.Logger:
    """
    Configura y retorna un logger con nombre 'microservice'.
    - Nivel INFO por defecto.
    - Salida a stdout.
    - Formato: timestamp - nivel - logger - mensaje.
    """
    logger = logging.getLogger("microservice")

    # Si aún no tiene handlers, configuramos uno nuevo
    if not logger.handlers:
        logger.setLevel(logging.INFO)

        # Handler para enviar logs a la salida estándar
        handler = logging.StreamHandler(sys.stdout)

        # Formato de los mensajes de log
        formato = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
        formatter = logging.Formatter(formato)
        handler.setFormatter(formatter)

        logger.addHandler(handler)

    return logger


# Instancia global del logger para toda la aplicación
logger = _configurar_logger()
