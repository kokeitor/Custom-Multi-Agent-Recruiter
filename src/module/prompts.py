from langchain.prompts import PromptTemplate

# Prompts
analyze_cv = PromptTemplate(
                template="""Eres un modelo de IA diseñado para evaluar la idoneidad de los candidatos para puestos de trabajo específicos asignando una puntuacion. Recibirás el título de una oferta de trabajo y un CV completo de un candidato. 
                Tu tarea es proporcionar una salida en formato JSON que contenga:
                1. La puntuación. 
                2. Un listado con las experiencias del candidato que estan relacionadas con la oferta propuesta, junto con la informacion de esa experiencia si se encuentra en el cv : Puesto, Empresa y Duracion
                3. Una descripción de por qué el candidato obtuvo la puntuación dada.
            
                Como salida, debe proporcionar un JSON con la siguiente estructura:
                    [
                    puntuacion: 0-100,
                    Experiencias: [
                        [
                        Experiencia: '',
                        Puesto : '',
                        Empresa: '',
                        Duracion: ''
                        ]
                    ],
                    Descripcion: ''
                    ]
                    
                Aqui esta el input:
                Título del Trabajo: {oferta}
                CV del Candidato: {cv}
                
                Un ejemplo de un analisis de un candidato es:

                Título del Trabajo: Cajero en Supermercado Dia
                CV del Candidato: 
                Nombre: Juan Pérez
                Dirección: Calle Falsa 123, Ciudadville
                Email: juan.perez@ejemplo.com
                Teléfono: (555) 555-5555

                Experiencia Laboral:
                - Cajero en Supermercado ABC, 2018-2020
                Responsabilidades: Operar la caja registradora, asistir a los clientes, manejar devoluciones y cambios.

                - Vendedor en Tienda XYZ, 2016-2018
                Responsabilidades: Ayudar a los clientes con sus compras, reponer estanterías, gestionar inventarios.
                
                - Entrenador de futbol
                Responsabilidades: Liderar equipo de juveniles y planear los entrenamientos.

                Educación:
                - Diploma de Educación Secundaria, Escuela Secundaria Ciudadville, 2015

                Habilidades:
                - Servicio al cliente
                - Manejo de efectivo
                - Gestión de inventarios
                - Habilidades de comunicación

                Salida:
                [
                    "puntuación": 70,
                    "Experiencias": ["Vendedor", "Representante de Servicio al Cliente"],
                    "descripción": "Juan Pérez tiene una experiencia significativa como cajero y vendedor, demostrando fuertes habilidades en servicio al cliente y manejo de efectivo, lo que lo convierte en un buen candidato para el puesto de Cajero en Supermercado Dia."
                ]
                
                """,
                input_variables=["cv", "oferta"]
                )

analyze_cv_ = PromptTemplate(
                template="""Eres un modelo de IA diseñado para evaluar la idoneidad de los candidatos para puestos de trabajo específicos asignando una puntuacion. Recibirás el título de una oferta de trabajo y un CV completo de un candidato. 
                Tu tarea es proporcionar una salida en formato JSON que contenga:
                1. La puntuación. 
                2. Un listado con las experiencias del candidato que estan relacionadas con la oferta propuesta, junto con la informacion de esa experiencia si se encuentra en el cv : Puesto, Empresa y Duracion
                3. Una descripción de por qué el candidato obtuvo la puntuación dada.
            
                Como salida, debe proporcionar un JSON con la siguiente estructura:
                    [
                    puntuacion: 0-100,
                    Experiencias: [
                        [
                        Puesto : '',
                        Empresa: '',
                        Duracion: ''
                        ]
                    ],
                    Descripcion: ''
                    ]
                    
                Aqui esta el input:
                Título del Trabajo: {oferta}
                CV del Candidato: {cv}

                Las instrucciones que debes seguir para el analisis son:
                1. Lee el título del trabajo y el CV del candidato.
                2. Compara la experiencia, habilidades y calificaciones del candidato con el título del trabajo.
                3. Asigna una puntuación de 0 a 100 basada en qué tan bien el candidato se ajusta al título del trabajo.
                4. Proporciona una lista de títulos de trabajo relacionados con el que se está evaluando que el candidato también podría ser adecuado.
                5. Escribe una descripción detallada que explique por qué el candidato recibió la puntuación dada.
                
                Un ejemplo de un analisis de un candidato es:

                Título del Trabajo: Cajero en Supermercado Dia
                CV del Candidato: 
                Nombre: Juan Pérez
                Dirección: Calle Falsa 123, Ciudadville
                Email: juan.perez@ejemplo.com
                Teléfono: (555) 555-5555

                Experiencia Laboral:
                - Cajero en Supermercado ABC, 2018-2020
                Responsabilidades: Operar la caja registradora, asistir a los clientes, manejar devoluciones y cambios.

                - Vendedor en Tienda XYZ, 2016-2018
                Responsabilidades: Ayudar a los clientes con sus compras, reponer estanterías, gestionar inventarios.
                
                - Entrenador de futbol
                Responsabilidades: Liderar equipo de juveniles y planear los entrenamientos.

                Educación:
                - Diploma de Educación Secundaria, Escuela Secundaria Ciudadville, 2015

                Habilidades:
                - Servicio al cliente
                - Manejo de efectivo
                - Gestión de inventarios
                - Habilidades de comunicación

                Salida:
                [
                    "puntuación": 70,
                    "Experiencias": ["Vendedor", "Representante de Servicio al Cliente"],
                    "descripción": "Juan Pérez tiene una experiencia significativa como cajero y vendedor, demostrando fuertes habilidades en servicio al cliente y manejo de efectivo, lo que lo convierte en un buen candidato para el puesto de Cajero en Supermercado Dia."
                ]


                Por favor, proporciona la salida en formato JSON según el formato dado.
                
                """,
                input_variables=["cv", "oferta"]
                )