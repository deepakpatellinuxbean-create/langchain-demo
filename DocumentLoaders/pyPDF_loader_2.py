# =============================================================================
# PDF LOADER (PyPDFLoader)
# =============================================================================
#
# Document Loader kya return karta hai?
#   list of Document objects
#
# Har Document object me:
#   1) page_content → us page ka text
#   2) metadata     → source path, page number, etc.
#
# PyPDFLoader specifically:
#   PDF file ko load karta hai.
#   HAR PAGE ke liye ALAG Document object banata hai.
#
# Example:
#   Agar PDF me 20 pages hain → loader.load() → list me 20 Document objects
#   docs[0] = page 1, docs[1] = page 2, ...
#
# Limitation:
#   Sirf TEXT-based / normal PDFs padhta hai.
#   Scanned pages, image screenshots, complex OCR content → sahi nahi padhega.
#
# Kab kaunsa PDF loader?
#   Simple clean text PDF          → PyPDFLoader
#   Tables / columns               → PDFPlumberLoader
#   Scanned / image PDF            → UnstructuredPDFLoader / AmazonTextractPDFLoader
#   Layout + images bhi chahiye    → PyMuPDFLoader
#   Best structure extraction      → UnstructuredPDFLoader
# =============================================================================

from langchain_community.document_loaders import PyPDFLoader

# PyPDFLoader initiate:
#   file_path → kaunsi PDF load karni hai
loader = PyPDFLoader(file_path="DocumentLoaders/pdf_file.pdf")

# load() → PDF read karta hai
# Return: list of Document objects (1 page = 1 Document)
docs = loader.load()

# Result check (optional):
#   print(len(docs))             → kitne pages / Documents
#   print(docs[0].page_content)  → pehle page ka text
#   print(docs[0].metadata)      → source, page number, etc.
#   print(docs)                  → saare Documents

print(docs)
