from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser

# RunnableBranch se hum conditional chain implement kar sakte hain.
# RunnableLambda ki help se hum kisi bhi normal Python function/lambda
# function ko Runnable bana sakte hain, taaki use chain ke part ki tarah
# use kiya ja sake. Technically, ye actual chain nahi hota, lekin Runnable
# ki tarah treat kiya jaata hai means as a chain run kr skta hai.

from langchain_core.runnables import RunnableBranch, RunnableLambda
from pydantic import BaseModel, Field
from typing import Literal

load_dotenv()

model = ChatOpenAI()


class Feedback(BaseModel):
    sentiment: Literal["positive", "negative"] = Field(
        description="Give the sentiment of the feedback"
    )


parser1 = StrOutputParser()
parser2 = PydanticOutputParser(pydantic_object=Feedback)

# Hume ensure karna hai ki LLM ka output sirf "positive" ya "negative" ho.
# Isliye hum PydanticOutputParser ka use kar rahe hain.
# PydanticOutputParser LLM ke output ko defined Pydantic structure
# ke according parse karta hai.
# Expected output kuch aisa hoga:
# {sentiment: "positive"} or {sentiment: "negative"}

prompt1 = PromptTemplate(
    template='''
    Classify the sentiment of the following feedback text into
    positive or negative.

    Feedback:
    {feedback}

    {format_instructions}
    ''',
    input_variables=['feedback'],
    partial_variables={
        "format_instructions": parser2.get_format_instructions()
    },
)


# Ye chain feedback ka sentiment classify karegi "positive or negative"
# aur ek Pydantic object return karegi.
#
# Example:
# Feedback(sentiment="positive")

classifier_chain = prompt1 | model | parser2


# Conditional chaining ke liye do prompts banaye hain and dono me user ka feedback pass kia hai (LLM ka response pass nahi kia hai because LLM ka response ka ti hum use srf pata karne k liye ki konsa chain run krna hai).
# Agar sentiment "positive" aata hai, to prompt2 run hoga.
# Agar sentiment "negative" aata hai, to prompt3 run hoga.

prompt2 = PromptTemplate(
    template='''
    Write an appropriate response to this positive feedback:

    {feedback}
    ''',
    input_variables=['feedback'],
)


prompt3 = PromptTemplate(
    template='''
    Write an appropriate response to this negative feedback:

    {feedback}
    ''',
    input_variables=['feedback'],
)


# Ye conditional chaining ka main part hai.
#
# Agar classifier_chain ka LLM response me sentiment "positive" hai,
# to pehli chain run hogi.
#
# Agar classifier_chain ka LLM response me sentiment "negative" hai,
# to doosri chain run hogi.
#
# Agar dono conditions false hoti hain,
# to default RunnableLambda run hoga.
branch_chain = RunnableBranch(

    # "x" hamara Pydantic Feedback object hai {sentiment="positive"}.
    # Us object se sentiment extract karke condition check kar rahe hain.
    #
    # Agar sentiment "positive" hai,
    # to positive feedback wali chain run hogi.
    (
        lambda x: x.sentiment == "positive",
        prompt2 | model | parser1
    ),

    # Agar sentiment "negative" hai,
    # to negative feedback wali chain run hogi.

    (
        lambda x: x.sentiment == "negative",
        prompt3 | model | parser1
    ),

    # Default chain:
    # Agar sentiment positive ya negative nahi milta,
    # to ye RunnableLambda execute hoga.
    #
    # Yahan hamare paas actual chain nahi hai,
    # sirf ek normal lambda function hai.
    # RunnableLambda ise Runnable bana deta hai,
    # isliye ise chain ke part ki tarah use kar sakte hain.
    #vese to Default chain should also be a chain
    RunnableLambda(lambda x: "Could not find sentiment")
)


# Pehle classifier_chain feedback ka sentiment identify karegi.
# Uske baad uska output branch_chain mein automatically pass hoga.
#
# Example:
#
# Feedback("This is a terrible phone")
#          ↓
# classifier_chain
#          ↓
# Feedback(sentiment="negative")
#          ↓
# branch_chain
#          ↓
# prompt3 → model → response

chain = classifier_chain | branch_chain


result = chain.invoke({
    "feedback": "This is a terrible phone"
})


print(result)