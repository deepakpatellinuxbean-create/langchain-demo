# jese single dynmaic prompt bhejna ho to PromptTemplate use karte hai vese hi jab multiple dynamic prompt (list of prompts in a single list) bhejna hota hai tab ChatPromptTemplate ka use karte hai

from langchain_core.prompts import ChatPromptTemplate

# jab ChatPromptTemplate ke through dynamic prompt generate krte hai tab hame AIMessage, SystemMessage, HumanMessage classes ka use nahi karte instead hum tuple ka use krte hai below is an example of that
# create a multiple dynamic prompt using ChatPromptTemplate
chat_template = ChatPromptTemplate([
    ("system", "You are a helpful {domain} expert"), # this is equal to SystemMessage class
    ("human", "explain in simple terms what is {topic}"), # this is equal to HumanMessage class
])

prompt = chat_template.invoke({"domain":"cricket", "topic":"dusra"})

print(prompt)