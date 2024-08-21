

$(document).ready(function(){
    $(".foot_comments").on('click', '.like', function(){
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
            console.log($(".dislike").filter(`[data-comment-id="${comment_id}"]`))
            $(".dislike").filter(`[data-comment-id="${comment_id}"]`).removeClass('is_rate');
            $(".dislike").filter(`[data-comment-id="${comment_id}"]`).attr('src', "/static/svg/like.svg");

            let prev_likes_count = $(this).siblings().html();
            $(this).siblings().html(Number(prev_likes_count)+1);
        }
        $.ajax({
           url: `${domain_name}/news/rate_comment`,
           type: "GET",
           data: {
                id: comment_id,
                type: 'like',
           },
           success: function(response) {

           },
           error: function(xhr, status, error) {
               console.log("category changed with error");
               window.location.href = "/users/login/";
           }
        });
    });
    $(".foot_comments").on('click', '.dislike', function(){
        console.log('clicked');
        let comment_id = $(this).attr('data-comment-id');
        if ($(this).hasClass('is_rate')) {
            $(this).removeClass('is_rate');
            $(this).attr('src', "/static/svg/like.svg");
        } else {
            $(this).addClass('is_rate');
            $(this).attr('src', "/static/svg/like_filled.svg");

            let like_img = $(".like").filter(`[data-comment-id="${comment_id}"]`);
            console.log(like_img)
            console.log(like_img.hasClass('is_rate'))
            if (like_img.hasClass('is_rate')){
                $(".like").filter(`[data-comment-id="${comment_id}"]`).removeClass('is_rate');
                $(".like").filter(`[data-comment-id="${comment_id}"]`).attr('src', "/static/svg/like.svg");

                let prev_likes_count = like_img.siblings().html();
                like_img.siblings().html(Number(prev_likes_count)-1);
            }
        }
        $.ajax({
           url: `${domain_name}/news/rate_comment`,
           type: "GET",
           data: {
                id: comment_id,
                type: 'dislike',
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