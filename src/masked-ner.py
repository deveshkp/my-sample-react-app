import csv
import spacy
import random
from spacy.training.example import Example

def offsets_to_biluo_tags(doc, entities):
    tags = ['O'] * len(doc)
    for entity in entities:
        start = entity['start_position']
        end = entity['end_position']
        entity_type = entity['entity_type']
        tags[start] = f"B-{entity_type}"
        for i in range(start + 1, end):
            tags[i] = f"I-{entity_type}"
    return tags

def train_ner_model(training_data):
    # Create blank NER model
    ner_model = spacy.blank("en")

    # Add NER component to the pipeline
    ner = ner_model.add_pipe("ner")

    # Define the labels for the NER model
    labels = set()
    for _, _, spans, _, _ in training_data:
        entities = eval(spans)
        for entity in entities:
            labels.add(entity['entity_type'])

    for label in labels:
        ner.add_label(label)

    # Prepare the training data in spaCy format
    formatted_data = []
    for text, _, spans, _, _ in training_data:
        entities = eval(spans)
        entities_formatted = []
        for entity in entities:
            start = entity['start_position']
            end = entity['end_position']
            entity_type = entity['entity_type']
            entities_formatted.append((start, end, entity_type))
        formatted_data.append((text, {"entities": entities_formatted}))

    # Train the NER model using the FastText algorithm
    optimizer = ner_model.initialize()
    for iteration in range(10):
        random.shuffle(formatted_data)
        for text, annotations in formatted_data:
            example = Example.from_dict(ner_model.make_doc(text), annotations)
            ner.update([example], sgd=optimizer)

    return ner_model

# Read the training data from CSV
training_data = []
with open('data.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        full_text = row['full_text']
        masked = row['masked']
        spans = row['spans']
        pii_entities = row['pii_entities'] if 'pii_entities' in row else '[]'
        other_entities = row['other_entities'] if 'other_entities' in row else '[]'
        training_data.append((full_text, masked, spans, pii_entities, other_entities))

# Train the NER model
ner_model = train_ner_model(training_data)

# Save the NER model
ner_model.to_disk('ner_model')

# Test the NER model on a sample text
sample_text = "The address of Persint is 6750 Koskikatu 25 Apt. 864, CO Uruguay 64677"
doc = ner_model(sample_text)

masked_text = sample_text
for ent in doc.ents:
    masked_text = masked_text.replace(ent.text, "{{MASKED}}")

print(masked_text)
