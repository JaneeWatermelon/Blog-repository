

$(document).ready(function(){
    $(".like").on('click', function(){
        console.log('clicked');
        let see_type;
        if ($(this).hasClass('choosed')) {
            $(this).removeClass('choosed');
            see_type = 'none';
        } else {
            $(this).addClass('choosed');
            $(".view").removeClass('choosed');
            see_type = 'like';
        }
        $.ajax({
           url: `${domain_name}/users/see_news_in_profile`,
           type: "GET",
           data: {
                type: see_type,
           },
           success: function(response) {
                $(".profile_adds_card_middle").load(window.location.href + " .profile_adds_card_middle > *");
           },
           error: function(xhr, status, error) {
               console.log("category changed with error");
           }
        });
    });
    $(".view").on('click', function(){
        console.log('clicked');
        let see_type;
        if ($(this).hasClass('choosed')) {
            $(this).removeClass('choosed');
            see_type = 'none';
        } else {
            $(this).addClass('choosed');
            $(".like").removeClass('choosed');
            see_type = 'view';
        }
        $.ajax({
           url: `${domain_name}/users/see_news_in_profile`,
           type: "GET",
           data: {
                type: see_type,
           },
           success: function(response) {
                $(".profile_adds_card_middle").load(window.location.href + " .profile_adds_card_middle > *");
           },
           error: function(xhr, status, error) {
               console.log("category changed with error");
               window.location.href = "/users/login/";
           }
        });
    });
});