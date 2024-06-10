from langchain_core.output_parsers import JsonOutputParser,StrOutputParser
from .prompts import (
    routing_prompt,
    grader_prompt,
    gen_prompt,
    hallucination_prompt,
    answer_prompt,
    clasify_prompt
)
from .models import (
    LLM
)

### Router chain
router_chain = routing_prompt | LLM | JsonOutputParser()

### Grader chain
grader_chain = grader_prompt |  LLM | JsonOutputParser()

### RAG chain (generation)
rag_chain = gen_prompt | LLM | StrOutputParser()

### Hallucination chain (grader)
hallucination_chain = hallucination_prompt |  LLM | JsonOutputParser()

### Answer grader
answer_chain = answer_prompt |  LLM | JsonOutputParser()

### calsifier grader
clasify_chain = clasify_prompt |  LLM | JsonOutputParser()


def main():
    print(type(router_chain))

if __name__ == '__main__':
    main()