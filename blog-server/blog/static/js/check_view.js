$(document).ready(function(){
    $.ajax({
       url: "http://127.0.0.1:8000/news/check_view",
       type: "GET",
       data: {
            id: $(".news_card").attr('data-object-id')
       },
       success: function(response) {
            $(".view_div").load(window.location.href + " .view_div > *");
       },
       error: function(xhr, status, error) {
           console.log("category changed with error");
       }
    });
});