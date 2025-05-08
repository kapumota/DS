"""Utilidades genéricas."""

import logging
logger = logging.getLogger("devops_testing")

def log_info(message: str) -> None:
    logger.info(message)
