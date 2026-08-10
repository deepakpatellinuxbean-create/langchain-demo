from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

load_dotenv()

model = ChatOpenAI()

prompt = PromptTemplate(
    template="Answer the question {question} from the following text - \n {text}",
    input_variables=["question", "text"]
)

parser = StrOutputParser()

url = "https://www.flipkart.com/motorola-edge-70-pantone-bronze-green-256-gb/p/itmc5fb119ade9e5?pid=MOBHHWX6CZUZFKBP&param=3251&ctx=eyJjYXJkQ29udGV4dCI6eyJhdHRyaWJ1dGVzIjp7InNvdXJjZUNvbnRlbnRUeXBlIjp7InNpbmdsZVZhbHVlQXR0cmlidXRlIjp7ImtleSI6InNvdXJjZUNvbnRlbnRUeXBlIiwiaW5mZXJlbmNlVHlwZSI6IlNDVCIsInZhbHVlIjoiSUFEIiwidmFsdWVUeXBlIjoiU0lOR0xFX1ZBTFVFRCJ9fX19fQ%3D%3D&nnc=T0JKR0Z20C55_IAD&pageUID=1786371625432"

loader = WebBaseLoader(url) # if we have multiple url we can pass that as well 

docs = loader.load()

chain = prompt | model | parser

result = chain.invoke({"question":"What is the product?" ,"text": docs[0].page_content})

print(result)