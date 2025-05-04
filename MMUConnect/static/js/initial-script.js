// Adjusted profiles array: Static image paths should be passed dynamically via Django
const profiles = [
  {
    name: "M.Muhyideen",
    course: "Foundation in Information Technology",
    style: "I speak Java and sarcasm",
    image: "/static/img/muhyideen.jpg" // Example path (adjust as needed)
  },
  {
    name: "Shaarvin",
    course: "Foundation in Information Technology",
    style: "99% sarcasm, 1% human",
    image: "/static/img/shaarvin.jpg" // Example path (adjust as needed)
  },
  {
    name: "Roshan",
    course: "Foundation in Engineering",
    style: "99% of my jokes are dad jokes",
    image: "/static/img/roshan.jpg" // Example path (adjust as needed)
  }
];

let current = 0;

// Function to load and display a profile
function loadProfile() {
  const container = document.getElementById("cardContainer");
  container.innerHTML = ""; // Clear the container

  if (current < profiles.length) {
    const profile = profiles[current];

    // Create profile card dynamically
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

// Function for "like" action
function likeProfile() {
  if (current < profiles.length) {
    alert(`❤️ You matched with ${profiles[current].name}!`);
  }
  current++;
  loadProfile();
}

// Function for "skip" action
function skipProfile() {
  current++;
  loadProfile();
}

// Load the first profile on page load
window.onload = loadProfile;