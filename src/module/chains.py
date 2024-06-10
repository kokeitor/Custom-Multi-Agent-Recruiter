from langchain_core.output_parsers import JsonOutputParser,StrOutputParser
from .prompts import (
    classify_cv
    )
from .models import (
    LLM
)

### Router chain
classify_chain = classify_cv | LLM | JsonOutputParser()


def main():
    print(type(classify_chain))

if __name__ == '__main__':
    main()