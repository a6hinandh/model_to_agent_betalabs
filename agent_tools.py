import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

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
            "You are an AI assistant with memory and access to web search. "
            "Use conversation memory for personal questions. "
            "Use web search only for factual, news, sports, or current events."
        )
    )
]

def web_search(query):
    print("🔎 Using web search...")
    result = tavily.search(query=query, max_results=2)
    return result["results"][0]["content"]


# simple decision logic
def needs_search(query):
    keywords = [
        "latest", "news", "current", "today",
        "score", "match", "who won", "weather",
        "president", "prime minister"
    ]
    query_lower = query.lower()
    return any(word in query_lower for word in keywords)


while True:
    user_input = input("You: ")

    chat_history.append(HumanMessage(content=user_input))

    if needs_search(user_input):
        search_result = web_search(user_input)

        chat_history.append(
            HumanMessage(content=f"Web search result: {search_result}")
        )

    response = llm.invoke(chat_history)

    answer = response.content

    chat_history.append(AIMessage(content=answer))

    print("AI:", answer)