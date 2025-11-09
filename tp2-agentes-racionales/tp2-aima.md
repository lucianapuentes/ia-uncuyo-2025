# Respuestas 2.10 y 2.11 

---

- ## **Pregunta 2.10**

  - **a)** 
    Un agente de reflejo simple toma decisiones basadas en el estado actual del entorno, no puede ser perfectamente racional en este entorno porque cada movimiento da lugar a una penalización.
    Un agente de reflejo simple tiende a hacer movimientos innecesarios ya que no tiene memoria de estados anteriores.
    Esto resultaría en que el agente perdería puntos por movimientos innecesarios, incluso cuando todas las celdas están limpias.
  
  - **b)**
    Un agente de reflejo con estado puede ser más racional en este entorno ya que tiene memoria interna que se fija si todas las celdas están limpias, y una vez que termina de limpiar
    puede entrar en un estado en el que deja de moverse, evitando así la penalización por movimientos innecesarios.
    Un ejemplo de diseño podría ser reglas como: "Si todas las celdas están limpias, no hacer nada".
  
  - **c)**
    Si las reglas del agente le permiten conocer el estado limpio/sucio de todas las celdas, el agente de reflejo simple puede mejorar bastante, ya que 
    puede evitar movimientos innecesarios al tener una visión completa del entorno en el que está. Sin embargo, un agente de reflejo con estado seguiría siendo superior, ya que
    podría tomar decisiones informadas basadas tanto en la historia (por su memoria) como en el  estado completo del entorno.


- ## **Pregunta 2.11**

  - **a)**
    Un agente de reflejo simple no puede ser perfectamente racional en este entorno por la falta de conocimiento sobre la geografía.
    Sin información sobre los límites o la ubicación de los obstáculos, un agente de reflejo simple podría hacer movimientos inútiles o entrar en bucles infinitos.
  - **b)**
    Un agente de reflejo simple con una función aleatorizada podría superar a un agente de reflejo simple en ciertos entornos, mas que nada si la aleatorización le facilita
    escapar de bucles infinitos. Un ejemplo de este diseño podría ser un agente que elige aleatoriamente entre moverse hacia una dirección u otra 
    cuando no tiene suficiente información para tomar una decisión. El rendimiento de este agente se podría medir simulando varios entornos y comparando
    la cantidad de suciedad limpiada y el número de movimientos penalizados.
  - **c)**
    Un entorno en el que el agente aleatorizado funcione mal sería uno con un entorno con muchos obstáculos.
    En tal entorno, el agente podría pasar mucho tiempo moviéndose aleatoriamente sin encontrar ni limpiar la suciedad, entonces los resultados podrían mostrar 
    un bajo rendimiento en términos de suciedad limpiada y un alto número de movimientos innecesarios.
  - **d)**
    Sí, un agente de reflejo con estado puede superar a un agente de reflejo simple porque puede almacenar información sobre los obstáculos
    y lo descubierto en su entorno, lo que le permite tomar decisiones más informadas. Un ejemplo de diseño podría incluir un mapa interno que se actualiza
    a medida que el agente va explorando el entorno. Este puede decidir no regresar a áreas previamente exploradas que no contengan suciedad.