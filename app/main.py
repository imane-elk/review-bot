import os
from flask import Flask, request, jsonify
from langchain_agent import review_full_repo_langchain
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)

@app.route('/review-full', methods=['POST'])
def review_full():
    data = request.get_json()
    print("📥 Reçu depuis n8n :", data)

    # Vérification des paramètres obligatoires
    required_params = ["repo_owner", "repo_name", "pr_number"]
    missing = [p for p in required_params if not data.get(p)]

    if missing:
        return jsonify({"error": f"Paramètres manquants: {', '.join(missing)}"}), 400

    # Construction de l’URL du repo
    repo_url = f"https://github.com/{data['repo_owner']}/{data['repo_name']}.git"

    try:
        comment = review_full_repo_langchain(repo_url)

        return jsonify({
            "repo_owner": data["repo_owner"],
            "repo_name": data["repo_name"],
            "pr_number": data["pr_number"],
            "comment": comment
        })
    except Exception as e:
        print("❌ Erreur dans review_full :", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
