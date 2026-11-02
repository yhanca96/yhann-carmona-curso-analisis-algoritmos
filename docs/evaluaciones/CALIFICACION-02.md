# Retroalimentación — Laboratorio 2: Dividir y vencer

**Estudiante:** Yhan Camilo Carmona Usme · **Laboratorio:** Laboratorio evaluativo 02 — Dividir y vencer
**Fecha límite:** 2026-11-01 23:59 · **Versión revisada:** commit `3bf4877`

Excelente trabajo: un laboratorio muy completo y bien razonado.

## Nota

| Criterio | Puntos |
|---|---|
| Corrección conceptual | 20 / 20 |
| Calidad de la explicación teórica | 20 / 20 |
| Corrección de la implementación | 25 / 25 |
| Calidad del análisis de las gráficas | 25 / 25 |
| Documentación y organización del informe | 9 / 10 |
| **Total** | **99 / 100** |
| **Nota (0–5)** | **4.95** |

## 1. Corrección conceptual (20 / 20)
**Lo que hizo bien:**
- Identifica con sus propios datos que divide y vencerás empieza a ganar entre n=10 y n=50, y explica por qué en tamaños pequeños pierde (el costo de las llamadas recursivas y de los dos barridos del caso cruzado).
- Compara bien con el máximo de un arreglo: la recurrencia `T(n) = 2T(n/2) + Θ(1)` da `Θ(n)`, igual que recorrerlo una vez, porque combinar cuesta muy poco. Contrasta con el subarreglo máximo, donde la alternativa era `Θ(n²)`.
- La recomendación para la cooperativa es clara. Declara que el valor a 1.000.000 de registros es una **estimación**, la calcula con la forma de cada curva (no con regla de tres lineal) y aclara que es un orden de magnitud.

## 2. Calidad de la explicación teórica (20 / 20)
**Lo que hizo bien:**
- Plantea `T(n) = 2T(n/2) + Θ(n)` explicando de dónde sale cada término: 2 subproblemas de tamaño n/2, un caso cruzado que cuesta `Θ(n)` y una combinación de `Θ(1)`.
- Resuelve con el método maestro verificando la condición del caso 2 (`f(n) = Θ(n^(log_b a))`) y llega a `Θ(n log n)`.
- Justifica que la fuerza bruta es `Θ(n²)` contando los n(n+1)/2 pares de días, cada uno a costo constante.

## 3. Corrección de la implementación (25 / 25)
**Lo que hizo bien:**
- Las tres funciones dan la suma correcta en la serie de ocho días (17), con un solo elemento, con todos negativos, con todos positivos y en un caso cruzado.
- Las pruebas comparan ambos algoritmos en 200 listas aleatorias (más de las 20 pedidas), comparan sumas y no índices, y revisan que la lista de entrada no cambie.
- `subarreglo_maximo` resuelve los tres casos sin llamar a la fuerza bruta, y la fuerza bruta acumula la suma dentro del ciclo.
- Todas las funciones tienen *docstring* con `Args` y `Returns`, *type hints* y las líneas en blanco entre funciones.

## 4. Calidad del análisis de las gráficas (25 / 25)
**Lo que hizo bien:**
- La gráfica tiene ambas curvas en los mismos ejes (en escala lineal y también log-log), título, ejes rotulados con unidades y leyenda, con nueve tamaños que incluyen dos menores de 100 y uno de 16000.
- Mide con `time.perf_counter()`, deja la generación de datos fuera del cronómetro, usa semilla fija, repite cada medición y reporta la mediana. Verifica en cada tamaño que las dos sumas coincidan.
- En la pregunta 2 calcula los factores al duplicar n (≈ 4,3 y ≈ 3,9 en fuerza bruta; ≈ 2,0 y ≈ 2,5 en divide y vencerás) y los contrasta correctamente con lo que predicen `Θ(n²)` y `Θ(n log n)`. Los valores del informe coinciden con lo que muestra la gráfica (fuerza bruta cerca de 5500 ms y divide y vencerás cerca de 20 ms en n=16000).

## 5. Documentación y organización del informe (9 / 10)
**Lo que hizo bien:**
- La carpeta del laboratorio está en una ubicación válida (`laboratorios/lab2-divide-y-vencer/`) y tiene todos los archivos del entregable.
- El `README.md` sigue el orden pedido, la gráfica está incrustada con ruta relativa que sí existe, cada parte enlaza su código y hay instrucciones de reproducción.
- Hay cinco commits descriptivos sobre el laboratorio.

**Lo que puede mejorar (y cómo corregirlo):**
- El nombre al inicio del informe aparece como "Yhann Camilo Carmona": le falta el segundo apellido y está escrito distinto a su nombre completo.
  → *Cómo corregirlo:* escriba su nombre completo, tal como figura en la lista del curso.
- El informe dice que las pruebas imprimen "Todas las pruebas pasaron.", pero el programa imprime "Todas las pruebas estan OK.".
  → *Cómo corregirlo:* haga que el mensaje del informe y el del programa digan lo mismo.

## ¿El código funciona?
Sí. Las pruebas corren sin errores y pasan todas. Los dos algoritmos coinciden en los casos fijos y en las listas aleatorias, y el experimento está preparado para regenerar la gráfica.
