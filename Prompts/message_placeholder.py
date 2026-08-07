# jab hume purane chats place krna ho ChatPromptTemplate ke andar tab hum MessagesPlaceholder class ka use karte hai ye ek list leta hai jisme user ki purani chats/messages pade hote hai. Automatically ye andar ke messages ko unpack kr dega

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

chat_template = ChatPromptTemplate([
    ("system", "you are a customer support agent"),
    MessagesPlaceholder(variable_name="chat_history"), # chat history should be a list of messages
    ("human", "{query}")
])

chat_history = []

# read chat history from file
with open("Prompts/chat_history.txt") as f:
    chat_history.extend(f.readlines())

prompt = chat_template.invoke({"chat_history": chat_history, "query": "Where is my refund"})

print(prompt)