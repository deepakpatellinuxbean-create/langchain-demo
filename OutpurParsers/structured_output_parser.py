# JsonOutputParser json to dega lekin schema enforce nahi kr skte hum bus itna confirm hai ki vo return kr dega JSON uske khud ke hisab se as a response


from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import ResponseSchema, StructuredOutputParser
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(max_completion_tokens=100)

# create a parser object
parser = StructuredOutputParser()

# 1st prompt -> detailed report
template = PromptTemplate(
    template='Give me name, age and city of a fictional character \n {format_instruction}',
    input_variables=[], # kuch nahi aayega input_variables me bcoz hum koi dyanmic value nahi bhej rhe hai user se leke run time pr instead hum to simply format_instruction bhej rhe hai bus to ye to predefine kiye jaa sakte hai. agar {some_value} hota to yaha usko mention and template me uski value set karna padti
    partial_variables={"format_instruction": parser.get_format_instructions()} # format instruction ki value is function se set hoti hai
)