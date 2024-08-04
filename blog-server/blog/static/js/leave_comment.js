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
    })
    $(".leave_comment > button").on('click', function(){
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
                $(".foot_comments").load(window.location.href + " .foot_comments > *");
                $(".card_bottom_icons").load(window.location.href + " .card_bottom_icons > *");
           },
           error: function(xhr, status, error) {
               console.log("category changed with error");
           }
        });
    });
});