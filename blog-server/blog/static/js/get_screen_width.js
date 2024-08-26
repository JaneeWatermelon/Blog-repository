function detectDevice() {
   const width = window.innerWidth;
   if (width <= 768) {
       $('.mobile').css('display', 'flex');

//     # full card
       $('.news_card > .mobile.card_header').css('display', 'block');
       $('.news_card > .mobile.card_body').css('display', 'block');
//     # registration_card
       $('.registration_card > .mobile.card_body').css('display', 'flex');

       $('.mobile.paginator_block').css('display', 'block');
       $('.desktop').css('display', 'none');
   } else {
       $('.desktop').css('display', 'flex');

//     # full card
       $('.news_card > .desktop.card_header').css('display', 'block');
       $('.news_card > .desktop.card_body').css('display', 'block');

//     # registration_card
       $('.registration_card > .desktop.card_body').css('display', 'flex');

       $('.desktop.paginator_block').css('display', 'block');

       $('.mobile').css('display', 'none');
   }
}

window.onload = detectDevice;
window.onresize = detectDevice;