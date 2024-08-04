
console.log('done 1');
$('.leave_comment textarea').on('input', function(){
    $('.leave_comment textarea').css('height', 'fit-content');
    console.log($('.leave_comment textarea').css('height'));
    $('.leave_comment textarea').css('height', `${this.scrollHeight}px`);
    console.log($('.leave_comment textarea').css('height'));
    $('.leave_comment textarea').parent().css('height', `${this.scrollHeight+20}px`);
    console.log($('.leave_comment textarea').val());
});
console.log('done 5');