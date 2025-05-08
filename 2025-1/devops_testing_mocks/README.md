### DevOps Testing - Stubs & Mocks y configuraciones avanzadas

Proyecto simple que ejemplifica los conceptos de *stub*, *mock*, `side_effect`, `autospec`, `parametrize`, `skip`, `xfail` y estrategias de *patching* local y holístico dentro de un pipeline DevOps.

* **Lenguaje:** Python 3.12  
* **Gestor de dependencias:** ninguno (sólo `pytest`)  
* **Estructura:**  
  * `devops_testing/` - código de producción  
  * `tests/` - suite de pruebas  
  * `docs/` - apuntes teóricos rápidos  

> **Nota:** Se evita intencionadamente cualquier configuración de CI (p. ej. `.github/`) para que puedas integrar el pipe  que prefieras sin contenido prefabricado.


> Instalación adicional : **pip install -U pytest hypothesis pytest-benchmark pytest-cov**
