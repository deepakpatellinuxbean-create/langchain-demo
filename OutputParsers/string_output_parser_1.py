from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(max_completion_tokens=100)

# 1st prompt -> detailed report
template1 = PromptTemplate(
    template='Write a detailed report on {topic}',
    input_variables=['topic']
)

# 2nd prompt -> summary
template2 = PromptTemplate(
    template='Write a 5 line summary on the following text: \n {text}',
    input_variables=['text']
)

# StrOutputParser: AIMessage -> plain string/text. Chain me zaroori hai warna next prompt ko AIMessage mil jaayega, srf .content ka content nahi.
parser = StrOutputParser()

# chain: template1 banao -> model ko bhejo -> string nikaalo/string parse kro (.content nikalo) -> template2 banao -> model ko bhejo -> string nikaalo/string parse kro (.content nikalo and result me dal do)
chain = template1 | model | parser | template2 | model | parser

result = chain.invoke({"topic": "black hole"})

print(result)

# Note: hum manually bhi .content nikal sakte hai: lekin chaining me parser ki need hoti hai taki content parse ho jaaye and next step me content available ho.