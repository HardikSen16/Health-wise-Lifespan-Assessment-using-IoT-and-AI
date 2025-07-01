window.addEventListener("DOMContentLoaded", () => {
  const prediction = sessionStorage.getItem("prediction");
  const initialMessage = sessionStorage.getItem("initial_message");

  if (prediction) {
      document.getElementById("predictionBox").innerText = `Predicted Life Expectancy: ${prediction} years`;
  }

  if (initialMessage) {
      let chatBox = document.getElementById("chatBox");
      let botMessage = document.createElement("div");
      botMessage.classList.add("message", "bot-message");

      // Optional: format using `marked` if needed
      const formattedMessage = marked.parse(initialMessage);

      botMessage.innerHTML = `<strong>ChatBot:</strong><br>${formattedMessage}`;
      chatBox.appendChild(botMessage);
  }
});


// Function to send message
function sendMessage() {
    let userInput = document.getElementById("userInput");
    let message = userInput.value.trim();
    if (message === "") return; // Prevent empty messages

    let chatBox = document.getElementById("chatBox");

    // Append User Message
    let userMessage = document.createElement("div");
    userMessage.classList.add("message", "user-message");
    userMessage.innerHTML = `<strong>You:</strong> ${message}`;
    chatBox.appendChild(userMessage);

    userInput.value = ""; // Clear input
    chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll down

    // Send user message to backend (replace with actual backend API call)
    fetch('http://127.0.0.1:8000/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ user_input: message })  // ✅ correct key and value
    })
    .then(response => response.json())
    .then(data => {
      const botReply = data.chatbot_response;
  
      let botMessage = document.createElement("div");
      botMessage.classList.add("message", "bot-message");
  
      // Use marked to convert Markdown to HTML
      const formattedReply = marked.parse(botReply);
  
      botMessage.innerHTML = `<strong>ChatBot:</strong><br>${formattedReply}`;
      chatBox.appendChild(botMessage);
      chatBox.scrollTop = chatBox.scrollHeight;
  })
  
    .catch(error => console.error('Error:', error));
          
    
}

// Function to allow sending messages with Enter key
function handleKeyPress(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}

// Run on page load
getPrediction();
