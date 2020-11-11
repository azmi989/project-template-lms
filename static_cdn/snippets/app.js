
$(document).ready(function(){
    $("#menu").click(function(){
        var collapse_className = $("#collapse").attr('class')
        if (collapse_className === 'collapse') {
            $("#collapse").addClass("element_animation_fadeDown");
            $("#collapse").addClass("active");
            $("#menu").removeClass("open");
            $("#menu").addClass("close");
            } else {
                $("#collapse").removeClass("element_animation_fadeDown");
                $("#collapse").removeClass("active");
                $("#menu").removeClass("close");
                $("#menu").addClass("open");
            };
    });
});


