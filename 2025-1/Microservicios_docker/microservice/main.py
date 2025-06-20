from fastapi import FastAPI
import uvicorn

from microservice.api.routes import router as api_router
from microservice.services.database import init_db
from microservice.utils.logger import logger


def get_application() -> FastAPI:
    """
    Crea y configura la instancia de FastAPI con sus rutas
    y eventos de ciclo de vida.
    """
    app = FastAPI(
        title="Microservicio bootstrap ",
        description="Microservicio de ejemplo con FastAPI y Docker.",
        version="0.1.0",
        docs_url="/",      # Documentación Swagger en la ruta raíz
        redoc_url=None,    # Deshabilita ReDoc
    )

    # Incluir las rutas definidas en el router de la API
    app.include_router(api_router)

    @app.on_event("startup")
    def on_startup() -> None:
        """
        Se ejecuta cuando la aplicación arranca.
        Inicializa la base de datos y escribe en el log.
        """
        logger.info("Arrancando la aplicación")
        init_db()

    @app.on_event("shutdown")
    def on_shutdown() -> None:
        """
        Se ejecuta justo antes de que la aplicación se detenga.
        Registra el evento de cierre en el log.
        """
        logger.info("Deteniendo la aplicación")

    return app


# Instancia global de la aplicación
app = get_application()


if __name__ == "__main__":
    # Permite ejecutar con `python -m microservice.main`
    uvicorn.run(
        "microservice.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Recarga automática en desarrollo
    )
