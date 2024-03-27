let messages = [{"role": "system", "content": "Du bist ein hilfreicher Assistent"}];

async function streamMessage() {
  // Adding a message about Ada Lovelace
  messages.push({ role: 'user', content: "Schreibe einen Blogbeitrag über Ada Lovelace?" });

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
      // Assuming you want to append each chunk of text as it arrives
      messageDiv.innerHTML += text;
    }
  } catch (error) {
    console.error('Streaming failed:', error);
    document.getElementById("message").innerHTML = `<p>Error occurred: ${error.message}</p>`;
  }
}

window.onload = streamMessage;
