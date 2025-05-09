document.getElementById("send-btn").addEventListener("click", async () => {
    const userMessage = document.getElementById("chat-input").value;
    if (!userMessage.trim()) return;

    const chatBox = document.getElementById("messages");
    chatBox.innerHTML += `<p><strong>You:</strong> ${userMessage}</p>`;

    try {
        const response = await fetch(`/api/chat/?message=${encodeURIComponent(userMessage)}`);
        const data = await response.json();
        chatBox.innerHTML += `<p><strong>AI:</strong> ${data.reply}</p>`;
    } catch (error) {
        chatBox.innerHTML += `<p><strong>Error:</strong> Could not fetch AI response.</p>`;
    }

    document.getElementById("chat-input").value = "";
});
