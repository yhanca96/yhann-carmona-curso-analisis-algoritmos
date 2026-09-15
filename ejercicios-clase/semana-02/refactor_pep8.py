"""Calcula el promedio de una lista de números.
 
Refactorización del script original 'CalcularPromedio', aplicando
las convenciones de PEP 8 y type hints.
"""
 
 
def calcular_promedio(numeros: list[float]) -> float:
    """Calcula el promedio (media aritmetica) de una lista de números.
 
    Args:
        numeros: lista de valores numericos.
 
    Returns:
        El promedio de los valores como float.
    """
    suma = 0
    for numero in numeros:
        suma = suma + numero
    return suma / len(numeros)
 
 
def main() -> None:
    """Punto de entrada del script."""
    lista = [1, 2, 3, 4, 5]
    print(calcular_promedio(lista))
 
 
if __name__ == "__main__":
    main()