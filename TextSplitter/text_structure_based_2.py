# =============================================================================
# TEXT STRUCTURE BASED SPLITTING (RecursiveCharacterTextSplitter)
# =============================================================================
#
# Ye Length Based splitter ki problem solve karta hai.
#
# Length Based (CharacterTextSplitter) me kya limitation thi?
#   1) separator=""  → hard cut: word ke beech se bhi toot sakta hai
#                      (context/meaning kharab).
#   2) separator="\n" → break sirf newline pe; words intact rehte hain,
#                      LEKIN agar ek line khud chunk_size se badi ho
#                      to further split NAHI hota → chunk size exceed
#                      ho sakta hai (warning aati hai).

#
# Text Structure Based me kya alag hai?
#   Yahan splitting separators ke hisaab se hoti hai — matlab pehle meaningful boundaries (paragraph, line, word) try karta hai. Isse sentence / paragraph ka sense zyada better rehta hai. default separator priority (sabse pehle → sabse last): Paragraph (\n\n) → Line (\n) → Word/Space (" ") → Character ("")
#
# Ye production me SABSE ZYADA use hone wala splitter hai.
# =============================================================================

from langchain_text_splitters import RecursiveCharacterTextSplitter

# Sample plain text
text = """
Space exploration has led to incredible scientific discoveries. From landing on the Moon to
exploring Mars, humanity continues to push the boundaries of what's possible beyond our
planet.

These missions have not only expanded our knowledge of the universe but have also
contributed to advancements in technology here on Earth. Satellite communications, GPS, and
even certain medical imaging techniques trace their roots back to innovations driven by
space programs.
"""

# =============================================================================
# RecursiveCharacterTextSplitter kaise kaam karta hai?
# =============================================================================
#
# "Recursive" isliye kehte hain kyunki process yeh hai:
#   split → check size → agar bada hai to further split → phir merge
#
# Step-by-step flow:
#
#   1) Pehle text ko PARAGRAPH (\n\n) ke basis par todta hai.
#   2) Check: kya har paragraph chunk_size ke andar hai?
#
#      Agar HAAN (paragraph <= chunk_size):
#          → usse further split nahi karta. Waise hi rakh deta hai.
#
#      Agar NAHI (paragraph > chunk_size):
#          → next separator use karta hai: LINE (\n)
#
#   3) Agar line bhi chunk_size se badi hai:
#          → WORD / SPACE (" ") par split karta hai.
#
#   4) Agar koi word bhi chunk_size se bada hai (rare):
#          → last option: CHARACTER ("") par todta hai.
#
# Split ke baad:
#   Chhote pieces ko dobara JOIN / MERGE karta hai
#   taaki final chunk ki length chunk_size ke andar rahe.
#
# chunk_overlap:
#   Agar overlap diya (jaise 50), to next chunk banate waqt
#   previous chunk ke last 50 characters bhi include ho jate hain.
#   Isse chunk boundaries pe context tootne ka chance kam hota hai.
#
# Detailed explanation (CampusX video):
#   https://youtu.be/SEWS9P4ODmc?t=1411
# =============================================================================

# Important parameters:
#   chunk_size    → ek chunk me max kitne characters (yahan 300)
#   chunk_overlap → next chunk me previous ke kitne chars repeat honge
#                   0 = overlap nahi
#
# Note: separators explicitly pass nahi kiye — default use ho rahe hain:
#   ["\n\n", "\n", " ", ""]
splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,      # har chunk max ~300 characters
    chunk_overlap=0,     # chunks ke beech overlap nahi
)

# split_text vs split_documents — IMPORTANT difference:
#
#   split_text(text_string)
#       → jab plain string (str) pass karna ho
#       → return: list of strings (chunks)
#
#   split_documents(docs)
#       → jab Document objects (loader se aaye hue) pass karne ho
#       → return: list of Document objects (har chunk ek Document)
#       → metadata bhi carry forward hoti hai
#
# Yahan `text` plain string hai, isliye split_text use kiya.
chunks = splitter.split_text(text)

# chunks kya hoga?
#   list of strings — har string ek chunk.
#   Length Based se farq: yahan break preferably paragraph/line/word pe hoga,
#   isliye meaning zyada better preserve rehti hai.
#
# Example check:
#   print(len(chunks))   → kitne chunks bane
#   print(chunks[0])     → pehla chunk
#   print(chunks[1])     → doosra chunk (agar bana ho)

print(len(chunks))
print(chunks)
