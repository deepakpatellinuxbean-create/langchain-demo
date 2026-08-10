from langchain_community.document_loaders import TextLoader
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

load_dotenv()

model = ChatOpenAI()

prompt = PromptTemplate(
    template="Write a summary for the following poem - \n {poem}",
    input_variables=["poem"]
)

parser = StrOutputParser()

# TextLoader ko initiate kro and file ka name and encoding pass kr do
loader = TextLoader(file_path="DocumentLoaders/text_file.txt", encoding="utf-8")

# ye actual me data ko load krega
docs = loader.load()
# After loading the data we will get a list with a documetn object and object will have page content and metadata

# LangChain doc loaders hamesha list return karte hain
# print(type(docs))  

# # 2. List ke andar actual "document" object hota hai jisme hmare, doc ka actual text (page_content) and metadata hota hai
# print(docs[0]) 

chain = prompt | model | parser

result = chain.invoke({"poem": docs[0].page_content})

print(result)