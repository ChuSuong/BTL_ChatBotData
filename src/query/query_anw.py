from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import openai
import os


load_dotenv()
openai.api_key = os.getenv("GPT_API_KEY")
llm = OpenAI(temperature=0.3)

prompt = PromptTemplate(
    input_variables=["name"],
    template="Hello, {name}. How can I help you today?"
)

llm_chain = LLMChain(prompt=prompt, llm=llm)

response = llm_chain.run({"name": "Alice"})
print(response)
