document.addEventListener('DOMContentLoaded', function () {
  const dropdownToggle = document.querySelector('.dropdown-toggle');
  const dropdownMenu = document.querySelector('.dropdown-menu');

  dropdownToggle.addEventListener('click', function (event) {
    event.stopPropagation();
    dropdownMenu.classList.toggle('show');
  });

  dropdownMenu.addEventListener('click', function (event) {
    event.stopPropagation(); // Prevent menu clicks from closing it
  });

  document.addEventListener('click', function (event) {
    if (!dropdownMenu.contains(event.target) && !dropdownToggle.contains(event.target)) {
      dropdownMenu.classList.remove('show');
    }
  });
});
