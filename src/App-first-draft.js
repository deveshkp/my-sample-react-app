import React, { useState } from "react";

function App() {
  const [inputText, setInputText] = useState("");
  const [outputText, setOutputText] = useState("");

  const handleInputChange = (event) => {
    setInputText(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    setOutputText(inputText);
    setInputText("");
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
          <button type="submit" style={{marginTop: '10px', padding: '10px 20px', background: 'blue', color: 'white', border: 'none', borderRadius: '5px', fontSize: '16px'}}>Submit</button>
        </form>
      </div>
      <div style={{width: '50%', textAlign: 'center', fontSize: '16px'}}>{outputText}</div>
    </div>
  );
}

export default App;
