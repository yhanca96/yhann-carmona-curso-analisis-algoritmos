# Retroalimentación — Laboratorio 1: Fundamentos, complejidad y recurrencias

**Estudiante:** Yhann Camilo Carmona Usme · **Laboratorio:** Laboratorio evaluativo 01 — Fundamentos, complejidad y recurrencias
**Fecha límite:** 2026-10-30 23:59 · **Versión revisada:** commit `092f91c`

Muy buen trabajo: el informe es claro, apoyado en sus propias mediciones y el código funciona.

## Nota

| Criterio | Puntos |
|---|---|
| Corrección conceptual | 24 / 25 |
| Calidad de la explicación teórica | 24 / 25 |
| Corrección de la implementación | 20 / 20 |
| Calidad del análisis de las gráficas | 19 / 20 |
| Documentación y organización del informe | 8 / 10 |
| **Total** | **95 / 100** |
| **Nota (0–5)** | **4.75** |

## 1. Corrección conceptual (24 / 25)
**Lo que hizo bien:**
- Distingue bien entre que el algoritmo sea correcto y que cumpla la ventana de cuatro horas, y nombra la restricción incumplida.
- Explica con números por qué duplicar la velocidad del servidor no arregla el problema: los datos crecieron 60 veces y el trabajo 3.600 veces.
- Da un segundo ejemplo propio (conciliación de pagos) con cantidad de datos y restricción de tiempo.
- Relaciona el tiempo con la energía (E = P × t), lo multiplica por las noches del año y señala que la máquina nueva también tiene huella ambiental.
- En la parte ética presenta dos casos (paciente y operador), dice quién asume el costo en cada uno y discute completitud, empates y "fallar bien".

**Lo que puede mejorar (y cómo corregirlo):**
- En la dimensión ambiental el ejemplo de 300 W es supuesto y no compara con lo que gastaría el algoritmo recomendado con cifras. → *Cómo corregirlo:* use el tiempo estimado de cada algoritmo en la Parte 4 para comparar los kWh por noche de ambos.

## 2. Calidad de la explicación teórica (24 / 25)
**Lo que hizo bien:**
- Define peor, mejor y promedio indicando sobre qué conjunto de entradas se toma el máximo, el mínimo y el promedio, y justifica usar el peor caso.
- Deja la predicción escrita antes del experimento y la contrasta después con datos.
- Plantea la recurrencia de merge sort explicando cada término y la resuelve con árbol de recursión: costo por nivel, número de niveles y costo total, con comprobación por método maestro.
- Calcula insertion sort línea a línea y presenta la tabla de complejidades.

**Lo que puede mejorar (y cómo corregirlo):**
- La tabla línea a línea usa expresiones como "a lo sumo K + n − 1" en varias filas, lo que deja la suma final algo imprecisa. → *Cómo corregirlo:* indique para cada línea el conteo exacto en el mejor y en el peor caso, y súmelos por separado.

## 3. Corrección de la implementación (20 / 20)
**Lo que hizo bien:**
- `insertion_sort` y `merge_sort` ordenan bien, no modifican la lista recibida, cuentan solo comparaciones entre elementos y no usan `sorted()` ni `list.sort()`.
- `merge_sort` tiene su propia mezcla recursiva.
- Los generadores producen listas del tamaño pedido, con valores distintos y semilla reproducible.
- Todas las funciones tienen *docstring* con `Args` y `Returns`, *type hints* y dos líneas en blanco entre funciones.

## 4. Calidad del análisis de las gráficas (19 / 20)
**Lo que hizo bien:**
- Las tres gráficas existen, con título, ejes rotulados y leyenda, y los escenarios (o algoritmos) van en los mismos ejes.
- Identifica con evidencia el peor caso (C), el promedio (A) y que B está cerca del mejor caso pero sigue siendo cuadrático.
- Describe lo que hace cada curva en la Parte 4 y contrasta con las complejidades de 4.1; explica el comportamiento con tamaños pequeños.
- El concepto técnico recomienda merge sort, responde a la compra del servidor con un dato de `parte4_tiempo.png` en n = 6400, extrapola a la ventana de cuatro horas declarándolo estimación y discute memoria, estabilidad y riesgo del escenario B.

**Lo que puede mejorar (y cómo corregirlo):**
- Las estimaciones para 1.200.000 registros no coinciden entre secciones: en la Parte 3 dice unas 10 h para el escenario A y en 4.3 unas 9,2 h. → *Cómo corregirlo:* use una sola base de cálculo (el mismo tiempo y el mismo método) en todo el informe y cite siempre esa cifra.

## 5. Documentación y organización del informe (8 / 10)
**Lo que hizo bien:**
- La carpeta `laboratorios/lab1-fundamentos-complejidad-recurrencias/` es una ubicación válida y trae todos los archivos del entregable.
- El `README.md` está ordenado por partes, con instrucciones de reproducción, gráficas incrustadas con ruta relativa que funcionan y enlaces al código de cada parte.

**Lo que puede mejorar (y cómo corregirlo):**
- Solo hay 4 commits que tocan el laboratorio y se pedían al menos 5; además, "parte 3 y 4 del laboratorio" junta demasiado trabajo en uno. → *Cómo corregirlo:* haga un commit por avance pequeño (por ejemplo, un commit por parte o por archivo) con un mensaje que diga qué cambió.
- El nombre en el informe aparece como "Yhann Camilo Carmona", sin el segundo apellido. → *Cómo corregirlo:* escriba su nombre completo tal como aparece en la lista del curso.

## ¿El código funciona?
Sí. Ambos scripts corren sin errores, generan las gráficas, y los dos algoritmos ordenan correctamente en las pruebas hechas con listas pequeñas y aleatorias.
