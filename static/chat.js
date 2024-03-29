let messages = [{"role": "system", "content": "Du bist ein hilfreicher Assistent, antworte auf Deutsch."}];

document.addEventListener('DOMContentLoaded', (event) => {
  addBotMessage('Hallo, wie kann ich helfen?');
});

// Define a global variable to control the streaming process
let stop_stream = false;

document.getElementById("stop_button").addEventListener("click", stopStreaming);

async function stopStreaming() {
  // Set the flag to true to stop streaming
  stop_stream = true;
}

async function streamMessage() {
  const chatInput = document.getElementById("chat_input");
  const userMessage = chatInput.value.trim();

  if (userMessage !== '') {
    messages.push({ role: 'user', content: userMessage });
    addUserMessage(userMessage); // Display the user message in the chat
    chatInput.value = ''; // Clear the input field after sending the message

    toggleButtonVisibility();
    stop_stream = false;
    chatInput.readOnly = true;



    // Instantly add a bot message template to be filled with streamed content
    const botMessageElement = addBotMessage(''); // Initially empty
    let accumulatedResponse = ''; // Variable to accumulate the streamed response

    try {
      const response = await fetch('/stream', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(messages)
      });

      if (!response.body) {
        throw new Error('Failed to get a readable stream from the response');
      }

      const reader = response.body.getReader();

      while (true) {
        
        const { done, value } = await reader.read();
        if (done || stop_stream) {
          // After finishing the streaming, update the messages array and log it
          messages.push({ role: 'assistant', content: accumulatedResponse });
          console.log('Stream finished, messages array:', messages);
          toggleButtonVisibility();
          chatInput.readOnly = false;


          break;
        }
        const text = new TextDecoder().decode(value);
        // Append the streamed text directly to the bot message element
        botMessageElement.textContent += text;
        accumulatedResponse += text; // Accumulate the response
        scrollToBottom();
      }
    } catch (error) {
      console.error('Streaming failed:', error);
      botMessageElement.textContent = `Error occurred: ${error.message}`;
      // Even in case of error, consider adding an error message to the array
      messages.push({ role: 'assistant', content: `Error occurred: ${error.message}` });
    }
  }
}

function clearChatAndMessage() {
  console.log("Clearing chat and message content");
  const chatInput = document.getElementById("chat_input");
  chatInput.value = '';

  const messagesContainer = document.getElementById("chat_messages");
  messagesContainer.innerHTML = ''; // Clear all messages from the chat
  
  // Reset messages array to only include the system message again
  messages.length = 0; // Clear the array
  messages.push({"role": "system", "content": "Du bist ein hilfreicher Assistent, antworte auf Deutsch."});
  
  // Add the initial bot message again
  addBotMessage('Hallo, wie kann ich helfen?');
}

function toggleButtonVisibility() {
  const chatButton = document.getElementById("chat_button");
  const stopButton = document.getElementById("stop_button");

  chatButton.classList.toggle("hidden");
  stopButton.classList.toggle("hidden");
 
}




function addBotMessage(text) {
  const template = document.getElementById('bot-message-template').content.cloneNode(true);
  const contentElement = template.querySelector('.content');
  contentElement.textContent = text;
  document.getElementById('chat_messages').appendChild(template);
  return contentElement; // Return the element that will contain the bot message text
}


function addUserMessage(text) {
  const template = document.getElementById('user-message-template').content.cloneNode(true);
  template.querySelector('.content').textContent = text;
  document.getElementById('chat_messages').appendChild(template);
  scrollToBottom();
}

document.getElementById("chat_button").addEventListener("click", streamMessage);

document.getElementById("chat_input").addEventListener("keydown", function(event) {
  if ((event.metaKey || event.ctrlKey) && event.key === "Enter") {
    event.preventDefault();
    streamMessage();
  }
});

function scrollToBottom() {
  setTimeout(() => {
    const chatMessages = document.getElementById("chat_messages");
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }, 0); // Verzögerung von 0 ms, was den Effekt hat, die Ausführung bis nach dem Rendering zu verzögern
}



document.getElementById("reset_button").addEventListener("click", clearChatAndMessage);
