import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

prompt_template = PromptTemplate(
    input_variables=["repo_url", "code_bundle"],
    template="""
You are a senior AI code reviewer and refactoring assistant.

Repository URL: {repo_url}

You have full access to the source code files provided from this repository.

Your responsibilities:
- Review all files included in the input below. Do not limit your analysis to a few files — analyze each file individually and in the context of the overall architecture.
- Evaluate design decisions, consistency, structure, and separation of concerns across modules.
- Detect bad practices, duplicated logic, anti-patterns, and dead code.
- Suggest meaningful and actionable improvements.
- If any file requires modification, return the full corrected version of that file with improvements applied.

📄 When returning code modifications, use the following format:
### File: filename.py
```python
# updated code
Format your response in English with the following sections:
✅ Strengths  
❌ Weaknesses  
🧠 Architecture Notes  
🧹 Dead Code  
🛠️ Refactoring Suggestions  
📄 Modified Files  
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