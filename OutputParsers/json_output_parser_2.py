# JsonOutputParser: LLM response ko JSON/dict me parse karta hai.
# Limitation: fields/schema enforce nahi hota — LLM apne hisaab se keys bhej sakta hai response me.

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(max_completion_tokens=100)

parser = JsonOutputParser()

# format_instruction partial_variables se pehle se fix ho jaata hai (runtime pe user se nahi aata).
# isliye input_variables empty — koi dynamic {topic} etc. nahi hai.
# agar {topic} hota to input_variables=["topic"] likhte.
template = PromptTemplate(
    template='Give me name, age and city of a fictional character \n {format_instruction}',
    input_variables=[],
    partial_variables={"format_instruction": parser.get_format_instructions()},  # parser ke format rules prompt me inject karta hai
)

# Manual flow: format -> invoke -> parse
prompt = template.format()
result = model.invoke(prompt)
final_result = parser.parse(result.content)

print(final_result)

# OR — chain (same kaam, steps auto-connect): template | model | parser
# chain = template | model | parser
# result = chain.invoke({})  # dynamic values na ho to bhi empty dict bhejna padta hai
# print(result)
