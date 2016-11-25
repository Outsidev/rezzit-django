$(document).ready(function(){
    
    $('body').on('click', '.point-arrow', function(event){
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

    $('#comment-form').submit(function(event){
        console.log("SUBMTAI WORKDS!");
        event.preventDefault();
        sendComment();
    });

    $('ul.header-menu').on('click', 'li', function(event){
        event.preventDefault();
        $('#activated-tab').removeAttr('id');
        $(this).attr('id','activated-tab');
        sortway = $(this).attr('id-name');
        $.get("/"+sortway+"/", function(data){
            console.log(data);
            $('.posts').remove();
            $('.content').append(data);
        })
    });

    function sendComment(){
        text = $("#talk-tome").val()
        parentpost_id = $(".post-box").first().attr("data-post-id")
        $.post("/make_comment/", {text:text, parentpost_id:parentpost_id},
            function(data){
                $(".comments").prepend(data);                
            });
    };

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