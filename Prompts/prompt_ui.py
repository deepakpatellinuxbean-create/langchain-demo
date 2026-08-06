from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import streamlit as st
# PromptTemplate -> Use when creating a prompt directly inside the Python file.
# load_prompt -> Use when the prompt is already saved in a separate file (resusable template)
#                (e.g., template.json) and you want to reuse it.
from langchain_core.prompts import PromptTemplate, load_prompt 

load_dotenv()

model = ChatOpenAI(model="gpt-4", max_completion_tokens=100)

st.header("Research Tool")

paper_input = st.selectbox(
    "Select Research Paper Name",
    [
        "Attention Is All You Need",
        "BERT: Pre-training of Deep Bidirectional Transformers",
        "GPT-3: Language Models are Few-Shot Learners",
        "Diffusion Models Beat GANs on Image Synthesis"
    ]
)

style_input = st.selectbox(
    "Select Explanation Style",
    [
        "Beginner-Friendly",
        "Technical",
        "Code-Oriented",
        "Mathematical"
    ]
)

length_input = st.selectbox(
    "Select Explanation Length",
    [
        "Short (1-2 paragraphs)",
        "Medium (3-5 paragraphs)",
        "Long (detailed explanation)"
    ]
)


# create a single dynamic prompt using prompt template with the file
template = PromptTemplate(
    template = """
Please summarize the research paper titled "{paper_input}" with the following specifications:
Explanation Style: {style_input}
Explanation Length: {length_input}

1. Mathematical Details:
   - Include relevant mathematical equations if present in the paper.
   - Explain the mathematical concepts using simple, intuitive code snippets where applicable.

2. Analogies:
   - Use relatable analogies to simplify complex ideas.

If certain information is not available in the paper, respond with:
"Insufficient information available" instead of guessing.

Ensure the summary is clear, accurate, and aligned with the provided style and length.
""",
input_variables=["paper_input", "style_input", "length_input"]
)

# Ye load_prompt tab required hai jab hum PromptTemplate se template kisi or file me banwante hai for e.g. prompt.generator file and vaha se is file me us template ko import karte hai. asa isliye taki same template multiple module me reuse kia jaa sake
# template = load_prompt('template.json')

# fill the variable values for the input
prompt = template.invoke({
    "paper_input": paper_input,
    "style_input": style_input,
    "length_input": length_input
})

if st.button("Summarize"):
    result = model.invoke(prompt)
    st.write(result.content)


# PromptTemplate use krne ke benefits:
# 1) inbuilt validation
# 2) reusability
# 3) tightly coupled with langchain ecosystem (e.g. for chaining)