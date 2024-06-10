from langchain.prompts import PromptTemplate

### PROMPTS 
classify_cv = PromptTemplate(
            template="""system You are an assistant specialized in categorizing documents from the Spanish
            Boletín Oficial del Estado (BOE). Your task is to classify the provided text using the specified list of labels. The posible labels are: {labels}
            You must provide three posible labels ordered by similarity score with the text content. The similarity scores must be a number between 0 and 1.
            Provide the values as a JSON with three keys : 'Label_1','Label_2','Label_3'and for each label two keys : "Label" for the the label name and "Score" the similarity score value.
            user
            Text: {text} assistant""",
            input_variables=["text", "labels"]
        )


