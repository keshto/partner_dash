document.addEventListener('DOMContentLoaded', function() {
  var elems = document.querySelectorAll('.dropdown-trigger');
  var drop_options = {};
  var instances = M.Dropdown.init(elems, drop_options);

  var elems = document.querySelectorAll('.autocomplete');
  var instances = M.Autocomplete.init(elems, auto_options);
});