# **Custom Multi-Agent Recruiter with LangGraph**

## **Introduction and motivation**

...

## **Prerequisites**

1. **Install Python version 3.11 (just in case you haven’t already installed it :stuck_out_tongue_winking_eye:)**

   [Python official download website](https://www.python.org/downloads/)

2. **Install Git**

   [Git official download website](https://www.git-scm.com/downloads)

3. **Navigate to your local machine project directory and initialize a new git repository version control**

    On Windows:
    ```sh
    cd your/dir/path/
    git init
    ```

    *You may have to set your username and email at this point* -> [Git config tutorial](https://www.youtube.com/watch?v=yDntCIs-IJM)

4. **Clone this GitHub repository to your local machine directory**

    [Tutorial for beginners](https://www.youtube.com/watch?v=q9wc7hUrW8U)

    On Windows:
    ```sh
    git clone https://github.com/kokeitor/Cv-Analyzer.git
    ```
   
5. **Virtual environment setup**
  
    - Create your virtual environment
    
        On Windows:
        ```sh
        cd your/dir/path/
        python -m venv <venv_name>
        ```

    - Activate your virtual environment
    
        On Windows:
        ```sh
        <venv_name>\Scripts\activate
        ```

    - Install the necessary packages and libraries

        On Windows:
        ```sh
        pip install -r requirements.txt
        ```

    *WAIT for the installation to finish! :smiley:*

6. **API token/key configuration**
   
   Open the *.env* file and add your OpenAI and LangChain keys
   ```
   OPENAI_API_KEY = "<your_openai_key>"
   LANGCHAIN_API_KEY = "<your_langsmith_key>"
   ```
    *For get both you should check this tutorials*

   [Fancy OpenAI Key tutorial](https://www.youtube.com/watch?v=aVog4J6nIAU)

   [Fancy LangChain [LangSmith] tutorial](https://www.youtube.com/watch?v=bE9sf9vGsrM)

## **App modes**

For using the Custom Multi-Agent Recruiter, i have design several **"app modes"** *some of them still on the develop phase*

1. **One-Shot Pipeline Mode**

    - Set up the configuration JSON file 

        Open *config* folder and, inside the *data.json* file, add all the candidates CV (Curriculum vitae or resume) you want to analyze with the job offer linked to that analysis

        *I have include, in the last JSON object inside this JSON array, an example or template you could tune for your specific case*

        ***Note that with this template you ensure a good performance of the model and the agents analysis***

        ```json
        [
            {
                "oferta": "<job_offer_description_1>", 
                "cv": "<candidate_1_CV>"
            },
            { 
                "oferta": "<job_offer_description_2>", 
                "cv": "<candidate_2_CV>"
            },
            {
                "oferta": "Analista de Datos en Empresa Tecnológica",
                "cv": "Nombre: Carlos Ruiz\nResidencia: Calle del Parque 78, Ciudad Central\nCorreo: carlos.ruiz@ejemplo.com\nTeléfono: 555-456-7891\n\nEXPERIENCIA PROFESIONAL\n- Junio 2021 / Presente: Analista de Datos - TechData Solutions\n  Análisis de grandes conjuntos de datos, creación de dashboards, generación de informes.\n\n- Septiembre 2018 / Mayo 2021: Programador - Software Innovators\n  Desarrollo de software, pruebas de calidad, implementación de mejoras.\n\n- Enero 2016 / Agosto 2018: Soporte Técnico - HelpDesk Corp\n  Resolución de incidencias técnicas, soporte al cliente, mantenimiento de sistemas.\n\nFORMACIÓN ACADÉMICA\n- Finalizada en Mayo 2018: Ingeniería Informática, Universidad de Ciudad Central\n\nIDIOMAS\n- Inglés: Fluido (C2) en lectura, Fluido (C2) en oral, Fluido (C2) en escrita\n- Español: Nativo (C2) en lectura, Nativo (C2) en oral, Nativo (C2) en escrita\n\nHABILIDADES\n- Análisis de datos\n- Programación en Python y Java\n- Creación de dashboards\n\nOtros datos\n- Certificación en Data Science, 2020\n- Participación en proyectos de inteligencia artificial\n"
            }
        ]
        ```

    - Run the pipeline

        Navigate to your local directory project where *app.py* is located using cmd on windows:

        ```sh
        cd your/dir/path
        ``` 

        Then type:
        ```sh
        python app.py --mode 'pipeline'
        ````
        

2. **LangGraph Multi-Agent Mode**
3. **FastApi Mode**
4. **Chat-Bot Web Mode** [Development]
