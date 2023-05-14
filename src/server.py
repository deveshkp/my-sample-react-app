from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, allow_headers=["Content-Type", "Authorization"])

@app.route('/process_text', methods=['POST'])    
def process_text():
    input_text = request.json['input_text']
    output_text = input_text.upper()  # replace this with your actual ML model processing logic
    response = {'output_text': output_text}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
