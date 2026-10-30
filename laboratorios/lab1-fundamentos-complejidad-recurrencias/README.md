# Parte 1: Analizar el algoritmo antes de comprar hardware

**Pregunta:** La Secretaría está por firmar la compra de un servidor del doble de velocidad para que el proceso de Tamiza quepa en la ventana de cuatro horas. ¿Por qué debe analizarse primero el algoritmo, si el que está en producción lleva ocho años entregando el resultado correcto?

## Corrección y eficiencia no son lo mismo

Para mí, un algoritmo es _correcto_ si, para toda entrada válida, termina y entrega la salida que se pide. Tamiza lo cumple: insertion sort siempre devuelve los registros ordenados de mayor a menor riesgo. La _eficiencia_ mide otra cosa: cuánto de un recurso consume el algoritmo cuando crece la entrada. Aquí el recurso es el tiempo de ejecución, y se mide contra la restricción de cerrar antes de las 6:00 a. m.

La corrección dice qué sale, pero no dice cuánto tarda en salir. Un algoritmo puede dar siempre la respuesta correcta y aun así no servir si la da tarde. Tamiza incumple la ventana de cuatro horas (2:00 a. m. a 6:00 a. m.): con la lista incompleta, el centro de contacto llamó sin orden de riesgo. Por eso las tres fallas recientes no son un error de lógica, son un incumplimiento de tiempo.

## Por qué el servidor del doble de velocidad no resuelve el problema de fondo

Insertion sort, en el caso aleatorio, hace del orden de n² operaciones. Hace ocho años n era unos 20.000 y hoy es 1.200.000, es decir, 60 veces más datos. El trabajo no se multiplicó por 60 sino por 60² = 3.600. Un servidor del doble de velocidad divide el tiempo entre 2 y no toca ese factor de 3.600.

Además, como el costo crece con n², si los datos se duplican el trabajo se cuatriplica. La máquina nueva solo aguantaría unas √2 ≈ 1,4 veces más registros antes de volver a desbordar la ventana. Estaríamos pagando por posponer la falla, no por quitarla.

Un algoritmo como merge sort, del orden de n log n, haría unas 1,2·10⁶ × 20 ≈ 2,4·10⁷ operaciones. Comparado con n², eso es una mejora de decenas de miles de veces, y ningún reloj más rápido la alcanza. El análisis también muestra que el escenario importa. En el B (casi ordenado) insertion sort se acerca a n, pero en A y C no.

## Segundo ejemplo: conciliación de pagos de una tienda en línea

Imagine un script que, cada noche, cruza 2.000.000 de movimientos del banco con 2.000.000 de pedidos de la tienda, usando dos ciclos `for` anidados. Es correcto: encuentra todos los pagos que coinciden. Pero hace unas 4·10¹² comparaciones. Si el equipo hace del orden de 10⁸ a 10⁹ comparaciones por segundo, eso toma entre 1 y 11 horas. La restricción incumplida es que el reporte debe estar listo en una hora, antes de que abra contabilidad. Ordenar una de las listas, o guardarla en una tabla hash, lo reduce a del orden de n log n o n operaciones. No hace falta cambiar de máquina.

## Concepto

No se debe firmar la compra todavía. Primero hay que analizar el algoritmo y medir cómo crece su costo en tiempo con n, porque el hardware no cambia ese crecimiento y solo lo desplaza un poco.

---

# Parte 2: Responsabilidad ambiental y ética de la implementación

**Pregunta:** Como responsable técnico de Tamiza, ¿qué responsabilidad ambiental y ética asume al decidir qué algoritmo de ordenamiento se ejecuta cada madrugada sobre los datos de 1.200.000 pacientes?

## Dimensión ambiental

La energía que gasta un computador es, aproximadamente, su potencia por el tiempo que trabaja (E = P × t). Si el proceso nocturno mantiene el servidor a plena carga durante toda la ventana, cada hora de ejecución se vuelve kilovatios-hora. Como ejemplo supuesto (no medido): un servidor de unos 300 W que trabaja 4 horas gasta 1,2 kWh por noche. Un algoritmo de orden n log n terminaría en pocos minutos y gastaría una fracción pequeña de eso.

La diferencia se multiplica porque el proceso corre todas las madrugadas: 1,2 kWh × 365 noches ≈ 440 kWh al año, y unos 3.500 kWh en ocho años, por una decisión que se tomó una sola vez. Además, con un costo de orden n², cada vez que crecen los datos el consumo crece más rápido que ellos. Duplicar la velocidad del servidor tampoco es neutro: es una máquina más potente, con su propia huella de fabricación, para correr el mismo algoritmo lento. Cambiar el algoritmo es la forma más barata de gastar menos energía, porque el ahorro se repite todos los días.

## Dimensión ética

**Caso 1: el paciente de riesgo alto.** Pensemos en una persona con índice 950. Si el proceso no termina y la lista queda parcial y sin ordenar, a esa persona la pueden llamar de las últimas o no llamarla ese día, y su valoración médica se retrasa. _¿Quién asume el costo?_ El paciente, y es el costo más grave: es de salud y no se puede devolver. La Secretaría lo asume después, como responsabilidad institucional.

**Caso 2: el operador del centro de contacto.** A las 6:00 a. m. recibe una lista incompleta y desordenada. Pasa la jornada llamando a personas de bajo riesgo mientras hay otras más graves sin contactar, y es quien habla con el paciente cuando este pregunta por qué lo llamaron tarde. _¿Quién asume el costo?_ El operador, en desgaste y carga moral, aunque no eligió el algoritmo ni el servidor.

El equipo de desarrollo casi no paga el costo directo del error: lo pagan quienes tienen menos poder de decisión. Esa asimetría es la razón por la que la responsabilidad recae en quien decide, es decir, en mí.

## Tensión propia del caso: el orden decide a quién se llama primero

En un ordenamiento común, un error es una molestia. Aquí el orden es la decisión clínica, así que la corrección exige más que terminar a tiempo:

- **Completitud:** cada registro debe aparecer exactamente una vez; ninguno se pierde ni se duplica.
- **Orden verificado:** conviene comprobar al final que la lista quedó de mayor a menor riesgo, y no suponerlo.
- **Empates:** el índice va de 0 a 1000 y hay 1.200.000 registros, así que habrá muchísimos empates. Necesito una regla explícita y estable (por ejemplo, el resultado más antiguo primero) y no un desempate arbitrario. Merge sort es estable.
- **Fallar bien:** si el tiempo se agota, entregar una lista parcial sin orden es el peor resultado. Es preferible garantizar que lo entregado sea el tramo de mayor riesgo, ya ordenado, y avisar que la lista está incompleta.
  Aquí tiempo y corrección no son independientes: una lista correcta que llega tarde equivale, para el paciente de riesgo alto, a una lista incorrecta.

---

# Parte 3: Peor caso, mejor caso y caso promedio

## 3.1 Explicación

Para hablar de los tres casos primero hay que fijar el tamaño de la entrada. En Tamiza, n = 1.200.000 registros con índice de riesgo entre 0 y 1000. El **conjunto de entradas** son todas las listas posibles de ese tamaño, es decir, todas las formas en que los registros pueden llegar acomodados. El caso describe qué operación estadística se hace sobre el costo del algoritmo (comparaciones y desplazamientos) a lo largo de ese conjunto:

- **Peor caso:** el _máximo_ del costo sobre todas las entradas de tamaño n. Para insertion sort es n(n−1)/2 ≈ 7,2·10¹¹ operaciones, cuando cada registro nuevo tiene que recorrer toda la parte ya ordenada.
- **Mejor caso:** el _mínimo_ del costo sobre esas mismas entradas. Para insertion sort es n−1 ≈ 1,2·10⁶ comparaciones, cuando la lista ya viene en el orden pedido y nada se desplaza.
- **Caso promedio:** el _promedio_ del costo sobre todas las entradas de tamaño n, suponiendo una distribución de probabilidad sobre ellas (aquí, que todos los acomodos son igual de probables). Para insertion sort es cerca de n²/4 ≈ 3,6·10¹¹.
  El peor y el mejor caso son propiedades del algoritmo y de n, no de "un mal día". El promedio, además, depende de la distribución que yo suponga, y si los datos reales no la cumplen, el número no sirve.

### ¿Cuál caso usaría para decidir si entra en producción?

El **peor caso**. La ventana de cuatro horas es estricta: una sola noche que se pase deja al centro de contacto sin lista ordenada, y ya vimos que eso perjudica a pacientes concretos. El peor caso es el único que da una garantía de tiempo para cualquier lote que llegue. El mejor caso no garantiza nada, porque depende de que la suerte acomode los datos. El caso promedio sirve para estimar el consumo energético típico, pero no para firmar un compromiso de tiempo, porque el lote del escenario C no es una rareza hipotética: llega por una migración real.

### Predicción (antes de medir)

Como Tamiza necesita la lista **de mayor a menor** riesgo:

| Escenario            | Mi predicción para insertion sort                                                                                                                                                                                                                                                                                                                                       |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **A, aleatorio**     | Caso promedio: del orden de n²/4.                                                                                                                                                                                                                                                                                                                                       |
| **B, casi ordenado** | Lo más cercano al mejor caso entre los tres escenarios. Pero no es el mejor caso exacto: el 2 % nuevo (unos 24.000 registros) se anexa sin ordenar, y cada uno tiene que desplazarse en promedio medio camino por la lista ya ordenada. Estimo del orden de 1,4·10¹⁰ operaciones: unas 25 veces menos que A, pero miles de veces más que el mejor caso verdadero (n−1). |
| **C, orden inverso** | **Peor caso**: el sistema legado exporta de menor a mayor, o sea justo al revés de lo pedido, y cada registro recorre toda la parte ordenada. Estimo cerca de n²/2.                                                                                                                                                                                                     |

Una precisión sobre los empates: como el índice solo toma 1001 valores, habrá muchos registros con el mismo índice. Con comparación estricta, insertion sort no mueve registros iguales entre sí, así que A y C deberían quedar un poco por debajo de n²/4 y n²/2. La diferencia debería ser de alrededor de 0,1 %, y no debería cambiar la conclusión.
