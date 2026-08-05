# jese single dynmaic prompt bhejna ho to PromptTemplate use karte hai vese hi jab multiple dynamic prompt (list of prompt in a single list) bhejna hota hai tab ChatPromptTemplate ka use karte hai

from langchain_core.prompts import ChatPromptTemplate

chat_template = ChatPromptTemplate([
    ("system", "You are a helpful {domain} expert"),
    ("human", "explain in simple terms what is {topic}"),
])

prompt = chat_template.invoke({"domain":"cricket", "topic":"dusra"})

print(prompt)