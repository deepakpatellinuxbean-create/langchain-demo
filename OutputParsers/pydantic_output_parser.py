# PydanticOutputParser: Pydantic model se schema + data validation dono milte hain
# (types, constraints jaise gt=18). Galat type / invalid value pe parse fail ho sakta hai.

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

model = ChatOpenAI(max_completion_tokens=100)

# desired output shape + validation rules
class Person(BaseModel):
    name: str = Field(description="name of the person")
    age: int = Field(gt=18, description="age of the person (must be > 18)")
    city: str = Field(description="city of the person")

parser = PydanticOutputParser(pydantic_object=Person)

template = PromptTemplate(
    template='Generate the name, age and city of a fictional {place} person \n {format_instruction}',
    input_variables=["place"],
    partial_variables={"format_instruction": parser.get_format_instructions()},  # format rules prompt me inject
)

chain = template | model | parser

result = chain.invoke({"place": "Delhi"})

print(result)
