# =============================================================================
# CSV LOADER (CSVLoader)
# =============================================================================
#
# CSVLoader kya hai?
#   CSV file ko load karke LangChain Document objects banata hai.
#
# Important rule:
#   HAR ROW = ALAG Document object
#
# Example:
#   Agar CSV me 100 data rows hain → loader.load() → 100 Documents
#
# Har Document me kya hota hai?
#   page_content → us row ke columns "key: value" form me
#                  (har column ek nayi line pe)
#   metadata     → usually {"source": file_path, "row": row_index}
#
# page_content example (ek row):
#   name: Aarav
#   city: Delhi
#   age: 22
#   role: Student
#
# Useful optional params:
#   source_column    → metadata["source"] me file path ki jagah
#                      kisi column ki value set karo
#   metadata_columns → kuch columns page_content me nahi,
#                      metadata me daal do
#   content_columns  → page_content me sirf selected columns
#   encoding         → file encoding (jaise "utf-8")
#
# Kab use karein?
#   Tabular data (employees, products, FAQs, records) ko
#   RAG / search / LLM ke liye Documents me convert karna ho.
# =============================================================================

from langchain_community.document_loaders import CSVLoader

# CSVLoader initiate:
#   file_path → kaunsi CSV load karni hai
loader = CSVLoader(file_path="DocumentLoaders/csv_file.csv")

# Optional advanced example:
# loader = CSVLoader(
#     file_path="DocumentLoaders/csv_file.csv",
#     source_column="name",                 # metadata source = name column
#     metadata_columns=["city", "age"],     # ye columns metadata me jayenge
#     content_columns=["role"],             # page_content me sirf role
#     encoding="utf-8",
# )

# load() → CSV read karta hai
# Return: list of Document objects (1 row = 1 Document)
docs = loader.load()

# Result check (optional):
#   print(len(docs))             → kitni rows / Documents
#   print(docs[0].page_content)  → pehli row ka text
#   print(docs[0].metadata)      → source + row number

print(len(docs))
print(docs[0].page_content)
print(docs[0].metadata)
print(docs)
