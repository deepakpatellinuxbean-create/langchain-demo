# StructuredOutputParser: ResponseSchema se field names/structure enforce karta hai
# (output me roughly wahi keys aati hain jo schema me di hain).
# Limitation: data type validation nahi — int chahiye tha aur LLM string bhej de to reject nahi hoga.

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_classic.output_parsers import ResponseSchema, StructuredOutputParser
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(max_completion_tokens=100)

# ResponseSchema se desired fields define karo
schema = [
    ResponseSchema(name="fact_1", description="fact 1 about the topic"),
    ResponseSchema(name="fact_2", description="fact 2 about the topic"),
    ResponseSchema(name="fact_3", description="fact 3 about the topic"),
]

parser = StructuredOutputParser.from_response_schemas(schema)

# prompt: topic pe 3 facts + format instructions
template = PromptTemplate(
    template='Give 3 fact about {topic} \n {format_instruction}',
    input_variables=["topic"],
    partial_variables={"format_instruction": parser.get_format_instructions()},  # format rules prompt me inject
)

chain = template | model | parser

result = chain.invoke({"topic": "black hole"})

print(result)
