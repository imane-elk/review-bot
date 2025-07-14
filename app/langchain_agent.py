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
- Provide a clear and structured review: What is good, what is bad, and why.
- If there are any problems, **suggest a corrected version or a refactored snippet**.
- Be brief but helpful.
Format your answer with clear sections: Good, Bad, Suggestions, and Example Fix (if applicable).
"""
)


# Crée le LLM Gemini avec clé manuelle
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0.5,
    google_api_key=os.getenv("GOOGLE_API_KEY")  # ✅ important
)

def review_with_langchain(title, body, diff):
    final_prompt = prompt_template.format(title=title, body=body, diff=diff)
    return llm.invoke(final_prompt).content
