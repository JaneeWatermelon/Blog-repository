console.log($($(".all_cards").children()[0]));
for (let i = 1; i < $(".all_cards").children().length; i+=2) {
    $($(".all_cards").children()[i]).css({
        top: '50px',
    });
    console.log('done');
};