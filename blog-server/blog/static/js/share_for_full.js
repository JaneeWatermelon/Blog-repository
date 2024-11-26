
$('.share_div').on('click', function() {
    const width = window.innerWidth;
    if (width <= 768) {
       $('.dropdown .mobile').css('display', 'flex');
    } else {
       $('.dropdown .mobile').css('display', 'none');
    }
    var dropdown = $(this).find('.dropdown');
    if (dropdown.css('display') == 'flex') {
        dropdown.css('display', 'none');
    } else {
        dropdown.css('display', 'flex');
    }
})

Share = {
	telegram: function(purl, text) {
		url  = 'https://telegram.me/share/url?';
		url += 'url=' + encodeURIComponent(purl);
		url += `&text=На Blogus появилась свежая новость!`;
		Share.popup(url);
	},
	viber: function(purl, text) {
		url  = 'viber://forward?';
		url += `text=На Blogus появилась свежая новость! Смотри по ссылке:${encodeURIComponent(purl)}`;
		Share.popup(url);
	},
	whatsapp: function(purl, text) {
		url  = 'whatsapp://send?';
		url += `text=На Blogus появилась свежая новость! Смотри по ссылке:${encodeURIComponent(purl)}`;
		Share.popup(url);
	},
	vkontakte: function(purl, ptitle, pimg, text) {
		url  = 'http://vkontakte.ru/share.php?';
		url += 'url='          + encodeURIComponent(purl);
		url += '&title='       + encodeURIComponent(ptitle);
		url += '&description=' + encodeURIComponent(text);
		url += '&image='       + encodeURIComponent(pimg);
		url += '&noparse=true';
		Share.popup(url);
	},

	popup: function(url) {
		window.open(url,'','toolbar=0,status=0,width=626,height=436');
	}
};