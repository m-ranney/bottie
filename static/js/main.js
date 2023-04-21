document.addEventListener('DOMContentLoaded', function () {
  var buttons = document.querySelectorAll('.custom-button');

  buttons.forEach(function (button) {
    button.addEventListener('click', function () {
      alert('You clicked a custom button!');
    });
  });
});
