# =============================================================================
# LENGTH BASED TEXT SPLITTING (CharacterTextSplitter)
# =============================================================================
#
# Text Splitting kya hai?
#   Document / article / PDF ko chhote-chhote pieces (chunks) me todna.
#   Reason: LLM ki context length limited hoti hai — pura doc ek sath nahi bhej sakte. if we give the entire document to the LLM, it will not be able to process it properly.
#
# Length Based splitting kya hai?
#   Isme hum CHUNK SIZE (max characters in one chunk) aur SEPARATOR ke hisaab se split karte hain.
#   Yadi splitter me separator mention hai to separator ko preference deke hi cut kia jata hai text na ki chunk size ke hisab se.
#   Example: chunk_size=100 → har chunk me ~100 characters hona chaiye.
#   Splitter text ko utne characters ke hisaab se tod deta hai.
#
# Problem / Limitations (IMPORTANT):
#   1. separator="" (empty string) par: Srf number of character ke basis pr chunk ko break kr dia jata hai ho skta hai word bich me se break ho jaaye 
# For e.g. if the chunk_size is 4 and separator="" and text is "beautiful"
# after splitting it will become "beau", "tifu", "l"
#      - Problem: Context preserve nahi hota, hard cut hota hai (e.g., "beau" | "tiful").
#      - Problem: LLM can't it since the context isn't preserved

#   2. separator="\n" (ya koi custom string) par:
#      - Hum separator="\n" me \n mention karte hai to hmara splitter \n k basis pr text ko split karta hai. then splitted chunk ko merge karne ke kosis krta hai yadi merge krne pr chunk_size se chota hota hai to merge krta hai otherwise merge nahi karta or text ko 2 ala alag chunk ki tarah treat kia jata hai.
e.g. 
Line A: "Hello World"  (11 chars) \n
Line B: "LangChain"    (9 chars)  \n
Line C: "Python"       (6 chars)

Execution Step-by-Step:

Chunk 1 Process:

Line A (11 chars) -> Length = 11.

Line B (9 chars) check karo: 11 + 1 + 9 = 21.

21 <= 25 (chunk_size), toh Line B add ho jayegi! -> Total length = 21.

Agli Line C (6 chars) check karo: 21 + 1 + 6 = 28.

28 > 25, toh Line C add nahi ho sakti.

Chunk 1 Result: "Hello World\nLangChain" (21 chars)

Chunk 2 Process:

Line C se shuru hua.

Chunk 2 Result: "Python" (6 chars)

# 
#      - CRITICAL EDGE CASE: agar separator \n hai and splitter jab \n k basis pr split karta hai text and in case text chunk size se bada ho jata hai to splitter usse further split nahi karta instead usse ussi size ka rhne deta hai bus ek warning dikhata hai ki splitted text chunk_size se bada hai.

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
