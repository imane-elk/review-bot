import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_agent import review_with_langchain

# Charger la clé API depuis le fichier .env
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Fonction principale : revue de code avec Gemini 1.5 Flash
def review_code(title, body, diff):
    prompt = f"""
You are a senior software engineer reviewing a GitHub pull request.
Title: {title}
Description: {body}
Code Diff:
{diff}

Give a clear code review: what is good, what could be improved, and why.
Use bullet points.
"""
    # Utilisation de Gemini 1.5 Flash
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text


# Fonction alternative : revue avec LangChain (optionnelle)
def review_code_langchain(title, body, diff):
    from langchain_agent import review_with_langchain
    return review_with_langchain(title, body, diff)
