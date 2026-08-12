# =============================================================================
# LENGTH BASED TEXT SPLITTING (CharacterTextSplitter)
# =============================================================================
#
# Text Splitting kya hai?
#   Document / article / PDF ko chhote-chhote pieces (chunks) me todna.
#   Reason: LLM ki context length limited hoti hai — pura doc ek sath nahi bhej sakte. if we give the entire document to the LLM, it will not be able to process it properly.
#
# Length Based splitting kya hai?
#   Isme 2 cheezein matter karti hain:
#     1) chunk_size  → ek chunk me max kitne characters
#     2) separator   → text kis jagah todna hai
#
#   IMPORTANT rule:
#     Agar separator diya hai (jaise "\n"), to pehle separator ke hisaab
#     se split hota hai, phir chunks ko merge karke chunk_size ke andar
#     laane ki koshish hoti hai.
#     Agar separator="" (empty) hai, to seedha character-count (chunk_size) ke basis pr text ko hard cut krta hai.
#
#
# -----------------------------------------------------------------------------
# CASE 1: separator=""  (empty string)
# -----------------------------------------------------------------------------
#   Sirf chunk_size (characters) ke basis pe text break hota hai.
#   Word ke beech se bhi kat sakta hai → context toot jata hai.
#
#   Example:
#     text = "beautiful"
#     chunk_size = 4
#     separator = ""
#
#   Result chunks:
#     "beau" | "tifu" | "l"
#
#   Problem:
#     Word sense kharab → LLM ko samajhna mushkil.
#
#
# -----------------------------------------------------------------------------
# CASE 2: separator="\n"  (ya koi custom string)
# -----------------------------------------------------------------------------
#   Flow:
#     1) Pehle text ko separator (\n) pe tod do → alag lines milengi
#     2) Phir un lines ko merge karo jab tak chunk_size allow kare
#     3) Agar next line add karne se size badh jaye to merge mat perform kro instead → naya chunk start kr do
#
#   Example (chunk_size = 25):
#     Line A: "Hello World"  (11 chars)
#     Line B: "LangChain"    (9 chars)
#     Line C: "Python"       (6 chars)
#
#   Step-by-step:
#     Chunk 1:
#       Line A le lo → length = 11
#       Line B add?  11 + 1 + 9 = 21  → 21 <= 25 → HAAN, add
#       Line C add?  21 + 1 + 6 = 28  → 28 > 25  → NAHI
#       Chunk 1 = "Hello World\nLangChain" (21 chars)
#
#     Chunk 2:
#       Line C se start → "Python" (6 chars)
#
#   Final:
#     Chunk 1 → "Hello World\nLangChain"
#     Chunk 2 → "Python"
#
#
# -----------------------------------------------------------------------------
# CRITICAL EDGE CASE (separator wale mode me)
# -----------------------------------------------------------------------------
#   Agar separator="\n" hai and separator pe todne ke baad KOI EK piece khud chunk_size se bada ho, to CharacterTextSplitter usse FURTHER split NAHI karta instead usse ussi size ka rhne deta hai bus ek warning dikhata hai ki splitted text chunk_size se bada hai.

# Kab use karein?
#   Simple demos, exact character-size control, ya structure matter nahi.
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
    chunk_size=100,      # har chunk max ~100 characters
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
# Yahan docs Document objects hain → split_documents use kiya.
result = splitter.split_documents(docs)

# result kya hoga?
#   Agar text se ~10 chunks bane → result me 10 Document objects.
#   Har Document:
#     - page_content → us chunk ka text (max ~100 chars honge since separator="" hai)
#     - metadata     → original PDF ki info (jaise page number)
#
# Example check karne ke liye:
#   print(len(result))              → kitne chunks bane
#   print(result[0].page_content)   → pehle chunk ka text
#   print(result[0].metadata)       → pehle chunk ki metadata

print(result)
