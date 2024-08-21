$(document).ready(function(){
    console.log('clicked');
    console.log($(window).width());
    $.ajax({
       url: `${domain_name}/news/get_screen_width`,
       type: "GET",
       data: {
            width: $(window).width(),
       },
       success: function(response) {

       },
       error: function(xhr, status, error) {
           console.log("category changed with error");
       }
    });
});