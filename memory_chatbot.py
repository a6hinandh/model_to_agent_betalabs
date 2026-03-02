import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

# Initialize model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.3
)

# This list will store conversation history
chat_history = []

while True:
    user_input = input("You: ")

    # Add user message to memory
    chat_history.append(HumanMessage(content=user_input))

    # Send full history to model
    response = llm.invoke(chat_history)

    # Add AI response to memory
    chat_history.append(AIMessage(content=response.content))

    print("AI:", response.content)