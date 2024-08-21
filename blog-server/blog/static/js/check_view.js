$(document).ready(function(){
    setTimeout(function() {
        $.ajax({
           url: `${domain_name}/news/check_view`,
           type: "GET",
           data: {
                id: $(".news_card").attr('data-object-id')
           },
           success: function(response) {
                console.log('view + 1');
                $(".view_div").load(window.location.href + " .view_div > *");
           },
           error: function(xhr, status, error) {
               console.log("category changed with error");
           }
        });
    }, 5000);
});