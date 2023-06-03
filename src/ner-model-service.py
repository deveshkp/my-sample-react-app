from flask import Flask, request, jsonify
import spacy

app = Flask(__name__)

# Load the NER model
ner_model = spacy.load('ner_model')

@app.route('/mask', methods=['POST'])
def mask_text():
    data = request.get_json()
    text = data['text']

    # Apply the NER model to mask entities in the text
    doc = ner_model(text)

    masked_text = text
    for ent in doc.ents:
        masked_text = masked_text.replace(ent.text, "{{MASKED}}")

    response = {'masked_text': masked_text}
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
