# Retroalimentación — Laboratorio 03: Estructuras de datos

**Estudiante:** Yhan Camilo Carmona Usme · **Laboratorio:** Laboratorio evaluativo 03 — Estructuras de datos
**Fecha límite:** 2026-11-01 23:59 · **Versión revisada:** commit `3bf4877`

Excelente trabajo: un informe claro, con datos propios y un código bien hecho.

## Nota

| Criterio | Puntos |
|---|---|
| Corrección conceptual | 20 / 20 |
| Calidad de la explicación teórica | 20 / 20 |
| Corrección de la implementación | 25 / 25 |
| Calidad del análisis de las gráficas | 24 / 25 |
| Documentación y organización del informe | 10 / 10 |
| **Total** | **99 / 100** |
| **Nota (0–5)** | **4.95** |

## 1. Corrección conceptual (20 / 20)
**Lo que hizo bien:**
- Explica bien la colisión (hay 10¹⁰ guías posibles y solo m casillas) y usa el ejemplo de 10, 24 y 17 con m = 7.
- Compara encadenamiento y direccionamiento abierto con ventajas y costos de cada uno.
- Justifica por qué la tabla no sirve para rangos y estima la altura del árbol degenerado (≈ 400.000) frente al equilibrado (18).
- Recomienda tabla hash más árbol equilibrado y declara que la cifra para 5.000.000 de envíos es una estimación.

## 2. Calidad de la explicación teórica (20 / 20)
**Lo que hizo bien:**
- Justifica el Θ(n) de la lista para una guía inexistente y el Θ(1 + α) de la tabla.
- Nombra el supuesto de hash uniforme simple y explica qué pasa si todas las guías caen en una casilla (la tabla se vuelve una lista).

## 3. Corrección de la implementación (25 / 25)
**Lo que hizo bien:**
- Lista y tabla devuelven el estado correcto en búsquedas exitosas e infructuosas; `buscar` usa un ciclo y no recursión.
- La tabla reutiliza la lista, sin `dict`, `set` ni `hash()`.
- Las pruebas cubren la colisión forzada con m = 7, `factor_carga() == 3 / 7` y 30 colecciones aleatorias.
- Todas las funciones tienen docstrings con `Args` y `Returns`, y type hints.

## 4. Calidad del análisis de las gráficas (24 / 25)
**Lo que hizo bien:**
- Ambas gráficas tienen título, ejes rotulados y leyenda; la primera tiene siete valores de n y la segunda ocho valores de α.
- En la pregunta 2 calcula factores de crecimiento (×2,00 de 500 a 1.000 en la lista) y los contrasta con Θ(n) y Θ(1); el ajuste lineal para α es coherente con Θ(1 + α).

**Lo que puede mejorar (y cómo corregirlo):**
- Para la tabla compara solo un par de valores de n, y justo en n = 100.000 la curva sube (de unos 0,25 a unos 0,43 µs en la gráfica) sin que el informe lo comente.
  → *Cómo corregirlo:* mencione ese punto y proponga una causa que usted pueda comprobar con otra medición (por ejemplo, repetir la medida o cambiar el tamaño de la tabla).

## 5. Documentación y organización del informe (10 / 10)
**Lo que hizo bien:**
- La carpeta está en `laboratorios/lab3-estructuras-datos/`, una ubicación válida, con todos los archivos del entregable.
- El README sigue el orden pedido, las gráficas se ven con ruta relativa, cada parte enlaza su código y hay instrucciones de reproducción.
- Hay cuatro commits con mensajes descriptivos.

## ¿El código funciona?
Sí. Las pruebas pasan sin errores y el código genera las dos gráficas con tiempos coherentes con el informe.
