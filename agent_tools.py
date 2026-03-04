import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool

from tavily import TavilyClient

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.3
)

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

chat_history = [
    SystemMessage(
        content=(
            "You are an AI assistant with memory and web search access.\n"
            "For sports results, current events, news, weather, or anything that may change over time, "
            "you MUST use the web_search tool before answering.\n"
            "Do not rely on your internal knowledge for these topics."
        )
    )
]

@tool
def web_search(query: str):
    """Search the web for factual information, news, current events, weather, or sports. Returns the relevant content from the search results."""
    print(f"🔎 Using web search for: {query}")
    try:
        result = tavily.search(query=query, max_results=2)
        if result and result.get("results"):
            formatted_results = []
            for r in result["results"]:
                formatted_results.append(f"Source: {r['url']}\nContent: {r['content']}")
            return "\n\n".join(formatted_results)
        return "No results found for this search."
    except Exception as e:
        return f"Error during web search: {str(e)}"

llm_with_tools = llm.bind_tools([web_search])


while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    chat_history.append(HumanMessage(content=user_input))
    while True:
        response = llm_with_tools.invoke(chat_history)
        chat_history.append(response)

        if not response.tool_calls:
            break

        for tool_call in response.tool_calls:
            if tool_call["name"] == "web_search":
                result = web_search.invoke(tool_call["args"])
                print("TOOL RESULT:", result)
                chat_history.append(ToolMessage(content=str(result), tool_call_id=tool_call["id"]))

    answer = response.content
    if isinstance(answer, list):
        answer = "\n".join([item.get("text", "") if isinstance(item, dict) else str(item) for item in answer])
    
    if not answer:
        answer = "I've processed your request but don't have a direct answer. How can I help further?"
 
    print("AI:", answer)