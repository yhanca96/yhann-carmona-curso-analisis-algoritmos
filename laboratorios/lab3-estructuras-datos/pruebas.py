"""Pruebas con assert para ListaEnlazada y TablaHash."""

import random

from estructuras import ListaEnlazada, TablaHash

ESTADOS = ("en bodega", "en reparto", "entregado")


def prueba_busquedas_basicas() -> None:
    """Busqueda exitosa e infructuosa en lista y tabla."""
    lista = ListaEnlazada()
    tabla = TablaHash(7)
    assert lista.buscar(5) is None  # lista vacia
    assert tabla.buscar(5) is None  # tabla vacia
    datos = ((1000000010, "en bodega"), (1000000024, "en reparto"),
             (1000000017, "en bodega"), (1000000005, "entregado"))
    for guia, estado in datos:
        lista.insertar(guia, estado)
        tabla.insertar(guia, estado)
    for guia, estado in datos:
        assert lista.buscar(guia) == estado
        assert tabla.buscar(guia) == estado
    assert lista.buscar(999) is None
    assert tabla.buscar(999) is None
    assert lista.tamano == 4 and tabla.tamano == 4
    # insercion al inicio: la ultima insertada es la cabeza
    assert lista.cabeza is not None and lista.cabeza.guia == 1000000005


def prueba_colision_forzada() -> None:
    """Con m = 7, las guias 10, 24 y 17 caen en la casilla 3."""
    tabla = TablaHash(7)
    estados = {10: "en bodega", 24: "en reparto", 17: "entregado"}
    for guia, estado in estados.items():
        assert tabla.hash(guia) == 3
        tabla.insertar(guia, estado)
    for guia, estado in estados.items():
        assert tabla.buscar(guia) == estado
    assert tabla.buscar(31) is None  # tambien cae en 3, pero no existe
    assert tabla.casillas[3].tamano == 3
    assert sum(c.tamano for c in tabla.casillas) == 3
    assert tabla.factor_carga() == 3 / 7


def prueba_colecciones_aleatorias() -> None:
    """Lista y tabla coinciden en 30 colecciones aleatorias."""
    azar = random.Random(2026)
    for _ in range(30):
        n = azar.randint(0, 300)
        m = azar.choice((1, 2, 7, 11, 101, 257))
        guias = azar.sample(range(10**9, 10**10), n)
        lista = ListaEnlazada()
        tabla = TablaHash(m)
        estados = {}
        for guia in guias:
            estado = azar.choice(ESTADOS)
            estados[guia] = estado
            lista.insertar(guia, estado)
            tabla.insertar(guia, estado)
        assert tabla.factor_carga() == n / m
        for guia in guias:  # existentes
            assert lista.buscar(guia) == tabla.buscar(guia) == estados[guia]
        conjunto = set(guias)
        for _ in range(100):  # inexistentes
            guia = azar.randint(10**9, 10**10 - 1)
            if guia in conjunto:
                continue
            assert lista.buscar(guia) is None
            assert tabla.buscar(guia) is None


if __name__ == "__main__":
    prueba_busquedas_basicas()
    prueba_colision_forzada()
    prueba_colecciones_aleatorias()
    print("Todas las pruebas pasaron.")
