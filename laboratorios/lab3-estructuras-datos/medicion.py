"""Experimentos A y B: lista enlazada frente a tabla hash."""

import os
import random
import statistics
import time

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from estructuras import ListaEnlazada, TablaHash  # noqa: E402

SEMILLA = 2026
BUSQUEDAS = 200
REPETICIONES = 15
ESTADOS = ("en bodega", "en reparto", "entregado")
CARPETA = os.path.dirname(os.path.abspath(__file__))
GRAFICAS = os.path.join(CARPETA, "graficas")


def generar_guias_inexistentes(
    existentes: set[int], cantidad: int, semilla: int = 7
) -> list[int]:
    """Genera guias de diez digitos que no estan en la coleccion.

    Args:
        existentes: guias almacenadas en las estructuras.
        cantidad: cuantas guias inexistentes generar.
        semilla: semilla del generador, para reproducir la medicion.

    Returns:
        Una lista con `cantidad` guias que no pertenecen a `existentes`.
    """
    azar = random.Random(semilla)
    inexistentes: list[int] = []
    while len(inexistentes) < cantidad:
        guia = azar.randint(10**9, 10**10 - 1)
        if guia not in existentes:
            inexistentes.append(guia)
    return inexistentes


def es_primo(numero: int) -> bool:
    """Indica si un entero es primo.

    Args:
        numero: entero a evaluar.

    Returns:
        True si el numero es primo.
    """
    if numero < 2:
        return False
    divisor = 2
    while divisor * divisor <= numero:
        if numero % divisor == 0:
            return False
        divisor += 1
    return True


def primo_cercano(objetivo: int) -> int:
    """Busca el primo mas cercano a un entero (el menor en caso de empate).

    Args:
        objetivo: entero de referencia.

    Returns:
        El primo mas proximo a `objetivo`.
    """
    distancia = 0
    while True:
        for candidato in (objetivo - distancia, objetivo + distancia):
            if es_primo(candidato):
                return candidato
        distancia += 1


def generar_guias(n: int, semilla: int = SEMILLA) -> list[int]:
    """Genera n guias distintas de diez digitos con semilla fija.

    Args:
        n: cantidad de guias.
        semilla: semilla del generador.

    Returns:
        Lista de n enteros distintos entre 10**9 y 10**10 - 1.
    """
    azar = random.Random(semilla)
    return azar.sample(range(10**9, 10**10), n)


def construir(
    guias: list[int], m: int
) -> tuple[ListaEnlazada, TablaHash]:
    """Construye lista y tabla con las mismas guias y estados.

    Args:
        guias: guias a almacenar.
        m: numero de casillas de la tabla.

    Returns:
        La lista enlazada y la tabla hash ya pobladas.
    """
    azar = random.Random(SEMILLA + 1)
    lista = ListaEnlazada()
    tabla = TablaHash(m)
    for guia in guias:
        estado = azar.choice(ESTADOS)
        lista.insertar(guia, estado)
        tabla.insertar(guia, estado)
    return lista, tabla


def verificar(lista: ListaEnlazada, tabla: TablaHash, guias: list[int]) -> None:
    """Comprueba que lista y tabla devuelven lo mismo en una muestra.

    Args:
        lista: lista enlazada poblada.
        tabla: tabla hash poblada.
        guias: guias almacenadas, de las que se toma la muestra.
    """
    azar = random.Random(SEMILLA + 2)
    muestra = azar.sample(guias, min(200, len(guias)))
    for guia in muestra:
        estado = lista.buscar(guia)
        assert estado is not None and estado == tabla.buscar(guia)


def medir(estructura: ListaEnlazada | TablaHash, consultas: list[int]) -> float:
    """Mide el tiempo medio de buscar guias inexistentes.

    Solo se cronometran las busquedas. Se repite el bloque y se devuelve
    la mediana de los tiempos medios por busqueda.

    Args:
        estructura: lista o tabla donde se busca.
        consultas: guias inexistentes a buscar.

    Returns:
        Tiempo medio por busqueda, en microsegundos.
    """
    medias: list[float] = []
    for _ in range(REPETICIONES):
        inicio = time.perf_counter()
        for guia in consultas:
            resultado = estructura.buscar(guia)
        fin = time.perf_counter()
        assert resultado is None
        medias.append((fin - inicio) / len(consultas) * 1e6)
    return statistics.median(medias)


def experimento_a() -> list[tuple[int, int, float, float, float]]:
    """Ejecuta el experimento A y grafica lista_vs_tabla.png.

    Returns:
        Filas (n, m, alfa, t_lista_us, t_tabla_us).
    """
    filas = []
    for n in (100, 500, 1000, 5000, 20000, 50000, 100000):
        m = primo_cercano(n // 2)
        guias = generar_guias(n)
        lista, tabla = construir(guias, m)
        verificar(lista, tabla, guias)
        consultas = generar_guias_inexistentes(set(guias), BUSQUEDAS)
        t_lista = medir(lista, consultas)
        t_tabla = medir(tabla, consultas)
        filas.append((n, m, tabla.factor_carga(), t_lista, t_tabla))
        print(f"n={n:>6} m={m:>6} alfa={tabla.factor_carga():.2f} "
              f"lista={t_lista:10.2f} us tabla={t_tabla:7.2f} us")
    ns = [f[0] for f in filas]
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(ns, [f[3] for f in filas], "o-", label="Lista enlazada")
    ax.plot(ns, [f[4] for f in filas], "s-", label="Tabla hash (α ≈ 2)")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Número de guías n (unidades, escala log)")
    ax.set_ylabel("Tiempo medio por búsqueda (µs, escala log)")
    ax.set_title("Búsqueda de guías inexistentes: lista frente a tabla hash")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(GRAFICAS, "lista_vs_tabla.png"), dpi=150)
    plt.close(fig)
    return filas


def experimento_b() -> list[tuple[int, float, float]]:
    """Ejecuta el experimento B y grafica tiempo_vs_alfa.png.

    Returns:
        Filas (m, alfa, t_tabla_us).
    """
    n = 20000
    guias = generar_guias(n)
    consultas = generar_guias_inexistentes(set(guias), BUSQUEDAS)
    filas = []
    for alfa_objetivo in (0.25, 0.5, 1, 2, 4, 6, 8, 10):
        m = primo_cercano(round(n / alfa_objetivo))
        lista, tabla = construir(guias, m)
        verificar(lista, tabla, guias)
        t_tabla = medir(tabla, consultas)
        filas.append((m, tabla.factor_carga(), t_tabla))
        print(f"m={m:>6} alfa={tabla.factor_carga():5.2f} tabla={t_tabla:7.2f} us")
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot([f[1] for f in filas], [f[2] for f in filas], "s-",
            label="Tabla hash (n = 20.000)")
    ax.set_xlabel("Factor de carga α = n / m (adimensional)")
    ax.set_ylabel("Tiempo medio por búsqueda (µs)")
    ax.set_title("Efecto del factor de carga en la búsqueda inexistente")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(GRAFICAS, "tiempo_vs_alfa.png"), dpi=150)
    plt.close(fig)
    return filas


if __name__ == "__main__":
    os.makedirs(GRAFICAS, exist_ok=True)
    print("== Experimento A ==")
    experimento_a()
    print("== Experimento B ==")
    experimento_b()
