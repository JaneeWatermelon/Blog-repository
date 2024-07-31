$(document).ready(function(){
    let n = 0;
    $(".category_name").on('click', function(){
        let category_id = $(this).attr('id');
        if (category_id == 'zero') {
            $(".category_name").removeClass('choosed_div');
            $(".category_name > p").removeClass('choosed_p');
            $(this).addClass('choosed_div');
            $(this).children().addClass('choosed_p');
            n = 0;
        }
        else {
            $(this).toggleClass('choosed_div');
            $(this).children().toggleClass('choosed_p');
            if ($(this).hasClass('choosed_div')) {
                n++;
            } else {
                n--;
            }
            if (n==0) {
                $("#zero").addClass('choosed_div');
                $("#zero > p").addClass('choosed_p');
            } else {
                $("#zero").removeClass('choosed_div');
                $("#zero > p").removeClass('choosed_p');
            }
            console.log(n);
        }
        $.ajax({
           url: "http://127.0.0.1:8000/news/change_category",
           type: "GET",
           data: {
                id: category_id
           },
           success: function(response) {
                $(".all_cards").load(window.location.href + " .all_cards > *", function(){
                    for (let i = 1; i < $(".all_cards").children().length; i+=2) {
                        $($(".all_cards").children()[i]).css({
                            top: '12vh',
                        });
                        console.log('done after ajax');
                    };
                });
           },
           error: function(xhr, status, error) {
               console.log("category changed with error");
           }
        });
    });
});