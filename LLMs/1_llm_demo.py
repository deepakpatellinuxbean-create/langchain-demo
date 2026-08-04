from langchain_openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

llm = OpenAI(model="gpt-3.5-turbo-instruct", max_completion_tokens=10) 

result = llm.invoke("what is the capital of India")

print(result)