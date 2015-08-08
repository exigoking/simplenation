$(document).ready(function() {
    

    $('.profile-explanation-span').each(function () {
        
        var not_html = $(this).text().replace(/(<([^>]+)>)/ig,"");
        $(this).html(not_html);
    });
    
});