function collapseMenu(){
    var x = document.getElementById("collapse");
    if (x.className === "collapse") {
      x.className += " show";
    } else {
      x.className = "collapse";
    }
  } 