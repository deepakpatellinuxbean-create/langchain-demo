# =============================================================================
# DIRECTORY LOADER (DirectoryLoader)
# =============================================================================
#
# Kab use karein?
#   Jab ek poora FOLDER load karna ho jisme multiple files hon.
#   Example: pdf_files_directory me kai PDFs hain → saari ek saath load.
#
# Important params:
#   path       → kaunsa folder load karna hai
#   glob       → kaunsi files chahiye (pattern)
#   loader_cls → har file ko load karne ke liye kaunsa loader use ho
#                (yahan PDFs hain, isliye PyPDFLoader)
#
# Common glob patterns:
#   "*.pdf"      → current folder me sirf .pdf files
#   "**/*.txt"   → saari subfolders me .txt files
#   "data/*.csv" → sirf data/ folder me .csv
#   "**/*"       → har type ki har file (all subfolders)
#
# load() vs lazy_load() — IMPORTANT:
#
#   load():
#     - Saari files / pages ek sath memory me list banata hai
#     - Return: list of Document objects
#     - Zyada files ho to slow + memory heavy
#
#   lazy_load():
#     - Generator return karta hai
#     - Ek baar me 1 Document yield hota hai
#     - Memory / time dono bachate hain
#     - DirectoryLoader me usually yahi prefer karo
#     - Jab agla document load hota hai memory me to previous document memory 
#       se bhi remove kr dia jata hai (lazy loading)
#
# Note (PyPDFLoader ke saath):
#   Har PDF page = 1 Document object
#   Example: 3 PDFs, total 15 pages → total 15 Documents
# =============================================================================

from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader

# DirectoryLoader initiate:
#   path       → folder jisme multiple PDFs hain
#   glob       → sirf .pdf files lo
#   loader_cls → har PDF ko PyPDFLoader se load karo
loader = DirectoryLoader(
    path="DocumentLoaders/pdf_files_directory",
    glob="*.pdf",
    loader_cls=PyPDFLoader,
)

# lazy_load() → generator milta hai (poori list ek sath nahi)
docs_gen = loader.lazy_load()

# Generator pe indexing (docs[4]) NAHI chalti.
# Demo / indexing ke liye list me convert kar sakte ho:
#   (yaad rahe: list() karne se saara data memory me aa jata hai)
docs = list(docs_gen)

# Lazy style (bina list banaye) aise iterate karte hain:
#   for doc in loader.lazy_load():
#       print(doc.metadata)
#       print(doc.page_content[:200])

# Result check:
#   print(len(docs))             → total kitne page-Documents bane
#   print(docs[0].page_content)  → pehle Document ka text
#   print(docs[0].metadata)      → source file, page number, etc.

print(len(docs))
print(docs[0].page_content)
print(docs[0].metadata)
