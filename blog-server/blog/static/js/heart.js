$(document).ready(function(){
    $(".heart_icon").on('click', function(){
        console.log('clicked');
        let news_id = $(this).attr('id');
        if ($(this).hasClass('is_heart')) {
            $(this).removeClass('is_heart');
            $(this).attr('src', "/static/svg/heart.svg");

            let prev_hearts_count = $(this).siblings().html();
            $(this).siblings().html(Number(prev_hearts_count)-1);
        } else {
            $(this).addClass('is_heart');
            $(this).attr('src', "/static/svg/heart_filled.svg");

            let prev_hearts_count = $(this).siblings().html();
            $(this).siblings().html(Number(prev_hearts_count)+1);
        }
        $.ajax({
           url: "http://127.0.0.1:8000/news/like_news",
           type: "GET",
           data: {
                id: news_id
           },
           success: function(response) {

           },
           error: function(xhr, status, error) {
               console.log("category changed with error");
           }
        });
    });
});