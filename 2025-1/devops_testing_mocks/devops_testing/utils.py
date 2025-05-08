"""Utilidades genéricas"""
import time, functools, logging

def retry(times: int = 3, delay: float = 0.1):
    """Decorador simple de reintento"""
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for _ in range(times):
                try:
                    return fn(*args, **kwargs)
                except Exception as exc:
                    last_exc = exc
                    time.sleep(delay)
            raise last_exc
        return wrapper
    return decorator

logger = logging.getLogger("devops_testing")

