$(document).ready(function(){
    function type_4() {
        if ($(window).width() > 768) {
            $(".news_card").css({
                width: '24%',
                transform: "translateY(4vh)",
            });
            $(".news_card_body").css({
                'aspect-ratio': '1',
            });
            for (let i = 1; i < $(".all_cards").children().length; i+=2) {
                $($(".all_cards").children()[i]).css({
                    transform: "translateY(12vh)",
                });
                console.log('done');
            };
        };
        $(".show_variants").attr('data-show_type', 'type_4');
    };

    function type_3() {
        if ($(window).width() > 768) {
            $(".news_card").css({
                width: '32%',
                transform: "translateY(4vh)",
            });
            $(".news_card_body").css({
                'aspect-ratio': '1.5',
            });
            for (let i = 1; i < $(".all_cards").children().length; i+=3) {
                $($(".all_cards").children()[i]).css({
                    transform: "translateY(12vh)",
                });
                console.log('done');
            };
        };
        $(".show_variants").attr('data-show_type', 'type_3');
    };
    function check_show_type() {
        if ($(".show_variants").attr('data-show_type') == 'type_4') {
            type_4();
        } else {
            type_3();
        };
    };
    check_show_type()

    let n = Number($(".category_card_body").attr('data-active-count'));
    console.log(n);
    $(".category_card_body").on('click', '.category_name', function(){
        let category_id = $(this).attr('id');
        if (category_id == '0') {
            $(".category_name").removeClass('choosed_div');
            $(this).addClass('choosed_div');
            n = 0;
        }
        else {
            $(this).toggleClass('choosed_div');
            if ($(this).hasClass('choosed_div')) {
                n++;
            } else {
                n--;
            }
            if (n==0) {
                $("#0").addClass('choosed_div');
            } else {
                $("#0").removeClass('choosed_div');
            }
            console.log(n);
        }
        $.ajax({
           url: `${domain_name}/news/change_category`,
           type: "GET",
           data: {
                id: category_id,
                page: $(".paginator_block").attr('data-page')
           },
           success: function(response) {
                console.log(response['choosed_theme'])
                if (response['redirect']) {
                    $(location).prop('href', domain_name);
                } else {
                    $(".all_cards").load(window.location.href + " .all_cards > *", function(){
                        check_show_type();
                        if ($('.change_theme').attr('data-theme') == 'light') {
                            $('.svg_icon').removeClass('inverted');
                        } else {
                            $('.svg_icon').addClass('inverted');
                        };
                    });
                    if ($(".paginator_block")) {
                        console.log('paginated');
                        $(".paginator_block").load(window.location.href + " .desktop.paginator_block > *");
                    };
                };

           },
           error: function(xhr, status, error) {
               console.log("category changed with error");
           }
        });
    });
    $(".variant").on('click', function(){
        let type;
        if ($(this).hasClass('choosed') == false) {
            if ($(this).hasClass('type_4')) {
                type = 'type_4';
                $(this).toggleClass('choosed');
                $(".type_3").toggleClass('choosed');
                type_4();
            } else {
                type = 'type_3';
                $(this).toggleClass('choosed');
                $(".type_4").toggleClass('choosed');
                type_3();
            };
        };
        $.ajax({
           url: `${domain_name}/news/change_show_type`,
           type: "GET",
           data: {
                show_type: type,
           },
           success: function(response) {

           },
           error: function(xhr, status, error) {
               console.log("category changed with error");
           }
        });
    });
});