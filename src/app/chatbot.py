import streamlit as st 
import logging
import time
from dotenv import load_dotenv
from typing import Union
import os
from model import states
from model import utils
from model import modes
from model.exceptions import GraphResponseError
from langgraph.graph.graph import CompiledGraph
from databases.google_sheets import GoogleSheet
import pandas as pd
import json

# Logger initializer
logger = logging.getLogger(__name__)


def run_app(compiled_graph : CompiledGraph, config : modes.ConfigGraphApi, graph_image : Union[bytes,None] = None) -> None: 
    
    load_dotenv()
    
    # Locals paths
    IMAGES_PATH = os.path.join('data','images')
    FILE_NAME = os.path.join(".secrets","recruiter-427908-67769637005a.json")
    DOCUMENT_NAME = "bbdd_recruiter"
    SHEET_NAME = "analisis"
    logger.info(f"Image path : {IMAGES_PATH=}")
    logger.info(f"Secrets BBDD path : {FILE_NAME=}")
    
    # Available models 
    MODELS = (
            "OpenAI-gpt-3.5-turbo", 
            "Meta-llama3-70b-instruct"
            )
    
    # Google Sheet database object
    bbdd_credentials = st.secrets["google"]["google_secrets"]
    BBDD = GoogleSheet(credentials=bbdd_credentials, document=DOCUMENT_NAME, sheet_name=SHEET_NAME)

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
        if response["analisis_final"]:
            
            # Manejo de respuesta del langcahin graph para almacenar en BBDD ..
            
            # Manejo de los modelos, agentes, usados en graph para almacenar en BBDD ..
            
            # Manejo del analisis final del modelo -> presentacion en front end y guardar en BBDD analisis
            puntuacion = str(response["analisis_final"].puntuacion)
            nombres_experiencias = [exp["experiencia"] for exp in response["analisis_final"].experiencias]
            puestos_experiencias = [exp["puesto"] for exp in response["analisis_final"].experiencias]
            empresas_experiencias = [exp["empresa"] for exp in response["analisis_final"].experiencias]
            duraciones_experiencias = [exp["duracion"] for exp in response["analisis_final"].experiencias]
            descripcion = response["analisis_final"].descripcion
            
            # Pydantic BaseModel 'Analisis' -> Dataframe to present results of the job experience
            experiencias = pd.DataFrame(
                                    data = {
                                            "Experiencia" : nombres_experiencias,
                                            "Puesto" : puestos_experiencias,
                                            "Empresa" : empresas_experiencias,
                                            "Duración" : duraciones_experiencias,
                                            }
                                    )
            
            # Insert into Google sheet BBDD -> Analisis y Candidato
            BBDD.write_data(
                            range=BBDD.get_last_row_range(), 
                            values=[GoogleSheet.get_record(
                                                            analisis=response["analisis_final"], 
                                                            candidato=response["candidato"]
                                                            )
                                    ]
                            )
            logger.info(f"Insertimg into BBDD -> {response['analisis_final']}")
        
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
        
        else:
            raise GraphResponseError()
    
    
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
    st.write("### Introduce la oferta de trabajo y el CV del candidato a analizar")
    st.write("#")
    
    c1,c2 = st.columns(2)
    sidebar = st.sidebar
    
    with sidebar:
        # Sidebar for selecting LLM model -> future implementation
        option = st.selectbox(
            label=":green[**Modelo**]",
            options =MODELS,
            help ="Modelo LLM para el análisis de arquitectura : Transformer-Decoder"
            )
        
        model_available = True
        if option is not None and str(option).startswith(MODELS[1].split("-")[0]):
            st.success(f"Modelo : {option} disponible")
            model_available = True
        elif option is not None and str(option).startswith(MODELS[0].split("-")[0]):
            model_available = False
            st.error(f"Modelo : {option} no disponible ¡Comming soon!")

    with c1:
        st.image(image=os.path.join(IMAGES_PATH,'logo.jpg'))
                
    with c2:

        offer = st.text_input("Descripción de la oferta de trabajo : ")
        cv = st.text_input("CV del candidato : ")
        politica = st.checkbox("Acepto las condiciones de privacidad de la empresa y el manejo de los datos introducidos")
        
        if model_available:
            inicio_analisis = st.button("Inicio del análisis")
        else:
            st.error("Elige un modelo LLM disponible")
            inicio_analisis = False
        st.write("##")
        st.caption("©️ 2024 Multi-Agent Recruiter. Todos los derechos reservados")
            

    if inicio_analisis:
        if not offer or not cv:
            st.error("Oferta y/o CV no introducidos")
        else:
            if politica:
                st.success("Campos correctamente introducidos")
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
                if graph_image:
                    with st.container():
                        st.markdown("**Grafo Multi-Agente utilizado para el análisis:**")
                        st.image(image=graph_image)
                        
            else:
                st.error("Debes aceptar la politica de la empresa para continuar con el análisis")
    