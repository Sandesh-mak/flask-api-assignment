from flask import Flask, request, jsonify

app = Flask(__name__)

# 3 Unique API Keys for RootSoftware Testers
API_KEYS = {
    "key_consumer_alpha_8f9a2b1c4d": "Tester 1 (Alpha)",
    "key_consumer_beta_7e3f1a9c8b": "Tester 2 (Beta)",
    "key_consumer_gamma_5d2e4c6b1a": "Tester 3 (Gamma)"
}

@app.route('/process', methods=['POST'])
def process_text():
    api_key = request.headers.get("X-API-Key")
    
    if not api_key:
        return jsonify({"error": "Unauthorized: Missing X-API-Key header"}), 401
    if api_key not in API_KEYS:
        return jsonify({"error": "Unauthorized: Invalid API Key"}), 401
    
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "Bad Request: Missing 'text' field"}), 400
    
    return jsonify({
        "consumer": API_KEYS[api_key],
        "original_text": data['text'],
        "processed_text": data['text'].upper(),
        "status": "Success"
    }), 200

if __name__ == '__main__':
    print("==========================================")
    print(">>> TASK 2 ROOTSOFTWARE SERVER RUNNING <<<")
    print("==========================================")
    app.run(debug=True, port=5000)