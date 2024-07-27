
console.log('done 1');
$('#comment_input').on('input', function(){
    $("#comment_input").css('height', 'fit-content');
    console.log($("#comment_input").css('height'));
    $("#comment_input").css('height', `${this.scrollHeight}px`);
    console.log($("#comment_input").css('height'));
    $("#comment_input").parent().css('height', `${this.scrollHeight+20}px`);
    console.log($("#comment_input").val());
});
console.log('done 5');