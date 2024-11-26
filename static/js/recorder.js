const startButton = document.getElementById("start");
const stopButton = document.getElementById("stop");
const statusText = document.getElementById("status");
const transcriptionText = document.getElementById("transcription");
let mediaRecorder;
let audioChunks = [];

// Function to read text aloud using Web Speech API
function readTextAloud(text) {
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = 'en-US'; // Set the language as per your requirement
  utterance.rate = 1; // Adjust the speed (0.1 to 10)
  utterance.pitch = 1; // Adjust the pitch (0 to 2)
  window.speechSynthesis.speak(utterance);
}

startButton.onclick = async () => {
  startButton.disabled = true;
  stopButton.disabled = false;
  transcriptionText.textContent = "";

  // Get audio stream from user's microphone
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  mediaRecorder = new MediaRecorder(stream);

  // Store recorded audio data chunks
  mediaRecorder.ondataavailable = event => {
    audioChunks.push(event.data);
  };

  // When recording stops, send the audio to the server
  mediaRecorder.onstop = async () => {
    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
    const formData = new FormData();
    formData.append('audio', audioBlob, 'recording.wav');

    // Send the audio file to the Flask server
    statusText.textContent = "Uploading audio...";
    try {
      const response = await fetch('/upload', {
        method: 'POST',
        body: formData
      });

      if (response.ok) {
        const result = await response.json();
        const transcription = result.answer || "No response generated";
        
        statusText.textContent = "Audio uploaded and processed successfully!";
        transcriptionText.textContent = transcription; // Display the transcription

        // Read the transcription out loud
        readTextAloud(transcription);

      } else {
        statusText.textContent = "Failed to upload and process audio.";
      }
    } catch (error) {
      console.error("Error uploading audio:", error);
      statusText.textContent = "An error occurred during upload.";
    }

    audioChunks = []; // Reset the audio chunks
  };

  // Start recording
  mediaRecorder.start();
  statusText.textContent = "Recording...";
};

stopButton.onclick = () => {
  startButton.disabled = false;
  stopButton.disabled = true;
  mediaRecorder.stop();
  statusText.textContent = "Stopped recording.";
};
