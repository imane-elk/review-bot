import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# Crée le prompt
prompt_template = PromptTemplate(
    input_variables=["title", "body", "diff"],
    template="""
You are a senior AI code reviewer.

Here is a GitHub Pull Request to review:

Title: {title}
Description: {body}
Code diff:
{diff}

Your task:
- Perform an in-depth analysis of the code: explain what is good, what could be improved, and why.
- Check if there is any **dead code** (code that will never run, is unused, or redundant). If yes, clearly explain why and suggest removing it.
- Pay attention to:
    - Code structure
    - Naming conventions
    - Separation of concerns
    - Class structure and dependencies (if any)
    - Respect of programming language or framework best practices
- If problems exist, suggest corrected or refactored code snippets with detailed justification.
- Always justify every point with examples when possible.

Format your answer in English with clear sections:
- ✅ Strengths (with justification)
- ❌ Weaknesses (with explanation)
- 💡 Suggestions for improvement
- 🧹 Dead Code (if detected, explain why)
- 🛠️ Refactored Code (if applicable)
"""

)
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.5,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

def review_with_langchain(title, body, diff):
    final_prompt = prompt_template.format(title=title, body=body, diff=diff)
    return llm.invoke(final_prompt).content
