# =============================================================================
# DOCUMENT STRUCTURE BASED SPLITTING
# (RecursiveCharacterTextSplitter.from_language)
# =============================================================================
#
# Ye Text Structure Based (RecursiveCharacterTextSplitter) ka EXTENDED version hai.
#
# Text Structure Based kab kaafi hota hai?
#   Jab document me plain English text ho —
#   paragraphs, lines, words naturally present hote hain.
#   Default separators kaafi hain: \n\n → \n → " " → ""
#
# Document Structure Based kab chahiye?
#   Jab file me plain English NA ho — jaise:
#     - Python / JS / Java code
#     - Markdown
#     - HTML / JSON etc.
#
#   In documents me "paragraph" wala sense alag hota hai.
#   Example: Python me meaningful break points hain:
#     class, def, empty lines, comments, etc.
#
# Logic same hai (recursive split → check size → further split → merge),
# bas SEPARATORS document type ke hisaab se change ho jate hain.
#
# Isliye hum from_language(...) use karte hain —
# ye automatically us language ke sahi separators set kar deta hai.
# =============================================================================

from langchain_text_splitters import RecursiveCharacterTextSplitter, Language

# Is example me hum PYTHON CODE split kar rahe hain (plain English text nahi)
text = """
class Student:
    def __init__(self, name, age, grade):
        self.name = name
        self.age = age
        self.grade = grade  # Grade is a float (like 8.5 or 9.2)

    def get_details(self):
        return self.name

    def is_passing(self):
        # Add passing condition here


# Example usage
student1 = Student("Aarav", 20, 8.2)

print(student1.get_details())

if student1.is_passing():
    print("The student is passing.")
else:
    print("The student is not passing.")
"""

# =============================================================================
# from_language() kya karta hai?
# =============================================================================
#
# Normal RecursiveCharacterTextSplitter:
#   default separators = ["\n\n", "\n", " ", ""]
#
# from_language(Language.PYTHON):
#   Python-specific separators use hote hain, jaise roughly:
#     - class / def boundaries
#     - blank lines
#     - lines / words / characters (fallback)
#
# Matlab pehle code structure ke hisaab se todne ki koshish —
# taaki ek function / class ka logic ek saath zyada better rahe.
#
# Language options examples:
#   Language.PYTHON, Language.JS, Language.MARKDOWN,
#   Language.HTML, Language.JAVA, etc.
#
# Important parameters:
#   language      → kis document type ke separators use karne hain
#   chunk_size    → ek chunk me max kitne characters (yahan 300)
#   chunk_overlap → next chunk me previous ke kitne chars repeat
#                   0 = overlap nahi
# =============================================================================

splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON,  # Python code ke separators auto-set
    chunk_size=300,            # har chunk max ~300 characters
    chunk_overlap=0,           # chunks ke beech overlap nahi
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
#       → metadata bhi carry forward hoti hai
#
# Yahan `text` plain string (Python code) hai, isliye split_text use kiya.
chunks = splitter.split_text(text)

# chunks kya hoga?
#   list of strings — har string ek code chunk.
#   Ideal case me: related code (jaise ek method / block) ek chunk me
#   zyada meaningful tarike se group hoga, vs random character cut.
#
# Example check:
#   print(len(chunks))   → kitne chunks bane
#   print(chunks[0])     → pehla chunk
#   print(chunks[1])     → doosra chunk (agar bana ho)

print(len(chunks))
print(chunks)
