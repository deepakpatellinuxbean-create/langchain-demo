from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel
# RunnableParallel use hota hai jab hume 2 chains ko parallel run karna hota hai.

load_dotenv()

model1 = ChatOpenAI()
model2 = ChatGoogleGenerativeAI(model="gemini-3.6-flash")

prompt1 = PromptTemplate(
    template='''
    Generate short and simple notes from the following text.

    Text:
    {text}
    ''',
    input_variables=['text']
)

prompt2 = PromptTemplate(
    template='''
    Generate 5 short question-answer pairs from the following text.

    Text:
    {text}
    ''',
    input_variables=['text']
)

prompt3 = PromptTemplate(
    template='''
    Create the final document using the following format:
    ===== NOTES =====
    {notes}

    ===== QUIZ =====
    {quiz}

    Keep the notes and quiz separate.
    Do not mix them.
    ''',
    input_variables=['notes', 'quiz']
)

parser = StrOutputParser()

# RunnableParallel will run both of these chains parallely
parallel_chain = RunnableParallel({
    "notes": prompt1 | model1 | parser,
    "quiz": prompt2 | model2 | parser,
})

merge_chain = prompt3 | model1 | parser

# set the execution order of the chain
chain = parallel_chain | merge_chain

result = chain.invoke({
    "text": "How does the Internet work?"
})

print(result)