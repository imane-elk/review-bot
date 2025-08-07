import os
import shutil
import subprocess
import logging
from flask import Flask, request, jsonify
from langchain_agent import review_full_repo_langchain  # Import direct
from urllib.parse import urlparse

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/review-full', methods=['POST'])
def review_full():
    data = request.json
    repo_url = data.get("repo_url", "").strip()

    # Vérification basique de l'URL
    if not repo_url or not repo_url.startswith("http"):
        return jsonify({"error": "Invalid or missing repo_url"}), 400

    try:
        # Définir un chemin temporaire basé sur le nom du repo
        parsed_url = urlparse(repo_url)
        repo_name = os.path.basename(parsed_url.path).replace(".git", "")
        repo_path = f"/tmp/review-repo-{repo_name}"

        # Nettoyer si le dossier existe déjà
        if os.path.exists(repo_path):
            shutil.rmtree(repo_path)

        # Cloner le repo
        logging.info(f"Cloning repo from {repo_url}")
        subprocess.run(["git", "clone", repo_url, repo_path], check=True)

        # Lecture des fichiers Python
        all_code = ""
        for root, _, files in os.walk(repo_path):
            for file in files:
                if file.endswith(".py"):
                    path = os.path.join(root, file)
                    try:
                        with open(path, "r", encoding="utf-8") as f:
                            rel_path = os.path.relpath(path, repo_path)
                            all_code += f"\n# File: {rel_path}\n" + f.read()
                    except Exception as e:
                        logging.warning(f"Erreur de lecture pour {path}: {e}")

        # Appel de l'agent LangChain
        logging.info("Calling LangChain agent")
        result = review_full_repo_langchain(repo_url, all_code)

        return jsonify({"review": result})

    except subprocess.CalledProcessError as e:
        logging.error(f"Erreur lors du clonage du repo: {e}")
        return jsonify({"error": "Git clone failed"}), 500

    except Exception as e:
        logging.error(f"Erreur générale: {e}")
        return jsonify({"error": "Internal server error"}), 500

    finally:
        # Nettoyage (optionnel, tu peux commenter si tu veux garder le dossier)
        if os.path.exists(repo_path):
            shutil.rmtree(repo_path)

if __name__ == '__main__':
    app.run(port=5001, debug=True)
