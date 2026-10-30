"""Parte 3.2: demostración experimental de peor, mejor y caso promedio.

Ejecuta insertion_sort sobre los tres escenarios de Tamiza y grafica las
comparaciones y el tiempo de ejecución frente al tamaño de entrada.
"""

import os
import time

import matplotlib.pyplot as plt

from algoritmos import insertion_sort
from datos import generar_aleatorio, generar_casi_ordenado, generar_inverso

TAMANOS = [100, 200, 400, 800, 1600, 3200, 6400]
REPETICIONES = 5  # el tiempo reportado es el minimo de las repeticiones
SEMILLA = 42

ESCENARIOS = {
    "A - aleatorio": lambda n: generar_aleatorio(n, SEMILLA),
    "B - casi ordenado": lambda n: generar_casi_ordenado(n, SEMILLA),
    "C - orden inverso": lambda n: generar_inverso(n),
}


def esta_descendente(lista: list[int]) -> bool:
    """Verifica que la lista quede de mayor a menor, sin ordenarla.

    Args:
        lista: lista de indices de riesgo a verificar.

    Returns:
        True si cada elemento es mayor o igual que el siguiente.
    """
    return all(lista[i] >= lista[i + 1] for i in range(len(lista) - 1))


def medir(nombre: str, n: int) -> tuple[float, int]:
    """Ejecuta insertion_sort sobre un escenario y mide solo el algoritmo.

    Args:
        nombre: nombre del escenario, una llave de ESCENARIOS.
        n: tamaño del lote de registros.

    Returns:
        Una tupla con el menor tiempo medido, en segundos, y el numero
        de comparaciones entre elementos.
    """
    datos = ESCENARIOS[nombre](n)  # la generacion NO se cronometra
    copia_original = list(datos)

    mejor_tiempo = float("inf")
    comparaciones = 0
    for _ in range(REPETICIONES):
        inicio = time.perf_counter()
        resultado, comparaciones = insertion_sort(datos)
        fin = time.perf_counter()
        mejor_tiempo = min(mejor_tiempo, fin - inicio)

    # Verificaciones de correccion (fuera del cronometro)
    assert datos == copia_original, "se modifico la lista recibida"
    assert esta_descendente(resultado), "la salida no quedo de mayor a menor"
    assert len(resultado) == n and len(set(resultado)) == n, (
        "se perdieron o duplicaron registros")
    return mejor_tiempo, comparaciones


def graficar(series: dict[str, list[float]], ylabel: str, titulo: str,
             archivo: str, referencia: bool = False) -> None:
    """Dibuja los tres escenarios en los mismos ejes, en escala log-log.

    Args:
        series: valores a graficar por escenario, uno por cada tamaño.
        ylabel: rotulo del eje vertical, con sus unidades.
        titulo: titulo de la grafica.
        archivo: ruta de la imagen PNG de salida.
        referencia: si es True, dibuja la recta del mejor caso, n - 1.
    """
    estilos = {"A - aleatorio": "o-", "B - casi ordenado": "s-",
               "C - orden inverso": "^-"}
    plt.figure(figsize=(8, 5.5))
    for nombre, valores in series.items():
        plt.plot(TAMANOS, valores, estilos[nombre], label=nombre)
    if referencia:
        plt.plot(TAMANOS, [n - 1 for n in TAMANOS], "k--", linewidth=1,
                 label="Mejor caso teórico (n - 1)")
    plt.xscale("log", base=2)
    plt.yscale("log")
    plt.xticks(TAMANOS, [str(n) for n in TAMANOS])
    plt.xlabel("Tamaño de entrada n (registros, escala log)")
    plt.ylabel(ylabel)
    plt.title(titulo)
    plt.grid(True, which="both", alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(archivo, dpi=150)
    plt.close()


def main() -> None:
    """Corre el experimento de la Parte 3.2 y genera las dos graficas."""
    os.makedirs("graficas", exist_ok=True)
    tiempos: dict[str, list[float]] = {nombre: [] for nombre in ESCENARIOS}
    comparaciones: dict[str, list[float]] = {n: [] for n in ESCENARIOS}

    print(f"{'escenario':<20}{'n':>7}{'comparaciones':>16}"
          f"{'tiempo (s)':>13}{'comp/n^2':>11}")
    for nombre in ESCENARIOS:
        for n in TAMANOS:
            t, c = medir(nombre, n)
            tiempos[nombre].append(t)
            comparaciones[nombre].append(c)
            print(f"{nombre:<20}{n:>7}{c:>16,}{t:>13.5f}{c / n**2:>11.4f}")

    graficar(comparaciones, "Comparaciones entre elementos (número)",
             "Insertion sort: comparaciones vs. tamaño (escala log-log)",
             "graficas/parte3_comparaciones.png", referencia=True)
    graficar(tiempos, "Tiempo de ejecución (s, escala log)",
             "Insertion sort: tiempo vs. tamaño (escala log-log)",
             "graficas/parte3_tiempo.png")


if __name__ == "__main__":
    main()
