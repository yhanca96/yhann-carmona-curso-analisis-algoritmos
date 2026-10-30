"""Generadores de lotes de registros para los escenarios de Tamiza."""

import random


def generar_aleatorio(n: int, semilla: int = 42) -> list[int]:
    """Genera un lote de n registros en orden aleatorio (escenario A).

    Args:
        n: cantidad de registros del lote.
        semilla: semilla del generador aleatorio, para que el
            experimento sea reproducible.

    Returns:
        Lista de n indices de riesgo enteros distintos, desordenada.
    """
    rng = random.Random(semilla)
    lote = list(range(n))
    rng.shuffle(lote)
    return lote


def generar_casi_ordenado(n: int, semilla: int = 42) -> list[int]:
    """Genera un lote casi ordenado: 98% ordenado y 2% al final (escenario B).

    Args:
        n: cantidad de registros del lote.
        semilla: semilla del generador aleatorio.

    Returns:
        Lista de n indices de riesgo enteros distintos, con el primer
        98% en el orden que el algoritmo produce y el 2% restante
        desordenado al final.
    """
    rng = random.Random(semilla)
    cantidad_nuevos = max(1, round(n * 0.02))
    # Resultados "nuevos del dia", que se anexan al final sin ordenar.
    nuevos = rng.sample(range(n), cantidad_nuevos)
    es_nuevo = set(nuevos)
    # La lista de ayer ya esta en el orden que produce el algoritmo
    # se arma recorriendo los valores de mayor a menor.
    ayer = [v for v in range(n - 1, -1, -1) if v not in es_nuevo]
    rng.shuffle(nuevos)
    return ayer + nuevos


def generar_inverso(n: int) -> list[int]:
    """Genera un lote en el orden exactamente contrario (escenario C).

    Args:
        n: cantidad de registros del lote.

    Returns:
        Lista de n indices de riesgo enteros distintos, en el orden
        inverso al que el algoritmo debe producir.
    """
    # El algoritmo produce descendente asi que la entrada es ascendente.
    return list(range(n))
