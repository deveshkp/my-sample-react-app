import React, { useState } from "react";
import axios from "axios";

function App() {
  const [inputText, setInputText] = useState("");
  const [outputText, setOutputText] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const handleInputChange = (event) => {
    setInputText(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsLoading(true);
    setErrorMessage("");

    try {
      const response = await axios.post("http://localhost:5000/process_text", {
        input_text: inputText,
      });
      setOutputText(response.data.output_text);
    } catch (error) {
      setErrorMessage("Error processing text. Please try again.");
    }

    setInputText("");
    setIsLoading(false);
  };

  return (
    <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100vh'}}>
      <h1>Data Weavers - Data Masking Platform</h1>
      <div style={{width: '50%', textAlign: 'center', marginBottom: '20px'}}>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            value={inputText}
            onChange={handleInputChange}
            placeholder="Enter text here..."
            style={{width: '100%', padding: '10px', fontSize: '16px', border: '1px solid #ccc', borderRadius: '5px'}}
          />
          <button type="submit" style={{marginTop: '10px', padding: '10px 20px', background: 'blue', color: 'white', border: 'none', borderRadius: '5px', fontSize: '16px'}}>
            {isLoading ? "Loading..." : "Submit"}
          </button>
        </form>
        {errorMessage && <p style={{color: 'red'}}>{errorMessage}</p>}
      </div>
      <div style={{width: '50%', textAlign: 'center', fontSize: '16px'}}>{outputText}</div>
    </div>
  );
}

export default App;
