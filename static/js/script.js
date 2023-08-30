// stolen from w3
function dropdownt() {
    document.getElementById("tagsdropdown").classList.toggle("show");
  }

function dropdownp() {
  document.getElementById("parentdropdown").classList.toggle("show");
}


window.onclick = function(event) {
  if (!event.target.matches('.dropdown')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}