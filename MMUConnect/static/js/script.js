// script.js
document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('profile-btn');
  let loggedIn = localStorage.getItem('loggedIn') === 'true';

  const updateProfileButton = () => {
    btn.textContent = loggedIn ? '🔓 Logout' : '👤 Login';
    btn.title = loggedIn ? 'Click to log out' : 'Click to log in';
  };

  btn.addEventListener('click', () => {
    if (loggedIn) {
      localStorage.removeItem('loggedIn');
      loggedIn = false;
      updateProfileButton();
      window.location.href = 'login.html';
    } else {
      window.location.href = 'login.html';
    }
  });

  document.getElementById('send-btn').addEventListener('click', () => {
    const message = document.getElementById('chat-input').value;
    if (message.trim() !== '') {
      const messagesDiv = document.getElementById('messages');
      const newMessage = document.createElement('div');
      newMessage.classList.add('message');
      newMessage.innerHTML = `<strong>You:</strong> ${message}`;
      messagesDiv.appendChild(newMessage);
      document.getElementById('chat-input').value = '';
    }
  });

  updateProfileButton();
});
