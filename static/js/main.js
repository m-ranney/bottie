document.addEventListener('DOMContentLoaded', function () {
  // Event listener for clickable cards
  const cards = document.querySelectorAll('.card');
  cards.forEach(card => {
    card.addEventListener('click', () => {
      const url = card.getAttribute('data-href');
      if (url) {
        window.location.href = url;
      }
    });
  });
});
