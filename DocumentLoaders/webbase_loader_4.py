# =============================================================================
# WEB BASE LOADER (WebBaseLoader)
# =============================================================================
#
# WebBaseLoader kya hai?
#   Web page (URL) se text content load karta hai.
#   Under the hood BeautifulSoup HTML parse karke visible text nikalta hai.
#
# Kab use karein?
#   Blogs, news articles, public websites —
#   jahan content mainly TEXT-based aur STATIC ho.
#
# Limitations:
#   - JavaScript-heavy pages sahi nahi load hoti
#     (dynamic content ke liye SeleniumURLLoader better)
#   - Sirf static HTML content aata hai
#     (page render ke baad JS se aane wala data miss ho sakta hai)
#
# Return:
#   list of Document objects
#   Har Document me:
#     page_content → page ka extracted text
#     metadata     → source URL, etc.
#
# Multiple URLs:
#   Ek URL string ya URLs ki list dono pass kar sakte ho.
# =============================================================================

from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

# .env se OPENAI_API_KEY load hota hai
load_dotenv()

# LLM model — webpage text se question answer karne ke liye
model = ChatOpenAI()

# Prompt: question + webpage text dono pass honge
prompt = PromptTemplate(
    template="Answer the question {question} from the following text - \n {text}",
    input_variables=["question", "text"]
)

# Model output ko plain string me convert karega
parser = StrOutputParser()

# Single URL example (Flipkart product page)
# Multiple URLs ke liye list bhi de sakte ho:
#   urls = ["https://example.com/a", "https://example.com/b"]
#   loader = WebBaseLoader(urls)
url = "https://www.flipkart.com/motorola-edge-70-pantone-bronze-green-256-gb/p/itmc5fb119ade9e5?pid=MOBHHWX6CZUZFKBP&param=3251&ctx=eyJjYXJkQ29udGV4dCI6eyJhdHRyaWJ1dGVzIjp7InNvdXJjZUNvbnRlbnRUeXBlIjp7InNpbmdsZVZhbHVlQXR0cmlidXRlIjp7ImtleSI6InNvdXJjZUNvbnRlbnRUeXBlIiwiaW5mZXJlbmNlVHlwZSI6IlNDVCIsInZhbHVlIjoiSUFEIiwidmFsdWVUeXBlIjoiU0lOR0xFX1ZBTFVFRCJ9fX19fQ%3D%3D&nnc=T0JKR0Z20C55_IAD&pageUID=1786371625432"

# WebBaseLoader initiate — URL se page load karega
loader = WebBaseLoader(url)

# load() → page fetch + HTML parse + text extract
# Return: list of Document objects
# Usually 1 URL = 1 Document → docs[0]
docs = loader.load()

# Result check (optional):
#   print(len(docs))
#   print(docs[0].page_content[:500])  → pehle 500 chars
#   print(docs[0].metadata)            → source URL etc.

# LCEL chain: prompt → model → parser
chain = prompt | model | parser

# Question + webpage text bhej ke answer nikal rahe hain
result = chain.invoke({
    "question": "What is the product?",
    "text": docs[0].page_content
})

print(result)
