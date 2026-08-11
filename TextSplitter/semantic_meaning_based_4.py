# =============================================================================
# SEMANTIC MEANING BASED SPLITTING (SemanticChunker)
# =============================================================================
#
# Pehle ke splitters (Length / Text Structure / Document Structure)
# text ko SIZE ya STRUCTURE (paragraph, line, code) se todte hain.
#
# Semantic Meaning Based alag sochta hai:
#   Text ko MEANING / TOPIC ke hisaab se todta hai.
#   Jab topic change hota hai → wahan naya chunk banata hai.
#
# Example (neeche sample me 3 alag topics hain):
#   1) Farming / fields
#   2) IPL cricket
#   3) Terrorism
#   SemanticChunker ideally in teeno ko alag-alag chunks me tod sakta hai
#   — chahe character count same ho ya nahi.
#
# Kaise kaam karta hai? (simple flow)
#   1) Text ko sentences me todta hai.
#   2) Har sentence ka EMBEDDING banata hai (vector = meaning ka number form).
#   3) Consecutive sentences ke beech DISTANCE / difference nikalta hai.
#      - Distance chhoti → meaning similar → same chunk me rakhna better
#      - Distance badi  → meaning change → BREAKPOINT → naya chunk
#   4) Threshold se decide hota hai ki difference "kitna bada" maana jaye.
#
# Pros:
#   - Topic / meaning better preserve hota hai
#   - Mixed-topic text me cleaner chunks milte hain (search / RAG ke liye useful)
#
# Cons:
#   - Embeddings API / model chahiye → slow + costly ho sakta hai
#   - Length based / recursive se zyada complex
#   - Threshold tuning chahiye (warna bahut kam ya bahut zyada splits)
#   - Offline / no-API setup me mushkil (agar OpenAI embeddings use kar rahe ho)
# =============================================================================

# SemanticChunker langchain_text_splitters me NAHI hai.
# Ye langchain_experimental me milta hai:
#   pip install langchain-experimental
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

# .env se OPENAI_API_KEY load hota hai (embeddings ke liye zaroori)
load_dotenv()

# =============================================================================
# SemanticChunker parameters
# =============================================================================
#
# OpenAIEmbeddings():
#   Sentences ko vectors me convert karta hai.
#   Iske bina semantic similarity measure nahi ho sakti.
#
# breakpoint_threshold_type:
#   Breakpoint (split point) decide karne ka method.
#   Common options:
#     - "percentile"          → distances ka Xth percentile above → split
#     - "standard_deviation"  → mean + (amount * std_dev) above → split
#     - "interquartile"       → IQR based threshold
#     - "gradient"            → distance ke sudden jump / gradient pe split
#
# breakpoint_threshold_amount:
#   Threshold kitna strict / sensitive ho.
#   standard_deviation + amount=1 → mean + 1*std
#   Amount chhota → zyada splits (sensitive)
#   Amount bada   → kam splits (strict)
#
# Yahan:
#   type="standard_deviation", amount=1
#   → meaning me 1 std-dev jitna jump aaye to naya chunk.
# =============================================================================

text_splitter = SemanticChunker(
    OpenAIEmbeddings(),
    breakpoint_threshold_type="standard_deviation",
    breakpoint_threshold_amount=1,
)

# Sample text me jaan-bujhkar 3 alag topics mix kiye hain:
# Farming → IPL → Terrorism
# Semantic splitter ko in topic shifts pe break karna chahiye.
sample = """Farmers were working hard in the fields, preparing the soil and planting seeds for the next season. The sun was bright, and the air smelled of earth and fresh grass. The Indian Premier League (IPL) is the biggest cricket league in the world. People all over the world watch the matches and cheer for their favourite teams.
Terrorism is a big danger to peace and safety. It causes harm to people and creates fear in cities and villages. When such attacks happen, they leave behind pain and sadness. To fight terrorism, we need strong laws, alert security forces, and support from people who care about peace and safety."""

# create_documents([text]) kya karta hai?
#   Input: list of plain text strings
#   Output: list of Document objects (har chunk ek Document)
#            → page_content = chunk text
#            → metadata bhi ho sakti hai
#
# Note:
#   Baaki splitters me aksar split_text / split_documents use hota hai.
#   SemanticChunker me commonly create_documents(...) use karte hain
#   (ye bhi internally semantic split karke Documents return karta hai).
docs = text_splitter.create_documents([sample])

# Result check:
#   Ideal expectation: topics alag chunks me (farming / IPL / terrorism)
#   Reality: threshold ke hisaab se break points change hote hain —
#   har run me perfect topic boundary guarantee nahi hoti.
#   Example: kabhi farming ke 2 sentences alag chunk me bhi aa sakte hain,
#   ya weather wala sentence IPL ke saath merge ho sakta hai.
#
#   print(len(docs))
#   print(docs[0].page_content)

print(len(docs))
for i, doc in enumerate(docs):
    print(f"\n----- Chunk {i + 1} -----")
    print(doc.page_content)


# Note: SemanticChunker ko perfectly explain kia hai campusx ke text splitter video me.
# https://youtu.be/SEWS9P4ODmc?t=2911

# Note: ye splitter itna accurate result nahi deta hai because it is in a experimental stage to iska use abhi bhut kam kia jata hai.
