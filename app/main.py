from flask import Flask, request, jsonify
from reviewer import review_code

app = Flask(__name__)

@app.route('/review', methods=['POST'])
def review():
    data = request.json
    title = data.get("title", "")
    body = data.get("body", "")
    diff = data.get("diff", "")
    
    if not diff:
        return jsonify({"error": "Missing diff"}), 400

    review_result = review_code(title, body, diff)
    return jsonify({"review": review_result})

if __name__ == '__main__':
    app.run(port=5001, debug=True)
