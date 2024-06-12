class NoOpenAIToken(Exception):
    """Excepcion para manejo de openAI token"""
    def __init__(self, message:str="No OpenAI API token provided"):
        super().__init__(message)
