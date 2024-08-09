$(document).ready(function(){
    $(".comment_shower").on('click', function(){
        if ($(this).hasClass('choosed_comment')) {
            $(this).removeClass('choosed_comment');
            $(".foot_comments").css({
                'display': 'none'
            });
        } else {
            $(this).addClass('choosed_comment');
            $(".foot_comments").css({
                'display': 'block'
            });
        };
    });
    $(".leave_comment > textarea").on('keydown keyup', function(){
        console.log('clicked');
        if ( $.trim($(".leave_comment > textarea").val()) == '' ) {
            $(".leave_comment > button").prop('disabled', true);
        } else {
            $(".leave_comment > button").prop('disabled', false);
        }
    });
    function make_base_comments() {
        let comments_page = Number($(".see_more_button").attr('data-page'));
        let all_comments = $(".all_comments").children();
        let comments_count = all_comments.length;
        for (let i = (comments_page-1)*10; i < comments_count && i < comments_page*10; i++){
            $(all_comments[i]).css('display', 'block');
        };
        if (comments_page*10 < comments_count) {
            $(".see_more_button").css('display', 'block');
        };
    };
    $(".foot_comments").on('click', '.leave_comment > button', function(){
        console.log('clicked');
        let news_id = $(".leave_comment textarea").attr('id');
        console.log(news_id);
        $.ajax({
           url: "http://127.0.0.1:8000/news/leave_comment",
           type: "GET",
           data: {
                text: $(".leave_comment textarea").val(),
                id: news_id,
           },
           success: function(response) {
                $(".leave_comment").load(window.location.href + " .leave_comment > *");
                $(".all_comments").load(window.location.href + " .all_comments > *", function() {
                    $(".see_more_button").attr('data-page', 1);
                    make_base_comments();
                });
                $(".comment_div").load(window.location.href + " .comment_div > *");
           },
           error: function(xhr, status, error) {
               console.log("category changed with error");
               window.location.href = "/users/login/";
           }
        });
    });
    make_base_comments();
    $(".see_more_button").on('click', function(){
        console.log('clicked');

        let comments_page = Number($(".see_more_button").attr('data-page'));
        let all_comments = $(".all_comments").children();
        let comments_count = all_comments.length;
        $(".see_more_button").attr('data-page', comments_page+1);
        comments_page = $(".see_more_button").attr('data-page');

        for (let i = (comments_page-1)*10; i < comments_count && i < comments_page*10; i++){
            $(all_comments[i]).css('display', 'block');
        };
        if (comments_page*10 >= comments_count) {
            $(".see_more_button").css('display', 'none');
        }
    });
});