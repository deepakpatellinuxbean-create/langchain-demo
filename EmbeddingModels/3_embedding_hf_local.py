# Model download kar ke embedding karna

from langchain_huggingface import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2")

# agar single query kaa embedding generate karna ho
text = "Delhi is the capital of India"

vector = embedding.embed_query(text)

# # agar multiple queries/doc kaa embedding generate karna ho
# documents = [
#     "Delhi is the capital of India",
#     "Kolkata is the capital of West Bengal",
#     "Paris is the capital of France"
# ]

# vector = embedding.embed_documents(documents)

print(str(vector))

