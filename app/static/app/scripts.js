document.addEventListener('DOMContentLoaded', function() {
  var elems = document.querySelectorAll('.dropdown-trigger');
  var drop_options = {};
  var instances = M.Dropdown.init(elems, drop_options);

  var elems = document.querySelectorAll('.autocomplete');
  var instances = M.Autocomplete.init(elems, auto_options);

  var tab_options = {}
  var elems = document.querySelectorAll('.tabs')
  var instance = M.Tabs.init(elems, tab_options);

  var elems = document.querySelectorAll('.chips');
  var instances = M.Chips.init(elems, chip_options);
});