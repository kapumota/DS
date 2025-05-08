"""
Benchmark: compara overhead del decorador retry frente a una
implementación manual.  Falla si el wrapper es > 3× más lento.
"""

import timeit
from itertools import count
import pytest
from devops_testing.utils import retry

FAIL_BEFORE_OK = 2          # numero fallos antes de éxito
REPEAT = 500                # repeticiones para timeit (rapidez ≈ 0.1 s)

# helpers deterministas 
def mk_unstable():
    _attempt = count()
    def unstable():
        if next(_attempt) < FAIL_BEFORE_OK:
            raise RuntimeError("boom")
        return "OK"
    return unstable


def make_baseline(unstable):
    def baseline():
        for _ in range(FAIL_BEFORE_OK + 1):
            try:
                return unstable()
            except RuntimeError:
                continue
        raise AssertionError("Deberia no alcanzar")
    return baseline


def make_wrapped(unstable):
    @retry(times=FAIL_BEFORE_OK + 1, delay=0)
    def wrapped():
        return unstable()
    return wrapped


#  benchmark 
@pytest.mark.benchmark
def test_retry_benchmark(benchmark):
    # Instancias "limpias" para esta medición
    unstable = mk_unstable()
    baseline = make_baseline(unstable)
    wrapped = make_wrapped(unstable)

    # 1. Medir ambos con timeit.repeat (ns -> s)
    baseline_t = min(timeit.repeat(baseline, number=1, repeat=REPEAT))
    wrapped_t  = min(timeit.repeat(wrapped,  number=1, repeat=REPEAT))

    # 2. Registrar el wrapper en el reporte de pytest-benchmark
    benchmark(wrapped)            # se ignora el resultado devuelto ("OK")

    # 3. Aserto de rendimiento (≤ 3×)
    assert wrapped_t <= baseline_t * 3, \
        f"Overhead {wrapped_t / baseline_t:.2f}× > 3×"
