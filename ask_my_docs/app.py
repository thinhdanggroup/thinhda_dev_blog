from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

from stream_console import StreamConsoleCallbackManager
from stream_token_handler import StreamTokenHandler
from collect_data import SourceCollector
from llm import LLMType, create_chat_model, new_model_config
from vector_storage import VectorStorage


class Explainer:
    def __init__(self, vector_storage: VectorStorage):
        self.vector_storage = vector_storage
        # model_config = new_model_config("gemini-pro", llm_type=LLMType.GEMINI)
        model_config = new_model_config("mistral", llm_type=LLMType.OLLAMA)
        stream_callback = StreamConsoleCallbackManager()
        self.llm = create_chat_model(
            model_config=model_config,
            temperature=0.3,
            stream_callback_manager=stream_callback,
            verbose=True,
            max_tokens=None,
            n=1,
            callbacks=None,
        )
    def get_conversional_chain(self):
        prompt_template="""
YOUR task answer the questions as detailed as possible from the provided context, if the answer is not in
provided context just say, "answer is not available".

YOUR TASK IS TO PROVIDE THE ANSWER IN THE FOLLOWING FORMAT BELOW:
```
Reasoning: You have to explain the reasoning why you give me that answer
Answer: Your answer uses the context to answer the question. The context is not fully provided in the given file, you have to analyze the context and provide the answer
Concerns: If the context is not enough to provide the answer, you have to mention your concerns. You have to ask question to get more information about the context to provide the answer.
```

Example:
If the context is:
JS is a programming language that is used to create interactive effects within web browsers.

The question is:
What is JavaScript?

Your answer should be:
Reasoning: JavaScript is a programming language that is used to create interactive effects within web browsers.
Answer: JavaScript is a programming language that is used to create interactive effects within web browsers.
Concerns: No concerns

If the context is:
JS is a programming language that is used to create interactive effects within web browsers.
The question is:
What is Python used for?

Your answer should be:
Reasoning: Python is not mentioned in the context, so I cannot provide the answer.
Answer: answer is not available
Concerns: The context does not mention anything about Python, so I cannot provide the answer. Problem with the context:
- The context does not mention anything about Python.
- The context should mention about usage of Python.
- Keywords for you to answer the question: Python, usage, programming language


Now, this is my context:
```
Context:\n{context}?\n
```
Question:\n```\n{question}\n```\n
        """

        prompt = PromptTemplate(template=prompt_template, input_variables=["context","question"])
        chain=load_qa_chain(self.llm,chain_type="stuff",prompt=prompt, verbose=True)
        return chain
        
    def explain(self, query: str):
        docs =  self.vector_storage.search(query)
        chain = self.get_conversional_chain()
        response = chain({"input_documents":docs, "question": query} , return_only_outputs=True)
        print(response.get("output_text","no answer found"))
        
        
        
        

def main():
    print("Hi there!")
    load_dotenv()
    
    vector_storage = VectorStorage()
    source_collector = SourceCollector(vector_storage)
    # source_collector.run(['EN'])
    # source_collector.run_from_parent_page('STG',["2675147153","2742550552","3286958381"])
    source_collector.run_from_parent_page('SD',["2967044270"])
    explainer = Explainer(vector_storage)
    
    query =""
    while query != "exit":
        query = input("Enter your query: ")
        query = query.strip()
        if query == "exit":
            break
        if not query:
            continue
        explainer.explain(query)    
    
    
if  __name__ == '__main__':
    main()