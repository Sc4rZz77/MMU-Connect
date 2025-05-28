// script.js
  const quotes = [
    "Success doesn't come from what you do occasionally, it comes from what you do consistently.",
    "Discipline is choosing between what you want now and what you want most.",
    "Push yourself, because no one else is going to do it for you.",
    "Study now, be proud later.",
    "Don’t watch the clock; do what it does. Keep going.",
    "Your future is created by what you do today, not tomorrow.",
    "Great things never come from comfort zones.",
    "Dream big. Work hard. Stay focused.",
    "Believe you can and you’re halfway there.",
    "Every accomplishment starts with the decision to try.",
    "Focus on your goal. Don’t look in any direction but ahead.",
    "Keep going. Everything you need will come to you.",
    "Small steps every day lead to big results.",
    "You don’t have to be great to start, but you have to start to be great.",
    "Success is the sum of small efforts, repeated day in and day out.",
    "Hard work beats talent when talent doesn’t work hard.",
    "Stay positive, work hard, make it happen.",
    "Failure is the opportunity to begin again more intelligently.",
    "Be stronger than your excuses.",
    "You’re capable of more than you know."
  ];

  let currentQuoteIndex = Math.floor(Math.random() * quotes.length);

  function showQuote(index) {
    document.getElementById("quote-text").textContent = quotes[index];
  }

  function showNextQuote() {
    currentQuoteIndex = (currentQuoteIndex + 1) % quotes.length;
    showQuote(currentQuoteIndex);
  }

  // Initial quote on page load
  document.addEventListener("DOMContentLoaded", () => {
    showQuote(currentQuoteIndex);

    // Optional: If you want a button to show next quote, add event listener here
    // document.getElementById("next-quote-btn").addEventListener("click", showNextQuote);
  });
