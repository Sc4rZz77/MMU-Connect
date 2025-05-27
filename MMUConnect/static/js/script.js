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

function showAuthor(index) {
  authors.forEach(author => {
    author.style.display = 'none';
    author.style.opacity = '0';
  });
  if (index < authors.length) {
    let current = authors[index];
    current.style.display = 'block';
    // Re-trigger animation
    void current.offsetWidth; 
    current.style.animation = 'fadeIn 0.5s ease forwards';
  } else {
    alert("No more authors to display.");
  }
}
