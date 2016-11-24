$(document).ready(function(){
    
    $('.point-arrow').click(function(event){
        var parent,id;
        parent = $(this).closest('.post-box');  
        id = parent.attr('data-post-id');      
        arrowDir = $(this).hasClass('up-arrow');
        what_type = parent.attr('data-type');          
        $.get('/give_point/', 
            { post_id: id, arrow_dir: arrowDir, what_type:what_type }, 
            function(data){
                $(event.target).closest('.post-box').find(".post-point").html(data);
        });

    });

});