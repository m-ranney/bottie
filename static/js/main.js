document.addEventListener('DOMContentLoaded', function () {
  var cards = document.querySelectorAll('.card');

  cards.forEach(function (card) {
    card.addEventListener('click', function () {
      var targetUrl = this.getAttribute('data-href');
      if (targetUrl) {
        location.href = targetUrl;
      }
    });
  });
});
