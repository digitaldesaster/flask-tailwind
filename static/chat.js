let messages = [{"role": "system", "content": "Du bist ein hilfreicher Assistent"}];

async function streamMessage() {
  const chatInput = document.getElementById("chat_input");
  const userMessage = chatInput.value.trim();

  if (userMessage !== '') {
    messages.push({ role: 'user', content: userMessage });
    chatInput.value = ''; // Clear the input field after sending the message

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
      const messageDiv = document.getElementById("message");
      messageDiv.innerHTML = ''; // Clear the div before streaming new content

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const text = new TextDecoder().decode(value);
        messageDiv.innerHTML += text;
      }
    } catch (error) {
      console.error('Streaming failed:', error);
      document.getElementById("message").innerHTML = `<p>Error occurred: ${error.message}</p>`;
    }
  }
}

document.getElementById("chat_button").addEventListener("click", streamMessage);