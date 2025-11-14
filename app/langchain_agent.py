import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

prompt_template = PromptTemplate(
    input_variables=["repo_url", "code_bundle"],
    template="""
You are a senior AI code reviewer.

This code comes from GitHub repository: {repo_url}

Your task:
- Analyze the overall architecture and file structure.
- Identify good practices and areas for improvement.
- Detect dead code, anti-patterns, or poor organization.
- Suggest meaningful refactoring and clean-up strategies.

Code:
{code_bundle}

Format response in English with clear sections:
✅ Strengths  
❌ Weaknesses  
🧠 Architecture Notes  
🧹 Dead Code  
🛠️ Refactoring Suggestions
"""
)

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.5,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

def review_full_repo_langchain(repo_url, code_bundle):
    prompt = prompt_template.format(repo_url=repo_url, code_bundle=code_bundle)
    return llm.invoke(prompt).content