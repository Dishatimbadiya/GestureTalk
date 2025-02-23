import React, { useRef, useEffect } from "react";
import Webcam from "react-webcam";
import axios from "axios";

const WebcamCapture = ({ setRecognizedText }) => {
    const webcamRef = useRef(null);

    useEffect(() => {
        const interval = setInterval(async () => {
            if (webcamRef.current) {
                const imageSrc = webcamRef.current.getScreenshot();
                if (imageSrc) {
                    try {
                        const response = await axios.post("http://127.0.0.1:5000/predict", { image: imageSrc });
                        setRecognizedText(response.data.gesture);
                    } catch (error) {
                        console.error("Error sending image to backend:", error);
                    }
                }
            }
        }, 500); // Adjust frame capture interval (every 500ms)

        return () => clearInterval(interval); // Cleanup on unmount
    }, [setRecognizedText]);

    return (
        <div>
            <Webcam
                audio={false}
                ref={webcamRef}
                screenshotFormat="image/jpeg"
                width={400}
                height={300}
            />
        </div>
    );
};

export default WebcamCapture;
