import streamlit as st 
import logging
import time
from dotenv import load_dotenv
import os
from model import states
from model import utils
from model import modes

IMAGES_PATH = os.path.join('data','images')

# Logger initializer
logger = logging.getLogger(__name__)


def run_app(compiled_graph, config : modes.ConfigGraphApi ) -> None: 

    def get_response():
        response = f"Pesimo candidatoo texto random jdije ieji2e2 hola analisis que tal estas ho jorge jajajaja ajjajaaj"  
        for word in response.split(" "):
            yield word + " "
            time.sleep(0.07)
            
    
    def get_graph_response(
            cv : str, 
            offer :str,
            chat_history : str, 
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
        
        """
        for word in response.split(" "):
            yield word + " "
            time.sleep(0.07)
        
        
        stream_iterator = config_graph.compile_graph.stream(inputs) # final_report -> report
        for event in stream_iterator:
            logger.info(f"event : {event}")

        return stream_iterator
        """
        return response
    
    
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


    st.title("Reclutador personal Multi-Agente")
    st.write("#")
    st.write("Introduce una descripción de la oferta de trabajo y, a continuación, el CV del candidato a analizar")
    st.write("#")
    
    c1,c2 = st.columns(2)

    with c1:
        st.image(os.path.join(IMAGES_PATH,'logoapp.jpg'))
                
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
                    time.sleep(2)
                    st.write(f"**¡Análisis completado!**")
                    st.write("##")
                st.write_stream(get_graph_response)
            else:
                st.error("Debes aceptar la politica de la empresa para continuar con el análisis")
    
