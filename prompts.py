PROMPT_NARRATIVO = """
Analiza la siguiente transcripción de una llamada sanitaria.

TRANSCRIPCIÓN:
{texto}

Evalúa:

1. Descripción del síntoma durante la llamada
2. Forma de expresión del malestar
3. Lenguaje utilizado
4. Uso de idioma y sus expresiones
5. Elementos narrativos asociados a la decisión de consulta
6. Minimización o normalización de síntomas
7. Interrupciones del relato
8. Influencia del relato en priorización y activación de recursos
9. Tipo de interrogatorio (guiado o no)
10. Concordancia relato–signo guía

Devuelve la respuesta en español y en formato JSON claro y válido.
"""

PROMPT_CLINICO = """
Analiza clínicamente la siguiente transcripción de una llamada sanitaria.

TRANSCRIPCIÓN:
{texto}

Evalúa:

1. Síntoma principal
2. Posibles diagnósticos diferenciales
3. Nivel de gravedad estimado: bajo, moderado, alto o crítico
4. Síntomas de alarma presentes
5. Síntomas potencialmente minimizados por el paciente
6. Coherencia clínica del relato
7. Posible infraestimación del riesgo
8. Recomendación de priorización asistencial:
   - consejo telefónico
   - consulta urgente
   - activación recurso sanitario
   - activación emergencias

Devuelve la respuesta en español y en formato JSON claro y válido.
"""