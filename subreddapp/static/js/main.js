$(document).ready(function(){
    
    //voting
    $('body').on('click', '.point-arrow', function(event){
        var parent,id,arrowDir,what_type;
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

    
    //sorting with menu
    $('ul.header-menu').on('click', 'li', function(event){
        event.preventDefault();
        $('#activated-tab').removeAttr('id');
        $(this).attr('id','activated-tab');
        var sortway = $(this).attr('id-name');
        $.get("/"+sortway+"/", function(data){
            $('.posts').remove();
            $('.content').append(data);
        })
    });  

    //posting comment
    $('body').on('submit','.comment-form', function(event){        
        event.preventDefault();

        var text,parentpost_id,parentcomment_id;        
        textbox = $(this).parent().find(".talk-tome");
        text = textbox.val();
        parentpost_id = $('.post-box').first().attr('data-post-id');  
        childComment = $(this).parent().hasClass('child');       
        if( childComment )
        {
            parentcomment_id = $(this).closest('.post-box').attr("data-post-id");
        }
        console.log(childComment);
        var thisElement = $(this);
        $.post("/make_comment/", {text:text, parentpost_id:parentpost_id, parentcomment_id:parentcomment_id},
            function(data){                
                if(childComment){
                    thisElement.parent().append(data);
                    thisElement.remove();
                }else{
                    $(".comments").prepend(data);
                    textbox.val("");
                }                
            });
    });

    //reply comment
    $('.comments').on('click','.reply-button', function(event){
        console.log("TIK"); 
        var child = $(this).closest('.post-info').find('.child').first();
        var comment_form = child.children('form');
        console.log("PAPA:"+comment_form.length); 
        if(comment_form.length==0){   //if reply box is not opened, add reply box
            console.log("kid:"+comment_form.length); 
            $.get('/templates/make_comment_box/', function(data){
                child.prepend(data);
            });
        }else{
            comment_form.show();
        }        
    });

    //csrf token things
    function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    ///////


});