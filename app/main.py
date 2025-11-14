import os
import shutil
import subprocess
from flask import Flask, request, jsonify
from langchain_agent import review_full_repo_langchain  # Import direct

app = Flask(__name__)

@app.route('/review-full', methods=['POST'])
def review_full():
    data = request.json
    repo_url = data.get("repo_url", "")

    if not repo_url:
        return jsonify({"error": "Missing repo_url"}), 400

    # Chemin temporaire pour cloner le repo
    repo_path = "/tmp/review-repo"
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)
    subprocess.run(["git", "clone", repo_url, repo_path], check=True)

    # Lecture des fichiers Python
    all_code = ""
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    all_code += f"\n# File: " + os.path.relpath(path, repo_path) + "\n" + f.read()

    # Appel du module LangChain
    result = review_full_repo_langchain(repo_url, all_code)
    return jsonify({"review": result})

if __name__ == '__main__':
    app.run(port=5001, debug=False)
