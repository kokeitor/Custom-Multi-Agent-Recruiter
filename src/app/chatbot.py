import streamlit as st 
import logging
import time
from typing import Union
from dotenv import load_dotenv
import os
from model import states
from model import utils
from model import modes
import pandas as pd

# Logger initializer
logger = logging.getLogger(__name__)


def run_app(compiled_graph, config : modes.ConfigGraphApi ) -> None: 
    
    IMAGES_PATH = os.path.join('data','images')
    logger.info(f"Image path : {IMAGES_PATH=}")

    def get_response():
        response = f"Pesimo candidatoo texto random jdije ieji2e2 hola analisis que tal estas ho jorge jajajaja ajjajaaj"  
        for word in response.split(" "):
            yield word + " "
            time.sleep(0.07)
            
    
    def get_graph_response(
            cv : str, 
            offer :str,
            chat_history : Union[str,None] = None, 
            compiled_graph = compiled_graph,
            config : modes.ConfigGraphApi = config
                ):
        
        logger.info(f"Candidato a analizar [Recibido del front end]:  {cv} - {offer}")

        # Instancia clase Candidato
        candidato = states.Candidato(id=utils.get_id(), cv=cv, oferta=offer)
        
        # Añade objeto candidato como valor de la clave "candidato" del state graph (dict) [input del grafo] 
        graph_state_input = {"candidato": candidato}
        logger.info(f"Candidato a analizar :  {candidato}")
        
        response = compiled_graph.invoke(
                                            input=graph_state_input, 
                                            config=config.config_graph,
                                            stream_mode='values'
                                            )
        
        puntuacion = str(response["analisis_final"].puntuacion)
        nombres_experiencias = [exp["experiencia"] for exp in response["analisis_final"].experiencias]
        puestos_experiencias = [exp["puesto"] for exp in response["analisis_final"].experiencias]
        empresas_experiencias = [exp["empresa"] for exp in response["analisis_final"].experiencias]
        duraciones_experiencias = [exp["duracion"] for exp in response["analisis_final"].experiencias]
        descripcion = response["analisis_final"].descripcion
        
        # Pydabtic BaseModel 'Analisis' -> Dataframe to present results of the job experience
        experiencias = pd.DataFrame(
                                data = {
                                        "Experiencia" : nombres_experiencias,
                                        "Puesto" : puestos_experiencias,
                                        "Empresa" : empresas_experiencias,
                                        "Duración" : duraciones_experiencias,
                                        }
                                )
        """
        for word in response.split(" "):
            yield word + " "
            time.sleep(0.07)
        
        
        stream_iterator = config_graph.compile_graph.stream(inputs) # final_report -> report
        for event in stream_iterator:
            logger.info(f"event : {event}")

        return stream_iterator
        """
        return puntuacion,descripcion,experiencias
    
    
    # Front-End 
    # Streamlit app setup
    st.set_page_config(
                        page_title="Reclutador personal Multi-Agente", 
                        page_icon=":alien:", 
                        layout="centered",
                        initial_sidebar_state="auto",
                        menu_items={
                                        'Get Help':  'https://www.linkedin.com/in/jorgeresinomartin/',
                                        'Report a bug': "https://github.com/kokeitor",
                                        'About':  "Reach me at : jresino143@gmail.com"
                                    }         
                            )

    st.logo(image=os.path.join(IMAGES_PATH,'logo.jpg'), link="https://github.com/kokeitor")
    st.title("Reclutador personal Multi-Agente")
    st.write("### Introduce una descripción de la oferta de trabajo y, a continuación, el CV del candidato a analizar")
    st.write("#")
    
    c1,c2 = st.columns(2)

    with c1:
        st.image(image=os.path.join(IMAGES_PATH,'logo.jpg'))
                
    with c2:
        st.header("Oferta y Candidato")
        offer = st.text_input("Descripción de la oferta de trabajo : ")
        cv = st.text_input("CV del candidato : ")
        politica = st.checkbox("Acepto las condiciones de privacidad de la empresa y el manejo de los datos introducidos")
        
        inicio_analisis = st.button("Inicio del analisis")
        st.write("##")
        st.caption("©️ 2024 Multi-Agent Recruiter. Todos los derechos reservados")
        

    if inicio_analisis:
        if not offer or not cv:
            st.error("Oferta y/o CV no introducidos")
        else:
            if politica:
                st.success("Campos introducidos correctos")
                with st.spinner("Analizando candidato ... "):
                    # st.write_stream(get_graph_response)
                    puntuacion,descripcion,experiencias = get_graph_response(cv=cv, offer=offer)
                """ 
                st.write(f"**¡Análisis completado!**")
                st.write(f"**Puntuación del candidato** : {puntuacion}") 
                st.write(f"**Descripción del análisis** : {descripcion}")
                st.write("##")
                st.write(experiencias)
                """
                with st.container():
                    st.write(f"### Puntuación del candidato: **{puntuacion}**") 
                    st.write(f"### Descripción del análisis:")
                    st.write(f"{descripcion}")
                    st.write("### Detalles de las experiencias:")
                    st.dataframe(
                                    experiencias,
                                    column_config={
                                        "Experiencia": st.column_config.TextColumn(
                                            "Experiencia",
                                            help="Experiencias detectadas en el CV del candidato"
                                        ),
                                        "Puesto": st.column_config.TextColumn(
                                            "Puesto",
                                            help="Puesto asociado a la experiencia detectada"
                                        ),
                                        "Empresa": st.column_config.TextColumn(
                                            "Empresa",
                                            help="Empresa asociada a la experiencia detectada"
                                        ),
                                        "Duración": st.column_config.TextColumn(
                                            "Duración",
                                            help="Duracion asociada a la experiencia detectada"
                                        ),
                                    },
                                    hide_index=True,
                                )
            else:
                st.error("Debes aceptar la politica de la empresa para continuar con el análisis")
    