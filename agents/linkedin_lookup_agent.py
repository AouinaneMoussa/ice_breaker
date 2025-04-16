import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from dotenv import load_dotenv
load_dotenv()

from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts.prompt import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import (
    create_react_agent,
    AgentExecutor,
)
from langchain import hub
from tools.tools import get_profile_url_tavily

def lookup(name: str) -> str:
    
    #llm = ChatOllama(model="llama3.2")
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.0-flash", temperature=0.7)

    template = """
          given the full name {name_of_person} I want you to get it me a link to their LinkedIn profile page.
          Your answer should contain only a URL"""
    
    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )

    tools_for_agent = [
        Tool(
            name="Crawl Google 4 linkedin profile page",
            func=get_profile_url_tavily,
            description="useful for when you need get the Linkedin Page URL",
        )
    ]

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )

    linked_profile_url = result["output"]
    return linked_profile_url

#if __name__ == "__main__":
    linkedin_url = lookup(name="Aouinane Moussa Devoteam")
    print(linkedin_url)

    