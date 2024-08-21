

$(document).ready(function(){
    $(".star_icon").on('click', function(){
        console.log('clicked');
        let category_id = $(this).siblings().attr('id');
        if ($(this).hasClass('in_star')) {
            $(this).removeClass('in_star');
            $(this).attr('src', "/static/svg/star.svg");
        } else {
            $(this).addClass('in_star');
            $(this).attr('src', "/static/svg/star_filled.svg");
        }
        $.ajax({
           url: `${domain_name}/news/change_star`,
           type: "GET",
           data: {
                id: category_id
           },
           success: function(response) {

           },
           error: function(xhr, status, error) {
               console.log("category changed with error");
               window.location.href = "/users/login/";
           }
        });
    });
});