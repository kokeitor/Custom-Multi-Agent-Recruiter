Aquí tienes las correcciones de las faltas de ortografía y gramática:

# **Custom Recruiter Agent with LangGraph**

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

For using the Custom Multi-Agent Recruiter i have design several **"app modes"** *some of them still on the develop phase*

1. **One-Shot Pipeline Mode***
2. **LangGraph Multi-Agent Mode**
3. **FastApi Mode**
4. **Chat-Bot Web Mode** [Development]
