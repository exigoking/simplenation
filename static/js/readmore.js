$(document).ready(function() {
    

    $('.exp-body').each(function() {
        var content = $(this).html();
        var explanation_id = $(this).attr('data-expid');

        content = content.split(/\s+/);

        if (content[content.length-1].toLowerCase().indexOf("...") >= 0){
            $("#see-more-"+explanation_id).show();
        }
 
    });
 
    $(".explanations-container-parent").on("click",".see-more", function(){
        
        var explanation_id = $(this).attr('data-expid');

        if ($(this).text()=="Show less"){
            
            $(this).text('Show more');
            $('#exp-full-body-'+explanation_id).hide();
            $('#exp-body-'+explanation_id).show();
        }
        else {
            
            $(this).text('Show less');
            $('#exp-body-'+explanation_id).hide();
            $('#exp-full-body-'+explanation_id).show();
        }

    });
});