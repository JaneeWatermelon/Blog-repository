$(document).ready(function(){
    $(".category_card_header").on('click', function(){
        console.log('clicked');
        $(".category_card_header").toggleClass('show');
        $(".category_card").toggleClass('show');
    });
});