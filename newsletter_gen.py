from tavily import TavilyClient
from dotenv import load_dotenv
import os
from swarm import Agent,Swarm
from swarm.repl import run_demo_loop


load_dotenv()

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
#print(os.getenv("TAVILY_API_KEY"))  

def search_news(query:str):
    """ 
       Search for news articles on the given query
    """
    try:
        response = tavily_client.search(query)
        print(f"Searching for news on the query: {query}")
        return response["results"]
    except Exception as e:
        print(f"Error fetching News : {e}")
        return []
    
    
    
def write_newsletter(articles):
    print(f"====> got the articles...{articles}")    
    """ Write a newsletter with the given articles/text"""
    
    print("Writing the newsletter...")
    newsletter = ""
    for article in articles:
        newsletter = ""
        for article in articles:
            newsletter += article
    return newsletter


def review_newsletter(newsletter):
    """ Review the newsletter before sending"""
    print("Reviewing the newsletter...")
    return f"Newsletter reviewed successfully!\n{newsletter}"


def transfer_to_search():
    return search_agent



def transfer_to_writer():
    return writer_agent


def transfer_to_editor():
    return editor_agent


search_agent = Agent(
    name="Search Agent",
    instructions="""
        You rae world class search agent (web searcher). You can search for news articles on any topic. your role is to:
        1. Search for most recent news articles on the given query provded by the user.
        2. Retrieve the article title, content, and URL.
        3. Transfer the conversation to the writer agent for drafting the news letter.
        Make sure to handle any errors that may occur during the search, only after finding the artile.
    """,
    functions=[search_news, transfer_to_writer],
)

writer_agent = Agent(
    name="Writing Agent",
    instructions="""
        You are a writer agent. Your role is to:
        1. Take search result and generate a newsletter draft with the given articles/text.
        1. Make sure newsletter includes the title, content, and url of each article.
        2. Transfer the conversation to the editor agent for reviewing the newsletter.
    """,
    functions=[write_newsletter, transfer_to_editor],
)

editor_agent = Agent(
    name="Editor Agent",
    instructions="""
        You are an editor agent. Your role is to:
        1. Review the newsletter before sending.
        2. Transfer the conversation back to the Writing agent if any changes are required.
    """,
    functions=[review_newsletter, transfer_to_writer],
)

triage_agent = Agent(
    name="Triage Agent",
    instructions="""
          Determine which agent is best suited to handle the user's request, and transfer the conversation to that agent.
          if task is to search news, transfer to search agent.
          if task is to write newsletter, transfer to writer agent.
          if task is to review newsletter, transfer to editor agent.
          """,
)

triage_agent.functions = [transfer_to_search, transfer_to_writer, transfer_to_editor]


if __name__ == "__main__":
    #client = Swarm()
    run_demo_loop(triage_agent)

        