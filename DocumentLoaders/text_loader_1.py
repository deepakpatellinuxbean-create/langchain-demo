# =============================================================================
# TEXT LOADER (TextLoader)
# =============================================================================
#
# Document Loader kya hai?
#   Kisi bhi type ke document (txt, pdf, webpage, folder...) ko
#   LangChain ke Document format me load karna.
#
# Loader hamesha kya return karta hai?
#   list of Document objects
#
# Har Document object me generally 2 cheezein hoti hain:
#   1) page_content → file ka actual text
#   2) metadata     → source path, encoding, etc. extra info
#
# TextLoader specifically:
#   Plain .txt files ko load karta hai.
#   Simple use case: poem, notes, article text file.
#
# Important params:
#   file_path → kis file ko load karna hai
#   encoding  → file encoding (Windows pe aksar "utf-8" dena safe hai)
# =============================================================================

from langchain_community.document_loaders import TextLoader
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

# .env se OPENAI_API_KEY load hota hai
load_dotenv()

# LLM model (summary generate karne ke liye)
model = ChatOpenAI()

# Prompt: poem ka summary likhne ke liye
# {poem} placeholder me baad me file ka text jayega
prompt = PromptTemplate(
    template="Write a summary for the following poem - \n {poem}",
    input_variables=["poem"]
)

# Model ka output plain string me convert karega
parser = StrOutputParser()

# TextLoader initiate:
#   file_path → DocumentLoaders/text_file.txt
#   encoding  → utf-8 (special characters sahi padhne ke liye)
loader = TextLoader(
    file_path="DocumentLoaders/text_file.txt",
    encoding="utf-8"
)

# load() → actual file read karta hai
# Return: list of Document objects
#
# TextLoader me usually 1 file = 1 Document object
# isliye docs[0] pe pehla (aur aksar only) Document milta hai.
docs = loader.load()

# docs structure check (optional):
#   print(type(docs))            → <class 'list'>
#   print(len(docs))             → kitne Document objects
#   print(docs[0])               → poora Document
#   print(docs[0].page_content)  → sirf text
#   print(docs[0].metadata)      → source, etc.

# LCEL chain: prompt → model → parser
chain = prompt | model | parser

# Poem text Document ke page_content se leke chain me bhej rahe hain
result = chain.invoke({"poem": docs[0].page_content})

print(result)
