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

6. **API token/keys configuration**
   
   Open the *.env* file and add your OpenAI and LangChain keys
   ```
   OPENAI_API_KEY = "<your_openai_key>"
   LANGCHAIN_API_KEY = "<your_langchain_key>"
   ```
   *You should have an account for both*

