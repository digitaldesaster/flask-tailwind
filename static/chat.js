
initChatMessages()

function initChatMessages(){
  if (messages.length === 0) {
    messages = [{ "role": "system", "content": systemMessage }];
    document.addEventListener('DOMContentLoaded', (event) => {
      addBotMessage(welcomeMessage);
    });
    document.getElementById('chat_input').focus();
  } else {
    if (use_prompt_template=='True')
      {
        document.addEventListener('DOMContentLoaded', (event) => {
          addBotMessage(welcomeMessage);
        });
        let chat_input_ui = document.getElementById('chat_input');
        chat_input_ui.textContent=messages[1]['content'];
        chat_input_ui.focus();
        messages.splice(1, 1);
        console.log(messages);
      }
    else
    {
      // Use for...of to iterate over the elements of the array directly
    for (const message of messages) {
      // Check if the role of the message is either 'system' or 'assistant'
      if (['system', 'assistant'].includes(message['role'])) {
        const botMessageElement = addBotMessage('');
        appendData(message['content'], botMessageElement)
  
      } else {
        addUserMessage(message['content']);
      }
    }
    document.getElementById('chat_messages').focus();
    }
    
  }
}

function appendData(text, botMessageElement) {
  const parts = text.split("```");
  for (let i = 0; i < parts.length; i++) {
    if (i % 2 === 0) {
      // Check for ###STOP### marker in the non-code part
      const stopIndex = parts[i].indexOf("###STOP###");
      if (stopIndex !== -1) {
        // If ###STOP### is found, process the text before and after it separately
        const textBeforeStop = parts[i].substring(0, stopIndex);
        // Append text before ###STOP### as normal text
        appendNormalText(botMessageElement, textBeforeStop);

        // Convert text after ###STOP### into a JSON array
        let JsonString = parts[i].substring(stopIndex + "###STOP###".length).trim();
        botMessageElement.innerHTML += '<br><span class="text-xs">' + JsonString +'</span';
        // JsonString = JsonString.replace(/'/g, '"');
        // try {
        //   const jsonObject = JSON.parse(JsonString);
        //   appendNormalText(botMessageElement, textBeforeStop);
          
        // } catch (e) {
        //   console.error("Failed to parse JSON", e);
        // }
      } else {
        // If ###STOP### is not found, append it as normal text
        appendNormalText(botMessageElement, parts[i]);
      }
    } else {
      // This part is code, append it within <pre> tags
      appendCodeText(botMessageElement, parts[i]);
    }
  }
}


// Define a global variable to control the streaming process
let stop_stream = false;

document.getElementById("stop_button").addEventListener("click", stopStreaming);


function saveChatData(messages) {
  // Daten für den POST-Request
  const formData = new FormData();
  formData.append('username', username);
  formData.append('chat_started', chat_started);
  formData.append('messages', JSON.stringify(messages));

  // Dynamische Generierung des API-Endpunkts aus der aktuellen URL
  const url = `${window.location.origin}/save_chat`;

  // POST-Request an den API-Endpunkt senden
  fetch(url, {
    method: 'POST',
    body: formData,
  })
    .then(response => {
      if (response.ok) {
        console.log("api call successful");
      }
      return response.text();
    })
    .then(data => {
      console.log(data); // Logge die Antwort des Servers
    })
    .catch(error => {
      console.error('Fehler beim Senden des Requests:', error);
    });
}

async function stopStreaming() {
  // Set the flag to true to stop streaming
  stop_stream = true;
}

// Function to append normal text
function appendNormalText(container, text) {
  const textNode = document.createTextNode(text);
  container.appendChild(textNode);
}

function appendCodeText(container, text) {
  // Get the template and clone its content
  const template = document.getElementById('code_template').content.cloneNode(true);

  const lines = text.split('\n');
  const language = lines[0].trim(); // Get the language info from the first line
  console.log(`Code block language: ${language}`); // Log the language info

  // Remove the first line (language info) and join the rest back into a single string
  const codeWithoutLanguageInfo = lines.slice(1).join('\n').trim();

  // Set the text content of the pre element
  const preElement = template.querySelector('pre');
  preElement.textContent = codeWithoutLanguageInfo;

  // Append the filled template to the specified container
  const importedNode = document.importNode(template, true);

  if (language) { // Check if the language string is not empty
    const languageInfoElement = importedNode.querySelector('.language-info');
    languageInfoElement.textContent = `${language}`; // Set the language info
  }

  // IMPORTANT: Add the event listener to the COPY button of this specific instance BEFORE appending to the container
  const copyButton = importedNode.querySelector('.copy-btn');
  const copiedInfo = importedNode.querySelector('.copied');
  copyButton.onclick = (event) => { // It's better to use onclick here to avoid multiple bindings
    copiedInfo.classList.remove("hidden");
    navigator.clipboard.writeText(preElement.textContent).then(() => {
      console.log('Text copied to clipboard');
    }).catch(err => {
      console.error('Failed to copy text:', err);
    });
    setTimeout(function () {
      copiedInfo.classList.add("hidden");
    }, 500);
  };

  container.appendChild(importedNode);
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
      let current_model = models[0];
      for (let i = 0; i < models.length; i++) {
        if (selected_model==models[i]['model'])
        {
          current_model = models[i];
        }
       
      }
      const response = await fetch('/stream', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({'messages':messages,'model':current_model})
      });

      if (!response.body) {
        throw new Error('Failed to get a readable stream from the response');
      }

      const reader = response.body.getReader();

      while (true) {
        const { done, value } = await reader.read();
        if (done || stop_stream) {
          // After finishing the streaming, update the messages array and log it
          const stopIndexAccumulated = accumulatedResponse.indexOf("###STOP###");
          if (stopIndexAccumulated !== -1) {
            // If ###STOP### is found, use only the text before it as accumulatedResponse
            accumulatedResponse = accumulatedResponse.substring(0, stopIndexAccumulated);
          }
          messages.push({ role: 'assistant', content: accumulatedResponse });
          console.log('Stream finished, messages array:', messages);
          saveChatData(messages);
          toggleButtonVisibility();
          chatInput.readOnly = false;
          break;
        }
        const text = new TextDecoder().decode(value);
        accumulatedResponse += text; // Accumulate the response

        // Before updating, clear the existing content to avoid duplication
        botMessageElement.innerHTML = '';

        appendData(accumulatedResponse, botMessageElement)

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

document.getElementById("chat_input").addEventListener("keydown", function (event) {
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

document.getElementById("reset_button").addEventListener("click", function () {
  window.location.href = "/";
});
