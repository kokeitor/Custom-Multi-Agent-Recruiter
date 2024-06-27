import streamlit as st 
import logging
import time
import os 

IMGAGES_PATH = os.path.join('data','images')

# Logging configuration
logger = logging.getLogger(__name__)

# Streamlit app setup
st.set_page_config(
                      page_title="Reclutador personal Multi-Agente", 
                      page_icon=":alien:", 
                      layout="centered", 
                      initial_sidebar_state="auto", 
                      menu_items=None
                      )
st.title("Reclutador personal Multi-Agente")
st.write("#")
st.write("Bienvenido! Introduce una descripción de la oferta de trabajo y, a continuación, el CV del candidato a analizar")
st.write("#")

def get_response():
    # Replace the below example code with your model's response generation logic
    # Example: response = chatbot(user_input)
    response = f"Pesimo candidatoo jajajajaa!"  # Placeholder example
    return response

c1,c2= st.columns(2)

with c1:
    st.image(os.path.join(IMGAGES_PATH,'logoapp.jpg'))
             
with c2:
    st.header("Oferta y Candidato")
    offer = st.text_input("Descripción de la oferta de trabajo : ")
    cv = st.text_input("CV del candidato : ")
    politica = st.checkbox("Acepto las condiciones de privacidad de la empresa y el manejo de los datos introducidos")
    
    enviar = st.button("Inicio del analisis")
    st.write("##")
    st.caption("©️ 2024 Multi-Agent Recruiter. Todos los derechos reservados")
    
if enviar:
    if not offer or not cv:
        st.error("Oferta y/o CV no introducidos")
    else:
        if politica:
            response = get_response()
            st.success("Campos introducidos correctos")
            with st.spinner("Analizando candidato ... "):
                time.sleep(3)
                st.text_area("Reclutador Multi-Agente :", value=response, height=200, max_chars=None)
                #st.write(f"Reclutador Multi-Agente :{response}")
    
        else:
            st.error("Debes aceptar la politica de la empresa para continuar con el análisis")
    

    

""" 

# Text input box for user to type their message
user_input = st.text_input("You:", "")

# If the user has typed a message
if user_input:
    # Get the chatbot's response
    response = get_response(user_input)
    
    # Display the chatbot's response
    st.text_area("Chatbot:", value=response, height=200, max_chars=None)

# Optionally, you can keep a chat history
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

if user_input:
    st.session_state['chat_history'].append({'You': user_input, 'Chatbot': response})

if st.session_state['chat_history']:
    for chat in st.session_state['chat_history']:
        st.write(f"You: {chat['You']}")
        st.write(f"Chatbot: {chat['Chatbot']}")

"""
