"""Algoritmos de ordenamiento instrumentados para el Laboratorio 1."""


def insertion_sort(datos: list[int]) -> tuple[list[int], int]:
    """Ordena una lista de indices de riesgo con el metodo de insercion.

    No modifica la lista recibida: trabaja sobre una copia.

    Args:
        datos: lista de indices de riesgo a ordenar.

    Returns:
        Una tupla con la lista ordenada y el numero total de
        comparaciones entre elementos realizadas durante el proceso.
    """
    # Tamiza necesita la lista de mayor a menor riesgo, asi que el orden
    # que produce el algoritmo es descendente.
    resultado = list(datos)  # copia: la lista recibida no se toca
    comparaciones = 0

    for i in range(1, len(resultado)):
        clave = resultado[i]
        j = i - 1
        # Se desplazan hacia la derecha los elementos menores que la clave.
        # Solo se cuenta la comparacion entre dos elementos de la lista
        # (resultado[j] < clave); la condicion j >= 0 es de limite y no
        # cuenta.
        while j >= 0:
            comparaciones += 1
            if resultado[j] < clave:
                resultado[j + 1] = resultado[j]
                j -= 1
            else:
                break
        resultado[j + 1] = clave

    return resultado, comparaciones


def _mezclar(izq: list[int], der: list[int]) -> tuple[list[int], int]:
    """Combina dos listas ya ordenadas de mayor a menor en una sola.

    En un empate se toma primero el elemento de la izquierda, lo que hace
    estable al ordenamiento.

    Args:
        izq: primera lista, ordenada de mayor a menor.
        der: segunda lista, ordenada de mayor a menor.

    Returns:
        Una tupla con la lista combinada y el numero de comparaciones
        entre elementos realizadas durante la mezcla.
    """
    resultado: list[int] = []
    i = j = 0
    comparaciones = 0
    # La condicion de limites del ciclo no se cuenta como comparacion.
    while i < len(izq) and j < len(der):
        comparaciones += 1
        if izq[i] >= der[j]:
            resultado.append(izq[i])
            i += 1
        else:
            resultado.append(der[j])
            j += 1
    # Cuando una mitad se agota, el resto de la otra ya esta en orden.
    resultado.extend(izq[i:])
    resultado.extend(der[j:])
    return resultado, comparaciones


def _merge_sort_rec(lista: list[int]) -> tuple[list[int], int]:
    """Aplica dividir, conquistar y combinar sobre una copia de la lista.

    Args:
        lista: lista que la funcion puede consumir sin afectar al llamador.

    Returns:
        Una tupla con la lista ordenada de mayor a menor y el numero total
        de comparaciones entre elementos.
    """
    if len(lista) <= 1:  # caso base: 0 o 1 elementos ya estan ordenados
        return lista, 0
    medio = len(lista) // 2
    izq, comp_izq = _merge_sort_rec(lista[:medio])  # dividir + conquistar
    der, comp_der = _merge_sort_rec(lista[medio:])
    resultado, comp_mezcla = _mezclar(izq, der)  # combinar
    return resultado, comp_izq + comp_der + comp_mezcla


def merge_sort(datos: list[int]) -> tuple[list[int], int]:
    """Ordena una lista de indices de riesgo con el metodo de mezcla.

    No modifica la lista recibida: trabaja sobre una copia.

    Args:
        datos: lista de indices de riesgo a ordenar.

    Returns:
        Una tupla con la lista ordenada y el numero total de
        comparaciones entre elementos realizadas durante el proceso.
    """
    # Igual que insertion_sort, produce orden descendente (mayor riesgo
    # primero).
    # Los cortes lista[:medio] y lista[medio:] crean listas nuevas, por lo que
    # la lista recibida nunca se modifica.
    return _merge_sort_rec(list(datos))
