"""Experimento: tiempo de fuerza bruta vs. divide y venceras."""

import random
import time
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  

from subarreglo import subarreglo_fuerza_bruta, subarreglo_maximo

SEMILLA = 2026
TAMANOS = [10, 50, 100, 500, 1000, 2000, 4000, 8000, 16000]
REPETICIONES = {10: 200, 50: 100, 100: 50, 500: 15, 1000: 9,
                2000: 5, 4000: 5, 8000: 3, 16000: 3}
RUTA_GRAFICA = Path(__file__).parent / "graficas" / "tiempo_vs_n.png"
AZUL = "#2a78d6"
NARANJA = "#eb6834"


def generar_datos(n: int, generador: random.Random) -> list[int]:
    """Genera n variaciones enteras entre -100 y 100.

    Args:
        n: cantidad de dias.
        generador: generador pseudoaleatorio con semilla fija.

    Returns:
        Lista de n enteros en [-100, 100].
    """
    return [generador.randint(-100, 100) for _ in range(n)]


def mediana(tiempos: list[float]) -> float:
    """Calcula la mediana de una lista de tiempos.

    Args:
        tiempos: mediciones en segundos.

    Returns:
        La mediana de las mediciones.
    """
    ordenados = sorted(tiempos)
    return ordenados[len(ordenados) // 2]


def medir(n: int, generador: random.Random) -> tuple[float, float]:
    """Mide ambos algoritmos sobre la misma lista de tamano n.

    Args:
        n: tamano de entrada.
        generador: generador pseudoaleatorio con semilla fija.

    Returns:
        Tupla (mediana de fuerza bruta, mediana de divide y venceras),
        en segundos.
    """
    datos = generar_datos(n, generador)  # fuera del cronometro
    t_fb: list[float] = []
    t_dv: list[float] = []
    for _ in range(REPETICIONES[n]):
        t0 = time.perf_counter()
        res_fb = subarreglo_fuerza_bruta(datos)
        t_fb.append(time.perf_counter() - t0)

        t0 = time.perf_counter()
        res_dv = subarreglo_maximo(datos, 0, n - 1)
        t_dv.append(time.perf_counter() - t0)

        assert res_fb[2] == res_dv[2], f"Sumas distintas en n={n}"
    return mediana(t_fb), mediana(t_dv)


def graficar(tamanos: list[int], fb: list[float], dv: list[float]) -> None:
    """Dibuja tiempo vs. tamano en escala lineal y logaritmica.

    Args:
        tamanos: tamanos de entrada medidos.
        fb: tiempos de fuerza bruta en milisegundos.
        dv: tiempos de divide y venceras en milisegundos.
    """
    fig, ejes = plt.subplots(1, 2, figsize=(12, 4.8))
    for eje, log in zip(ejes, (False, True)):
        eje.plot(tamanos, fb, "o-", color=NARANJA, lw=2, ms=6,
                 label="Fuerza bruta, Θ(n²)")
        eje.plot(tamanos, dv, "s-", color=AZUL, lw=2, ms=6,
                 label="Divide y vencerás, Θ(n log n)")
        eje.set_xlabel("Tamaño de entrada n (días)")
        eje.set_ylabel("Tiempo de ejecución (ms)")
        eje.grid(alpha=0.25)
        eje.legend()
        if log:
            eje.set_xscale("log")
            eje.set_yscale("log")
            eje.set_title("Escala log-log")
        else:
            eje.set_title("Escala lineal")
    fig.suptitle(
        "Subarreglo máximo: tiempo de ejecución vs. tamaño de entrada"
    )
    fig.tight_layout()
    RUTA_GRAFICA.parent.mkdir(exist_ok=True)
    fig.savefig(RUTA_GRAFICA, dpi=150)


def main() -> None:
    """Ejecuta el experimento, imprime la tabla y guarda la grafica."""
    generador = random.Random(SEMILLA)
    fb_ms: list[float] = []
    dv_ms: list[float] = []
    print(f"{'n':>7} {'fuerza bruta (ms)':>18} {'div. y venc. (ms)':>18}")
    for n in TAMANOS:
        t_fb, t_dv = medir(n, generador)
        fb_ms.append(t_fb * 1000)
        dv_ms.append(t_dv * 1000)
        print(f"{n:>7} {fb_ms[-1]:>18.4f} {dv_ms[-1]:>18.4f}")
    graficar(TAMANOS, fb_ms, dv_ms)
    print(f"Grafica guardada en {RUTA_GRAFICA}")


if __name__ == "__main__":
    main()
