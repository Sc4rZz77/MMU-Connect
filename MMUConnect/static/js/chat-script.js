document.getElementById("send-btn").addEventListener("click", async () => {
    const inputField = document.getElementById("chat-input");
    const userMessage = inputField.value.trim();
    const chatBox = document.getElementById("messages");

    if (!userMessage) return;

    // Add user message
    chatBox.innerHTML += `<p><strong>You:</strong> ${userMessage}</p>`;

    // Optional: Add "typing..." effect
    chatBox.innerHTML += `<p id="ai-typing"><strong>AI:</strong> Typing...</p>`;

    try {
        const response = await fetch(`/api/chat/?message=${encodeURIComponent(userMessage)}`);
        const data = await response.json();

        // Replace typing text with actual response
        document.getElementById("ai-typing").outerHTML = `<p><strong>AI:</strong> ${data.reply}</p>`;
    } catch (error) {
        document.getElementById("ai-typing").outerHTML = `<p><strong>Error:</strong> Could not fetch AI response.</p>`;
    }

    // Reset input field
    inputField.value = "";
    inputField.focus();  // Better UX
});
