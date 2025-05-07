<<<<<<< HEAD
const profiles = [
  {
    name: "M.Muhyideen",
    course: "Foundation in Information Technology",
    style: "I speak Java and sarcasm",
    image: "file:///C:/Users/User/Downloads/WhatsApp%20Image%202025-04-21%20at%2019.58.08_57f50f81.jpg"
  },
  {
    name: "Shaarvin",
    course: "Foundation in Information Technology",
    style: "99% sarcasm, 1% human",
    image: "file:///C:/Users/User/Downloads/shaarvin.jpg"
  },
  {
    name: "Roshan",
    course: "Foundation in Engineering",
    style: "99% of my jokes are dad jokes",
    image: "file:///C:/Users/User/Downloads/WhatsApp%20Image%202025-04-21%20at%2020.01.29_777565ba.jpg"
  },
  
];

let current = 0;

function loadProfile() {
  const container = document.getElementById("cardContainer");
  container.innerHTML = "";

  if (current < profiles.length) {
    const profile = profiles[current];

    const card = document.createElement("div");
    card.className = "profile-card";
    card.innerHTML = `
      <img src="${profile.image}" alt="${profile.name}" />
      <h3>${profile.name}</h3>
      <p>${profile.course}</p>
      <p>Bio: ${profile.style}</p>
    `;
    container.appendChild(card);
  } else {
    container.innerHTML = `<h2>No more profiles 😢</h2>`;
  }
}

function likeProfile() {
  alert(`❤️ You matched with ${profiles[current].name}!`);
  current++;
  loadProfile();
}

function skipProfile() {
  current++;
  loadProfile();
}

window.onload = loadProfile;
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
=======
const profiles = [
  {
    name: "M.Muhyideen",
    course: "Foundation in Information Technology",
    style: "I speak Java and sarcasm",
    image: "file:///C:/Users/User/Downloads/WhatsApp%20Image%202025-04-21%20at%2019.58.08_57f50f81.jpg"
  },
  {
    name: "Shaarvin",
    course: "Foundation in Information Technology",
    style: "99% sarcasm, 1% human",
    image: "file:///C:/Users/User/Downloads/shaarvin.jpg"
  },
  {
    name: "Roshan",
    course: "Foundation in Engineering",
    style: "99% of my jokes are dad jokes",
    image: "file:///C:/Users/User/Downloads/WhatsApp%20Image%202025-04-21%20at%2020.01.29_777565ba.jpg"
  },
  
];

let current = 0;

function loadProfile() {
  const container = document.getElementById("cardContainer");
  container.innerHTML = "";

  if (current < profiles.length) {
    const profile = profiles[current];

    const card = document.createElement("div");
    card.className = "profile-card";
    card.innerHTML = `
      <img src="${profile.image}" alt="${profile.name}" />
      <h3>${profile.name}</h3>
      <p>${profile.course}</p>
      <p>Bio: ${profile.style}</p>
    `;
    container.appendChild(card);
  } else {
    container.innerHTML = `<h2>No more profiles 😢</h2>`;
  }
}

function likeProfile() {
  alert(`❤️ You matched with ${profiles[current].name}!`);
  current++;
  loadProfile();
}

function skipProfile() {
  current++;
  loadProfile();
}

window.onload = loadProfile;
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
>>>>>>> 7ed2e66946d81267bfcaf1116c15102dd34617aa
