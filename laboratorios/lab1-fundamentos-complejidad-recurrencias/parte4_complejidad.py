"""Parte 4.2: validación experimental de insertion sort vs. merge sort.

Mide el tiempo de los dos algoritmos sobre el escenario A, genera la
grafica comparativa y calcula los datos de apoyo del concepto tecnico.
"""

import math
import os
import time
import tracemalloc
from typing import Callable

import matplotlib.pyplot as plt

from algoritmos import insertion_sort, merge_sort
from datos import generar_aleatorio, generar_casi_ordenado, generar_inverso
from parte3_casos import REPETICIONES, SEMILLA, TAMANOS, esta_descendente

Algoritmo = Callable[[list[int]], tuple[list[int], int]]

N_TAMIZA = 1_200_000  # registros reales de Tamiza
VENTANA_S = 4 * 3600  # ventana de cuatro horas, en segundos


def medir(algoritmo: Algoritmo, datos: list[int]) -> tuple[float, int]:
    """Mide un algoritmo; solo cronometra la llamada, no la generacion.

    Args:
        algoritmo: funcion de ordenamiento que devuelve (lista, comparaciones).
        datos: lote de registros a ordenar.

    Returns:
        Una tupla con el menor tiempo de las repeticiones, en segundos, y
        el numero de comparaciones entre elementos.
    """
    copia = list(datos)
    mejor = float("inf")
    comparaciones = 0
    for _ in range(REPETICIONES):
        inicio = time.perf_counter()
        resultado, comparaciones = algoritmo(datos)
        fin = time.perf_counter()
        mejor = min(mejor, fin - inicio)
    assert datos == copia, "el algoritmo modifico la lista recibida"
    assert esta_descendente(resultado) and len(resultado) == len(datos)
    assert len(set(resultado)) == len(datos), "registros perdidos o repetidos"
    return mejor, comparaciones


def memoria_pico(algoritmo: Algoritmo, datos: list[int]) -> int:
    """Mide el pico de memoria reservada durante una llamada.

    Se mide aparte del tiempo, porque tracemalloc hace mas lento el codigo.

    Args:
        algoritmo: funcion de ordenamiento que devuelve (lista, comparaciones).
        datos: lote de registros a ordenar.

    Returns:
        El pico de memoria reservada, en bytes.
    """
    tracemalloc.start()
    algoritmo(datos)
    _, pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return pico


def graficar_tiempos(tiempos: dict[str, list[float]], archivo: str) -> None:
    """Dibuja el tiempo de ambos algoritmos en los mismos ejes (log-log).

    Args:
        tiempos: tiempo en segundos por algoritmo, uno por cada tamaño.
        archivo: ruta de la imagen PNG de salida.
    """
    plt.figure(figsize=(8, 5.5))
    plt.plot(TAMANOS, tiempos["Insertion sort"], "o-", label="Insertion sort")
    plt.plot(TAMANOS, tiempos["Merge sort"], "s-", label="Merge sort")
    plt.xscale("log", base=2)
    plt.yscale("log")
    plt.xticks(TAMANOS, [str(n) for n in TAMANOS])
    plt.xlabel("Tamaño de entrada n (registros, escala log)")
    plt.ylabel("Tiempo de ejecución (segundos, escala log)")
    plt.title("Escenario A (aleatorio): insertion sort vs. merge sort")
    plt.grid(True, which="both", alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(archivo, dpi=150)
    plt.close()


def main() -> None:
    """Corre el experimento de la Parte 4.2 e imprime los datos de apoyo."""
    os.makedirs("graficas", exist_ok=True)
    algoritmos = {"Insertion sort": insertion_sort, "Merge sort": merge_sort}

    # --- Escenario A: mismos tamanos que la Parte 3 ---
    tiempos: dict[str, list[float]] = {nombre: [] for nombre in algoritmos}
    print("ESCENARIO A (aleatorio)")
    print(f"{'n':>7}{'insertion (s)':>15}{'merge (s)':>12}"
          f"{'comp. ins.':>14}{'comp. merge':>13}")
    for n in TAMANOS:
        datos = generar_aleatorio(n, SEMILLA)  # la generacion no se mide
        t_ins, c_ins = medir(insertion_sort, datos)
        t_mer, c_mer = medir(merge_sort, datos)
        tiempos["Insertion sort"].append(t_ins)
        tiempos["Merge sort"].append(t_mer)
        print(f"{n:>7}{t_ins:>15.5f}{t_mer:>12.5f}{c_ins:>14,}{c_mer:>13,}")
    graficar_tiempos(tiempos, "graficas/parte4_tiempo.png")

    # --- Datos de apoyo para el concepto tecnico (mayor n medido) ---
    n = TAMANOS[-1]
    generadores = {
        "A": generar_aleatorio(n, SEMILLA),
        "B": generar_casi_ordenado(n, SEMILLA),
        "C": generar_inverso(n),
    }
    # El escenario A reutiliza las mediciones de la grafica.
    medidas = {(nombre, "A"): tiempos[nombre][-1] for nombre in algoritmos}
    print(f"\nESCENARIOS B Y C, n = {n}")
    for esc in "BC":
        for nombre, alg in algoritmos.items():
            t, c = medir(alg, generadores[esc])
            medidas[(nombre, esc)] = t
            print(f"  {esc}  {nombre:<15}{t:>9.5f} s{c:>13,} comparaciones")

    print(f"\nMEMORIA (pico reservado durante la llamada, n = {n})")
    for nombre, alg in algoritmos.items():
        pico = memoria_pico(alg, generadores["A"])
        print(f"  {nombre:<15}{pico / 1024:>9.1f} KiB")

    # --- Extrapolacion a N_TAMIZA (estimacion, no medicion) ---
    # insertion: tiempo ~ k * n^2          -> k = t / n^2
    # merge:     tiempo ~ k * n * log2(n)  -> k = t / (n * log2(n))
    print(f"\nEXTRAPOLACION a n = {N_TAMIZA:,} "
          f"(estimacion; ventana = {VENTANA_S:,} s)")
    n_log = N_TAMIZA * math.log2(N_TAMIZA)
    for esc in "ABC":
        k = medidas[("Insertion sort", esc)] / n**2
        est = k * N_TAMIZA**2
        print(f"  Insertion sort, {esc}: k = {k:.3e} s -> "
              f"{est:,.0f} s = {est / 3600:.2f} h")
    for esc in "ABC":
        k = medidas[("Merge sort", esc)] / (n * math.log2(n))
        est = k * n_log
        print(f"  Merge sort,     {esc}: k = {k:.3e} s -> "
              f"{est:,.1f} s = {est / 60:.2f} min")


if __name__ == "__main__":
    main()
