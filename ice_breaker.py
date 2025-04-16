from langchain_core.prompts import PromptTemplate
#from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
#from langchain_google_vertexai import VertexAI
#from vertexai import init

from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv

from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent

def ice_break_with(name: str) -> str:
    linkedin_url = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_url)

    summary_template = """
          given the LinkedIn information {information} about a person from I want you to create:
          1. a short summary
          2. two interesting facts about them
     """
    
    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    llm = ChatGoogleGenerativeAI(model="models/gemini-2.0-flash", temperature=0.7)
    #llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    #llm = ChatOllama(model="mistral")
    #llm = ChatOllama(model="llama3.2")
    #llm = ChatOllama(model="gemma")
    #llm = VertexAI(model_name="gemini-pro")

    chain = summary_prompt_template | llm | StrOutputParser()

    res = chain.invoke(input={"information": linkedin_data})

    print(res)

if __name__ == "__main__":
    load_dotenv()
    print("Ice Breaker Enter")
    ice_break_with(name="Moussa Aouinane")