$(document).ready(function(){
    $(".profile_adds_card_middle").on('click', '.heart_icon', function(){
        console.log('clicked');
        let news_id = $(this).attr('id');
        let click_type;
        if ($(this).hasClass('is_heart')) {
            click_type = 'unlike';
            $(this).removeClass('is_heart');
            $(this).attr('src', "/static/svg/heart.svg");

            let prev_hearts_count = $(this).siblings().html();
            $(this).siblings().html(Number(prev_hearts_count)-1);
        } else {
            click_type = 'like';
            $(this).addClass('is_heart');
            $(this).attr('src', "/static/svg/heart_filled.svg");

            let prev_hearts_count = $(this).siblings().html();
            $(this).siblings().html(Number(prev_hearts_count)+1);
        }
        $.ajax({
           url: "http://127.0.0.1:8000/news/like_news",
           type: "GET",
           data: {
                type: click_type,
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