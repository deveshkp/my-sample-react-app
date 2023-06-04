#  Data Masking Platform

This is a React app for the  Data Masking Platform. It provides a user interface to interact with a backend service that masks sensitive data in text.

## Features

- Enter text to be processed and masked.
- Submit the text to the backend service for processing.
- Display the masked output text.
- Handle error cases gracefully.

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/your/repository.git
   ```

2. Navigate to the project directory:

   ```
   cd project-directory
   ```

3. Install the dependencies:

   ```
   npm install
   ```

## Usage

1. Start the development server:

   ```
   npm start
   ```

2. Access the app in your browser at `http://localhost:3000`.

3. Enter the text you want to process in the input field.

4. Click the "Submit" button to send the text to the backend service for processing.

5. The processed and masked output will be displayed below the input field.

## Configuration

The app is configured to send requests to the backend service at `http://127.0.0.1:5000/process_text`. If your backend service is running on a different URL, you can modify the endpoint in the `handleSubmit` function of the `App` component.

## Technologies Used

- React: JavaScript library for building user interfaces.
- Axios: Promise-based HTTP client for making API requests.

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

ner model code -  Here's an explanation of the code:

1. The code begins by importing the necessary libraries: `csv` for reading training data from a CSV file, `spacy` for natural language processing, `random` for shuffling the training data, and `Example` from `spacy.training.example` for creating training examples.

2. The function `offsets_to_biluo_tags` converts the entity offsets to a list of BIO (beginning-inside-outside) tags. It takes a spaCy `doc` object and a list of `entities` as input and returns a list of tags.

3. The function `train_ner_model` trains a named entity recognition (NER) model using the provided training data. It takes `training_data` as input, which is a list of tuples containing the full text, masked text, entity spans, and other information.

   - It initializes a blank NER model using `spacy.blank("en")`.
   - It adds the NER component to the pipeline of the model.
   - It extracts the unique entity labels from the training data and adds them as labels in the NER component.
   - It prepares the training data in spaCy format by converting the entity spans to the required format.
   - It trains the NER model using the FastText algorithm for a specified number of iterations.
   - Finally, it returns the trained NER model.

4. The code reads the training data from a CSV file named `data.csv` and stores it in the `training_data` list. The CSV file should have columns for full text, masked text, entity spans, PII (Personally Identifiable Information) entities, and other entities.

5. The `train_ner_model` function is called with the `training_data` to obtain the trained NER model.

6. The trained NER model is saved to disk using the `to_disk` method, and it is stored in a directory named `ner_model`.

7. The code tests the NER model on a sample text by creating a spaCy `doc` object using the `ner_model` and the sample text.

8. The `masked_text` variable is initialized with the sample text. Then, for each entity (`ent`) in the `doc.ents`, the corresponding entity text is replaced with the string "{{MASKED}}".

9. Finally, the `masked_text` is printed, which contains the sample text with the identified entities replaced by "{{MASKED}}".

This code trains a NER model using the provided training data and demonstrates its usage by masking the entities in a sample text.
