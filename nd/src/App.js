import logo from './logo.svg';
import './App.css';
import WebcamCapture from "./Components/WebcamCapture";

import React, { useState } from "react";


function App() {
  const [recognizedText, setRecognizedText] = useState("Waiting for recognition...");
  
  return (
    <div className="App">
 <div style={{ textAlign: "center", padding: "20px" }}>
            <h1>Real-Time Sign Language Detection</h1>
            <WebcamCapture setRecognizedText={setRecognizedText} />
            <h2>Detected Gesture:</h2>
            <p>{recognizedText}</p>
        </div>
    </div>
  );
}

export default App;
