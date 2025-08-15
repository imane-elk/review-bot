import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
load_dotenv()

# Récupération clé API Google
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("❌ La clé GOOGLE_API_KEY est manquante. Définis-la avant de lancer le script.")

# Initialisation du modèle Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.5,
    google_api_key=GOOGLE_API_KEY
)

def review_full_repo_langchain(repo_url: str) -> str:
    """
    Analyse complète d’un repository GitHub via Gemini.
    """
    print(f"🔍 Analyse du repo : {repo_url}")

    prompt_template = PromptTemplate(
        input_variables=["repo_url"],
        template="""
Tu es un expert en revue de code.
Analyse le repository suivant : {repo_url}

Fournis un rapport clair avec :
- Évaluation générale
- Points forts
- Problèmes détectés
- Améliorations suggérées
        """
    )

    try:
        prompt = prompt_template.format(repo_url=repo_url)
        response = llm.invoke(prompt)
        return response.content.strip()
    except Exception as e:
        print("❌ Erreur pendant l'appel LLM :", str(e))
        return "⚠ La génération de la review a échoué ou est vide."
