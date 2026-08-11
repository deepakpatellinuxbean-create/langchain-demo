# =============================================================================
# LENGTH BASED TEXT SPLITTING (CharacterTextSplitter)
# =============================================================================
#
# Text Splitting kya hai?
#   Document / article / PDF ko chhote-chhote pieces (chunks) me todna.
#   Reason: LLM ki context length limited hoti hai — pura doc ek sath nahi bhej sakte. if we give the entire document to the LLM, it will not be able to process it properly.
#
# Length Based splitting kya hai?
#   Isme hum sirf CHUNK SIZE (characters ki count) decide karte hain. chunk size is the maximum number of characters in a chunk.
#   Example: chunk_size=100 → har chunk me ~100 characters honge.
#   Splitter text ko utne characters ke hisaab se tod deta hai.
#
# Problem / Limitation:
#   Context preserve nahi hota — text KAHI SE BHI break ho sakta hai.
#   Example: "beautiful" word ke beech me break → "beau" | "tiful"
#   Sentence / paragraph ka sense toot sakta hai.
#   Isliye production me aksar RecursiveCharacterTextSplitter prefer kiya jata hai.
#
# Kab use karein?
#   Simple demos, exact character-size control chahiye, ya text structure matter nahi karti.
# =============================================================================

from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

# PyPDFLoader: PDF file ko load karta hai
# Result: list of Document objects (har page ek Document ban sakta hai)
# Har Document me 2 cheezein hoti hain:
#   1) page_content → actual text
#   2) metadata     → source, page number, etc.
loader = PyPDFLoader(file_path="TextSplitter/pdf_file.pdf")
docs = loader.load()

# CharacterTextSplitter = Length Based splitter
# Important parameters:
#   chunk_size    → ek chunk me max kitne characters honge (yahan 100)
#   chunk_overlap → next chunk banate waqt previous chunk ke kitne characters
#                   repeat honge. Overlap se context thoda better milta hai
#                   (jaise last 20 chars next chunk ke start me bhi aa jayein).
#                   0 = bilkul overlap nahi.
#   separator     → kis character/string par split try kare.
#                   "" (empty) = characters ke hisaab se tod do (hard cut).
#                   Agar separator="\n" diya to pehle newline par todne ki koshish karega.
splitter = CharacterTextSplitter(
    chunk_size=100,      # har chunk ~100 characters
    chunk_overlap=0,     # chunks ke beech overlap nahi
    separator=""         # empty → pure character-count based cut
)

# split_text vs split_documents — IMPORTANT difference:
#
#   split_text(text_string)
#       → jab plain string (str) pass karna ho
#       → return: list of strings (chunks)
#
#   split_documents(docs)
#       → jab Document objects (loader se aaye hue) pass karne ho
#       → return: list of Document objects
#       → har chunk ek alag Document ban jata hai
#       → metadata bhi carry forward hota hai (source, page, etc.)
#
# Yahan docs Document objects hain, isliye split_documents use kiya. agar text hota to split_text use kiya jata.
result = splitter.split_documents(docs)

# result kya hoga?
#   Agar text se ~10 chunks bane → result me 10 Document objects.
#   Har Document:
#     - page_content → us chunk ka text (max ~100 chars)
#     - metadata     → original PDF ki info (jaise page number)
#
# Example check karne ke liye:
#   print(len(result))              → kitne chunks bane
#   print(result[0].page_content)   → pehle chunk ka text
#   print(result[0].metadata)       → pehle chunk ki metadata

print(result)
