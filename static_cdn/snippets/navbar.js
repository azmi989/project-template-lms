$(document).ready(function(){
  var menu_icon = $("#menu_icon");
  var collapse = $("#collapse");

  menu_icon.click(function(){
    collapse.fadeToggle("slow");
  }); 


})