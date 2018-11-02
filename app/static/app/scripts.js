document.addEventListener('DOMContentLoaded', function() {
  var elems = document.querySelectorAll('.dropdown-trigger');
  var drop_options = {};
  var instances = M.Dropdown.init(elems, drop_options);

  var elems = document.querySelectorAll('.autocomplete');
  var instances = M.Autocomplete.init(elems, auto_options);

  var tab_options = {}
  var elems = document.querySelectorAll('.tabs')
  var instance = M.Tabs.init(elems, tab_options);

  // var elems = document.querySelectorAll('.chips');
  // var instances = M.Chips.init(elems, chip_options);
});

// in ms
var poller_timeout = 3000;
var poller_url = 'hash/';
// will update with ajax query
var poller_hash = -1;

var poller = function() {
  var httpRequest = new XMLHttpRequest();
  httpRequest.onreadystatechange = readyStateChanged;
  httpRequest.open('GET', poller_url);
  httpRequest.send();
};

if(document.readyState === 'complete')
  setTimeout(poller);
else if(document.addEventListener)
  document.addEventListener('DOMContentLoaded', poller);
else
  window.attachEvent('onload', poller);

var readyStateChanged = function() {
    if(this.readyState != 4)
        return;
    if(this.status == 200) {
      if (poller_hash < 0) 
        poller_hash = this.response;
      else if(poller_hash != this.response){
        document.getElementById("notification").classList.remove("hide");
        return
      };
    };
    setTimeout(poller, poller_timeout);
};

