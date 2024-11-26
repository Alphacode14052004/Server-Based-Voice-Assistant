// Get references to the DOM elements
const textInput = document.getElementById('textInput');
const speakButton = document.getElementById('speakButton');

// Function to convert text to speech
function textToSpeech() {
  // Get the text input
  const text = textInput.value;

  // Check if the browser supports the SpeechSynthesis API
  if ('speechSynthesis' in window) {
    // Create a new instance of SpeechSynthesisUtterance
    const speech = new SpeechSynthesisUtterance(text);

    // Optionally, set voice properties
    speech.lang = 'en-US'; // Set language
    speech.pitch = 1;      // Set pitch (range: 0-2)
    speech.rate = 1;       // Set speed (range: 0.1-10)
    speech.volume = 1;     // Set volume (range: 0-1)

    // Speak the text
    window.speechSynthesis.speak(speech);
  } else {
    alert('Sorry, your browser does not support text-to-speech!');
  }
}

// Add an event listener to the button
speakButton.addEventListener('click', textToSpeech);
