$('.leave_comment textarea').on('input', function(){
    console.log('inputed');
    $('.leave_comment textarea').css('height', 'fit-content');
//    console.log($('.leave_comment textarea').css('height'));
    $('.leave_comment textarea').css('height', `${this.scrollHeight}px`);
//    console.log($('.leave_comment textarea').css('height'));
    $('.leave_comment textarea').parent().css('height', `${this.scrollHeight+20}px`);
//    console.log($('.leave_comment textarea').val());
});