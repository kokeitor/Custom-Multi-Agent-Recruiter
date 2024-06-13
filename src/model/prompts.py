from langchain.prompts import PromptTemplate

# Prompts
analyze_cv_prompt = PromptTemplate(
                template="""Eres un modelo de IA diseñado para evaluar la idoneidad de un candidato para un puesto de trabajo específico asignando una puntuación. Recibirás el título de una oferta de trabajo y un CV completo de un candidato. 
                Tu tarea es proporcionar una salida en formato JSON que contenga:
                1. La puntuación.
                2. Un listado con las experiencias del candidato solo si están relacionadas con la oferta propuesta, junto con la información de esa experiencia si se encuentra en el CV, como son: Puesto, Empresa y Duración.
                3. Una descripción de por qué el candidato obtuvo la puntuación dada.

                Las instrucciones que debes seguir para el análisis son:
                1. Lee el título de la oferta de trabajo y el CV del candidato.
                2. Compara la experiencia, habilidades y responsabilidades del candidato que están relacionadas con la oferta de trabajo.
                3. Asigna una puntuación precisa de 0 a 100 basada en qué tan bien el CV del candidato y su experiencia se ajusta a la oferta de trabajo.
                4. Proporciona una lista de experiencias que incluya el puesto, la empresa y la duración de trabajo del candidato solo si están relacionados con la oferta.
                5. Escribe una descripción detallada basada en su CV que explique por qué el candidato recibió la puntuación dada.

                Debes ser exigente con la puntuación dada al candidato en función de su experiencia profesional y la relación real con la oferta de trabajo.
                No debes incluir en las experiencias de trabajo experiencias del candidato que no estén relacionadas con la oferta de empleo.
                Si el CV del candidato no está relacionado con la oferta de empleo y tampoco tiene experiencia previa relacionada con la oferta de trabajo:
                a) La puntuación debe ser baja.
                b) La descripción de por qué se le ha dado esa puntuación debe ser desfavorable.

                Como salida, debes proporcionar un JSON con la siguiente estructura:
                [ "puntuacion": 0-100 , "experiencias" : [ ["experiencia": "","puesto": "", "empresa": "","duracion": ""] ], "descripcion": "" ]

                Este es el CV del candidato a analizar y la oferta de trabajo:
                Título de la oferta de trabajo: {oferta}
                CV del candidato: {cv}
                """,
                input_variables=["cv", "oferta"]
                )

review_prompt = PromptTemplate(
                template="""
                Eres un modelo de IA diseñado para analizar las posibles alucinaciones de otro modelo al realizar un análisis sobre un CV de un candidato para una oferta de trabajo.
                Puntúa con un 1 si no es correcto, no tiene sentido o no es preciso el análisis realizado [hay alucinación por parte del modelo] y con un 0 si es correcto el análisis, es preciso y se ajusta a la oferta [no hay alucinación por parte del modelo].

                El modelo SÍ ha sufrido una alucinación si:
                1. Las experiencias incluidas en el análisis no tienen relación con la oferta de empleo.
                2. En la descripción se mencionan habilidades del candidato que no tienen relación con la oferta de empleo.
                3. La puntuación es elevada y las experiencias del candidato no tienen relación con la oferta de empleo.

                El modelo NO ha sufrido una alucinación si:
                1. No hay experiencias incluidas en el análisis y en su CV las experiencias del candidato no tienen relación con la oferta de empleo.
                2. En la descripción no se mencionan habilidades del candidato que no tienen relación con la oferta de empleo.
                3. La puntuación es baja y las experiencias del candidato no tienen relación con la oferta de empleo.

                Basate en la siguiente información proporcionada para dar esta puntuación de alucinación: 
                Título de la oferta de trabajo: {oferta}
                CV del candidato: {cv}
                Análisis del candidato: {analisis}

                El formato de salida debe ser en formato JSON según el esquema:
                [ alucionacion: <número entero: 0 o 1> ]
                """,
                input_variables=["cv", "oferta","analisis"]
                )

re_analyze_cv_prompt = PromptTemplate(
                template="""
            Eres un modelo de IA diseñado para corregir un análisis erróneo de un candidato para un puesto de trabajo específico. Tu función es volver a analizar el CV del candidato y corregir el análisis erróneo previo.
            Debes proporcionar una salida en formato JSON que contenga:
            1. La nueva puntuación corregida.
            2. Un listado corregido con las experiencias del candidato solo si están realmente relacionadas con la oferta propuesta, junto con la información de esa experiencia si se encuentra en el CV, como son: Puesto, Empresa y Duración.
            3. Una nueva descripción corregida de por qué el candidato obtuvo la puntuación dada.

            Las instrucciones que debes seguir para la corrección del análisis previo son:
            1. Debes ser exigente con la nueva puntuación corregida del candidato en función de su experiencia y la relación real con la oferta de trabajo.
            2. Debes mejorar y corregir los errores del anterior análisis.
            3. Si el CV del candidato no está relacionado con la oferta de empleo y no tiene experiencia previa relacionada con la oferta de trabajo:
                a) La puntuación debe ser baja.
                b) La descripción debe ser desfavorable.
            4. En la lista de experiencias no puede aparecer una experiencia que no esté relacionada con la oferta de empleo.

            Como salida, debes proporcionar un JSON con la siguiente estructura:
            [ "puntuacion": 0-100 , "experiencias" : [ ["experiencia": "","puesto": "", "empresa": "","duracion": ""] ], "descripcion": "" ]
            
            Este es el CV del candidato a analizar y la oferta de trabajo:
            Título de la oferta de trabajo: {oferta}
            CV del candidato: {cv}

            Este es el análisis erróneo previo:
            Análisis erróneo del candidato: {analisis_previo}
                """,
                input_variables=["cv", "oferta","analisis_previo"]
                )

_sucio = """    Las instrucciones que debes seguir para el analisis son:
                1. Lee el Título de la oferta de trabajo y el CV del candidato.
                2. Lee el analisis erroneo previo localizando sus errores.
                3. Elabora un nuevo analisis correcto del candidato comparando la experiencia, habilidades y responsabilidades del candidato que estan relacionadas con la oferta de trabajo.
                4. Asigna una nueva puntuación de 0 a 100 basada en qué tan bien el candidato se ajusta a la oferta de trabajo.
                5. Proporciona una nueva lista corregida de experiencias que incluya el puesto, la empresa y la duracion de trabajo del candidato solo si estan relacionados con la oferta.
                5. Escribe una nueva descripción detallada basada en su cv que explique por qué el candidato recibió la puntuación dada."""