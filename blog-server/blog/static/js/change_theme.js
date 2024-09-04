$(document).ready(function(){
    function applyTheme(theme) {
        if (theme == 'light') {
            $(".change_theme").attr('data-theme', 'dark');
            $(".change_theme img").attr('src', `${domain_name}/static/svg/moon.svg`);
            $('.svg_icon').addClass('inverted');
            $(':root').css({
                '--light-blue': 'black',
                '--normal-blue': '#3282B8',
                '--dark-blue': '#BBE1FA',
                '--success-color': '#D9EE58',
                '--blank-color': '#0a3857',

                '--light-font': '0, 0, 0',
                '--dark-font': '255, 255, 255',

                '--for-category': 'var(--dark-blue)',
                '--for-comment': 'var(--normal-blue)',
                '--for-gradient-div': 'var(--blank-color)',
            });
        } else {
            $(".change_theme").attr('data-theme', 'light');
            $(".change_theme img").attr('src', `${domain_name}/static/svg/sun.svg`);
            $('.svg_icon').removeClass('inverted');
            $(':root').css({
                '--light-blue': '#BBE1FA',
                '--normal-blue': '#3282B8',
                '--dark-blue': '#0a3857',
                '--success-color': '#D9EE58',
                '--blank-color': 'white',

                '--light-font': '255, 255, 255',
                '--dark-font': '0, 0, 0',

                '--for-category': 'var(--normal-blue)',
                '--for-comment': 'var(--light-blue)',
                '--for-gradient-div': 'var(--normal-blue)',
            });
        };
    }

    $(".change_theme").on('click', function(){
        applyTheme($(this).attr('data-theme'));
        $.ajax({
           url: `${domain_name}/change_theme`,
           type: "GET",
           data: {

           },
           success: function(response) {

           },
           error: function(xhr, status, error) {
               console.log("category changed with error");
           }
        });
    });
});