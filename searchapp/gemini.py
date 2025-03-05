# import os
# from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.schema import HumanMessage

# load_dotenv()
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# def process_query(query_text):
#     try:
#         llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=GEMINI_API_KEY)
#         response = llm.invoke([HumanMessage(content=query_text)])
#         return response.content
#     except Exception as e:
#         return f"Error: {str(e)}"

import os
import re
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def clean_ai_response(response_text):
    """
    Cleans and formats AI response by removing unnecessary markdown-style formatting.
    """
    # Remove bold (**text**) and asterisks
    response_text = re.sub(r"\*\*(.*?)\*\*", r"\1", response_text)  # **Bold** → Normal text
    response_text = response_text.replace("*", "")  # Remove extra asterisks
    response_text = re.sub(r"(\n){2,}", "\n", response_text)  # Remove excessive newlines

    return response_text.strip()

def process_query(query_text):
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=GEMINI_API_KEY)
        response = llm.invoke([HumanMessage(content=query_text)])
        
        # Clean and format the AI response
        formatted_response = clean_ai_response(response.content)

        return formatted_response
    except Exception as e:
        return f"Error: {str(e)}"
