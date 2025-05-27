// script.js
  const words = ["python", "django", "scramble", "student", "exam", "project", "coding", "keyboard", "monitor", "internet"];
  let currentWord = "";
  let scrambled = "";

  function shuffle(word) {
    return word.split('').sort(() => Math.random() - 0.5).join('');
  }

  function newScramble() {
    currentWord = words[Math.floor(Math.random() * words.length)];
    scrambled = shuffle(currentWord);
    // prevent scrambled = actual word
    while (scrambled === currentWord) {
      scrambled = shuffle(currentWord);
    }
    document.getElementById("scrambled-word").textContent = scrambled;
    document.getElementById("user-guess").value = "";
    document.getElementById("scramble-feedback").textContent = "";
  }

  function checkGuess() {
    const guess = document.getElementById("user-guess").value.trim().toLowerCase();
    const feedback = document.getElementById("scramble-feedback");

    if (guess === currentWord) {
      feedback.textContent = "✅ Correct! Loading new word...";
      feedback.style.color = "green";
      setTimeout(newScramble, 1500);
    } else {
      feedback.textContent = "❌ Try again!";
      feedback.style.color = "red";
    }
  }

  document.addEventListener("DOMContentLoaded", newScramble);

