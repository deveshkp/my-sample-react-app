import csv
import transformers
import torch
from transformers import BertTokenizer, BertForTokenClassification

def train_ner_model(training_data):
    # Load BERT tokenizer and model
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertForTokenClassification.from_pretrained('bert-base-uncased')

    # Set up optimizer
    optimizer = transformers.AdamW(model.parameters())

    # Prepare the training data
    formatted_data = []
    for text, _, spans, _, _ in training_data:
        entities = eval(spans)
        tokens = tokenizer.tokenize(text)
        tags = ['O'] * len(tokens)
        for entity in entities:
            start = entity['start_position']
            end = entity['end_position']
            entity_type = entity['entity_type']
            tags[start] = f"B-{entity_type}"
            for i in range(start + 1, end):
                tags[i] = f"I-{entity_type}"
        encoded_input = tokenizer.encode_plus(tokens, add_special_tokens=True, padding='longest', truncation=True, return_tensors='pt')
        input_ids = encoded_input['input_ids']
        attention_mask = encoded_input['attention_mask']
        labels = torch.tensor([tokenizer.encode(tags, add_special_tokens=False, truncation=True, max_length=len(tokens))])
        formatted_data.append((input_ids, attention_mask, labels))

    # Train the NER model using BERT
    model.train()
    for epoch in range(10):
        random.shuffle(formatted_data)
        for input_ids, attention_mask, labels in formatted_data:
            optimizer.zero_grad()
            outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
            loss = outputs.loss
            loss.backward()
            optimizer.step()

    return model


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
ner_model.save_pretrained('ner_model')

# Test the NER model on a sample text
sample_text = "The address of Persint is 6750 Koskikatu 25 Apt. 864, CO Uruguay 64677"
tokens = tokenizer.tokenize(sample_text)
input_ids = tokenizer.encode(sample_text, add_special_tokens=True, truncation=True, max_length=512, padding='longest', return_tensors='pt')
outputs = ner_model(input_ids=input_ids)
predictions = torch.argmax(outputs.logits, dim=2).squeeze().tolist()

masked_text = sample_text
for token, pred in zip(tokens, predictions):
    if pred == 1:  # Replace entity token with MASKED
        masked_text = masked_text.replace(token, "{{MASKED}}")

print(masked_text)
