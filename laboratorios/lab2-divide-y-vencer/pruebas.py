import random

from subarreglo import subarreglo_fuerza_bruta, subarreglo_maximo, suma_cruzada


def ambas(serie):
    copia = list(serie)
    fb = subarreglo_fuerza_bruta(serie)
    dv = subarreglo_maximo(serie, 0, len(serie) - 1)
    assert serie == copia, "una funcion modifico la lista"
    # El tramo devuelto debe sumar realmente lo que dice.
    for i, j, s in (fb, dv):
        assert sum(serie[i:j + 1]) == s
    return fb, dv


# Serie de la situacion problema.
fb, dv = ambas([-3, 5, -2, 8, -6, 3, 9, -4])
assert fb[2] == 17 and dv[2] == 17
assert fb[:2] == (1, 6) and dv[:2] == (1, 6)

# Un solo elemento (positivo y negativo).
for x in (7, -7, 0):
    fb, dv = ambas([x])
    assert fb == dv == (0, 0, x)

# Todos negativos: la mejor racha es el menor sacrificio (un solo dia).
fb, dv = ambas([-8, -3, -5, -1, -9])
assert fb[2] == -1 and dv[2] == -1

# Todos positivos: la mejor racha es toda la serie.
fb, dv = ambas([4, 1, 7, 2, 9, 3])
assert fb == dv == (0, 5, 26)

# El mejor tramo cruza el punto medio (medio = 3).
serie = [-10, 1, 2, 5, 6, 3, -20, -4]
fb, dv = ambas(serie)
assert fb[2] == dv[2] == 17
assert dv[0] <= 3 < dv[1]
assert suma_cruzada(serie, 0, 3, 7)[2] == 17

# Cero en la serie y empates: solo se compara la suma.
ambas([0, 0, 0])
ambas([5, -5, 5])

# creamos 200 listas aleatorias, de longitud 1 a 60, con semilla fija.
rng = random.Random(2026)
for _ in range(200):
    n = rng.randint(1, 60)
    serie = [rng.randint(-100, 100) for _ in range(n)]
    fb, dv = ambas(serie)
    assert fb[2] == dv[2]

print("Todas las pruebas estan OK.")
