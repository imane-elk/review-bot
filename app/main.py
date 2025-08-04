
import os
import re
import subprocess
import tempfile
from flask import Flask, request, jsonify, send_file
from langchain_agent import review_full_repo_langchain
import markdown2
import pdfkit

app = Flask(__name__)
report_pdf_path = "report.pdf"  # 📍 Fichier PDF fixe

def extract_modified_files(review_text):
    pattern = r"### File: (.*?)\\n```python\\n(.*?)```"
    matches = re.findall(pattern, review_text, re.DOTALL)
    return {filename.strip(): code.strip() for filename, code in matches}

@app.route('/review-full', methods=['POST'])
def review_full():
    data = request.get_json()
    repo_url = data.get("repo_url")
    if not repo_url:
        return jsonify({"error": "Missing repo_url"}), 400

    token = os.getenv("GITHUB_TOKEN")
    if token:
        repo_url = repo_url.replace("https://github.com/", f"https://{token}@github.com/")

    try:
        with tempfile.TemporaryDirectory() as repo_path:
            subprocess.run(["git", "clone", repo_url, repo_path], check=True)

            all_code = ""
            for root, _, files in os.walk(repo_path):
                for file in files:
                    if file.endswith(".py"):
                        path = os.path.join(root, file)
                        try:
                            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                                content = f.read()
                                all_code += f"\n# File: {os.path.relpath(path, repo_path)}\n{content}"
                        except Exception as e:
                            print(f"⚠️ Error reading {path}: {e}")

            review_text = review_full_repo_langchain(repo_url, all_code)
            modified_files = extract_modified_files(review_text)

            for filename, code in modified_files.items():
                full_path = os.path.join(repo_path, filename)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, "w", encoding="utf-8") as f:
                    f.write(code)

            subprocess.run(["git", "-C", repo_path, "config", "user.email", "bot@example.com"])
            subprocess.run(["git", "-C", repo_path, "config", "user.name", "ReviewBot"])
            subprocess.run(["git", "-C", repo_path, "add", "."])
            subprocess.run(["git", "-C", repo_path, "commit", "-m", "Auto-refactor from Gemini"])
            subprocess.run(["git", "-C", repo_path, "push", "origin", "main"])

            # ✨ Génère le rapport PDF
            html_report = markdown2.markdown(review_text)
            config = pdfkit.configuration(
    wkhtmltopdf=r"C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"
)

            pdfkit.from_string(html_report, report_pdf_path, configuration=config)


            return jsonify({
                "review": review_text,
                "modified_files": list(modified_files.keys()),
                "pdf_report_url": "/download-report"
            })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download-report', methods=['GET'])
def download_report():
    return send_file(report_pdf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(port=5001, debug=True)