$(document).ready(function(){
    $(".like").on('click', function(){
        console.log('clicked');
        let comment_id = $(this).attr('data-comment-id');
        if ($(this).hasClass('is_rate')) {
            $(this).removeClass('is_rate');
            $(this).attr('src', "/static/svg/like.svg");

            let prev_likes_count = $(this).siblings().html();
            $(this).siblings().html(Number(prev_likes_count)-1);
        } else {
            $(this).addClass('is_rate');
            $(this).attr('src', "/static/svg/like_filled.svg");

            let prev_likes_count = $(this).siblings().html();
            $(this).siblings().html(Number(prev_likes_count)+1);
        }
        $.ajax({
           url: "http://127.0.0.1:8000/news/rate_comment",
           type: "GET",
           data: {
                id: comment_id,
                type: 'like',
           },
           success: function(response) {

           },
           error: function(xhr, status, error) {
               console.log("category changed with error");
           }
        });
    });
    $(".dislike").on('click', function(){
        console.log('clicked');
        let comment_id = $(this).attr('data-comment-id');
        if ($(this).hasClass('is_rate')) {
            $(this).removeClass('is_rate');
            $(this).attr('src', "/static/svg/like.svg");
        } else {
            $(this).addClass('is_rate');
            $(this).attr('src', "/static/svg/like_filled.svg");
        }
        $.ajax({
           url: "http://127.0.0.1:8000/news/rate_comment",
           type: "GET",
           data: {
                id: comment_id,
                type: 'dislike',
           },
           success: function(response) {

           },
           error: function(xhr, status, error) {
               console.log("category changed with error");
           }
        });
    });
});