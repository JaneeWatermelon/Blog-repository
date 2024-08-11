$(document).ready(function(){
    $(".choose_bar").on('click', function() {
        let p = $(this).children().html();
        console.log(Number(p.slice(0, p.length-2)));
        $(".input_field").val(Number(p.slice(0, p.length-2)));
    });
});