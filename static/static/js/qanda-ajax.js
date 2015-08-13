$(document).ready(function() {


// initialize all popovers on page
$(function () {
  $('[data-toggle="popover"]').popover({html:true})
})


// questions votes-up control
$('#perg_upvote').click(function(){
    pergid = $(this).attr("data-pergid");
    var $th = $(this);
    
    // if it is active, turn off and remove 1 vote
    if($th.hasClass('active')) {
        $.get('/downvote/', {pergunta_id: pergid}, function(data){
            $('#votes_count').html(data);
            $('#perg_upvote').removeClass( 'upvote-on' ).removeClass( 'active' ).addClass( 'upvote-off' );
        });
    }
    
    // if vote down is active, turn down off, turn up on and add 2 votes
    else if ($('#perg_downvote').hasClass('active')) {
     $.get('/upvote/', {pergunta_id: pergid});
     $.get('/upvote/', {pergunta_id: pergid}, function(data){
            $('#votes_count').html(data);
            $('#perg_downvote').removeClass( 'downvote-on' ).removeClass( 'active' ).addClass( 'downvote-off' );
            $('#perg_upvote').addClass('active').addClass( 'upvote-on' );
            
        });
     
    }
    
    // if none of votes are active, turn on and add a vote
    else {
        $th.addClass('active');
        $.get('/upvote/', {pergunta_id: pergid}, function(data){
                   $('#votes_count').html(data);
                   $('#perg_upvote').removeClass( 'upvote-off' ).addClass( 'upvote-on' );
                   $('#perg_downvote').removeClass( 'downvote-on' ).removeClass( 'active' ).addClass( 'downvote-off' );
        });
    };
});


// questions down votes control
$('#perg_downvote').click(function(){
    pergid = $(this).attr("data-pergid");
    var $th = $(this);
    
    // if is active, tur it off and remove one vote
    if($th.hasClass('active')) {
        $.get('/upvote/', {pergunta_id: pergid}, function(data){
            $('#votes_count').html(data);
            $('#perg_downvote').removeClass( 'downvote-on' ).removeClass( 'active' ).addClass( 'downvote-off' );
        });
    }
    
    // if vote up is active, turn up off, turn down on and remove 2 votes
    else if ($('#perg_upvote').hasClass('active')) {
     $.get('/downvote/', {pergunta_id: pergid});
     $.get('/downvote/', {pergunta_id: pergid}, function(data){
            $('#votes_count').html(data);
            $('#perg_upvote').removeClass( 'upvote-on' ).removeClass( 'active' ).addClass( 'upvote-off' );
            $('#perg_downvote').addClass('active').addClass( 'downvote-on' );
            
        });   
    }
    
    // if none is active, just turn down on and remove 1 vote.
    else {
    $th.addClass('active');
    $.get('/downvote/', {pergunta_id: pergid}, function(data){
               $('#votes_count').html(data);
               $('#perg_downvote').removeClass( 'downvote-off' ).addClass( 'downvote-on' );
               $('#perg_upvote').removeClass( 'upvote-on' ).removeClass( 'active' ).addClass( 'upvote-off' );
        });
    };
});


/*
// answers votes-up control
$('#resp_upvote').click(function(){
    respid = $(this).attr("data-respid");
    var $th = $(this);
    
    // if it is active, turn off and remove 1 vote
    if($th.hasClass('active')) {    
        $.get('/resp-downvote/', {resposta_id: respid}, function(data){
            $('#resp_votes_count').html(data);
            $('#resp_upvote').removeClass( 'upvote-on' ).removeClass( 'active' ).addClass( 'upvote-off' );
        });
    }
    
    // if vote down is active, turn down off, turn up on and add 2 votes
    else if ($('#resp_downvote').hasClass('active')) {
     $.get('/resp-upvote/', {resposta_id: respid});
     $.get('/resp-upvote/', {resposta_id: respid}, function(data){
            $('#resp_votes_count').html(data);
            $('#resp_downvote').removeClass( 'downvote-on' ).removeClass( 'active' ).addClass( 'downvote-off' );
            $('#resp_upvote').addClass('active').addClass( 'upvote-on' );
            
        });
     
    }
    
    // if none of votes are active, turn on and add a vote
    else {
        $th.addClass('active');
        $.get('/resp-upvote/', {resposta_id: respid}, function(data){
                   $('#resp_votes_count').html(data);
                   $('#resp_upvote').removeClass( 'upvote-off' ).addClass( 'upvote-on' );
                   $('#resp_downvote').removeClass( 'downvote-on' ).removeClass( 'active' ).addClass( 'downvote-off' );
        });
    };
});



// answers down votes control
$('#resp_downvote').click(function(){
    respid = $(this).attr("data-respid");
    var $th = $(this);
    
    // if is active, tur it off and remove one vote
    if($th.hasClass('active')) {
        $.get('/resp-upvote/', {resposta_id: respid}, function(data){
            $('#resp_votes_count').html(data);
            $('#resp_downvote').removeClass( 'downvote-on' ).removeClass( 'active' ).addClass( 'downvote-off' );
        });
    }
    
    // if vote up is active, turn up off, turn down on and remove 2 votes
    else if ($('#resp_upvote').hasClass('active')) {
     $.get('/resp-downvote/', {resposta_id: respid});
     $.get('/resp-downvote/', {resposta_id: respid}, function(data){
            $('#resp_votes_count').html(data);
            $('#resp_upvote').removeClass( 'upvote-on' ).removeClass( 'active' ).addClass( 'upvote-off' );
            $('#resp_downvote').addClass('active').addClass( 'downvote-on' );
            
        });   
    }
    
    // if none is active, just turn down on and remove 1 vote.
    else {
    $th.addClass('active');
    $.get('/resp-downvote/', {resposta_id: respid}, function(data){
               $('#resp_votes_count').html(data);
               $('#resp_downvote').removeClass( 'downvote-off' ).addClass( 'downvote-on' );
               $('#resp_upvote').removeClass( 'upvote-on' ).removeClass( 'active' ).addClass( 'upvote-off' );
        });
    };
});
*/
// Test version with variables as id selector:


// answers votes-up control
$('a#resp_upvote').click(function(){
    respid = $(this).attr("data-respid");
    var $th = $(this);
    var myClass = $(this).attr('class').split(' ')[0];
    
    // if it is active, turn off and remove 1 vote
    if($th.hasClass('active')) {    
        $.get('/resp-downvote/', {resposta_id: respid}, function(data){
            $('p.'+myClass).html(data);
            $('.'+myClass+'#resp_upvote').removeClass( 'upvote-on' ).removeClass( 'active' ).addClass( 'upvote-off' );
        });
    }
    
    // if vote down is active, turn down off, turn up on and add 2 votes
    else if ($('.'+myClass+'#resp_downvote').hasClass('active')) {
     $.get('/resp-upvote/', {resposta_id: respid});
     $.get('/resp-upvote/', {resposta_id: respid}, function(data){
            $('p.'+myClass).html(data);
            $('.'+myClass+'#resp_downvote').removeClass( 'downvote-on' ).removeClass( 'active' ).addClass( 'downvote-off' );
            $('.'+myClass+'#resp_upvote').addClass('active').addClass( 'upvote-on' );
            
        });
     
    }    
    
    // if none of votes are active, turn on and add a vote
    else {
        $th.addClass('active');
        $.get('/resp-upvote/', {resposta_id: respid}, function(data){
                   $('p.'+myClass).html(data);
                   $('.'+myClass+'#resp_upvote').removeClass( 'upvote-off' ).addClass( 'upvote-on' );
                   $('.'+myClass+'#resp_downvote').removeClass( 'downvote-on' ).removeClass( 'active' ).addClass( 'downvote-off' );
        });
    };
});



// answers down votes control
$('a#resp_downvote').click(function(){
    respid = $(this).attr("data-respid");
    var $th = $(this);
    var myClass = $(this).attr('class').split(' ')[0];
    
    // if is active, tur it off and remove one vote
    if($th.hasClass('active')) {
        $.get('/resp-upvote/', {resposta_id: respid}, function(data){
            $('p.'+myClass).html(data);
            $('.'+myClass+'#resp_downvote').removeClass( 'downvote-on' ).removeClass( 'active' ).addClass( 'downvote-off' );
        });
    }
    
    // if vote up is active, turn up off, turn down on and remove 2 votes
    else if ($('.'+myClass+'#resp_upvote').hasClass('active')) {
     $.get('/resp-downvote/', {resposta_id: respid});
     $.get('/resp-downvote/', {resposta_id: respid}, function(data){
            $('p.'+myClass).html(data);
            $('.'+myClass+'#resp_upvote').removeClass( 'upvote-on' ).removeClass( 'active' ).addClass( 'upvote-off' );
            $('.'+myClass+'#resp_downvote').addClass('active').addClass( 'downvote-on' );
            
        });   
    }
    
    // if none is active, just turn down on and remove 1 vote.
    else {
    $th.addClass('active');
    $.get('/resp-downvote/', {resposta_id: respid}, function(data){
               $('p.'+myClass).html(data);
               $('.'+myClass+'#resp_downvote').removeClass( 'downvote-off' ).addClass( 'downvote-on' );
               $('.'+myClass+'#resp_upvote').removeClass( 'upvote-on' ).removeClass( 'active' ).addClass( 'upvote-off' );
        });
    };
});


// follow and unfollow users control


$('a#follow_user').click(function(){
    var $th = $(this);
    userid = $th.attr("data-userid");
    var myClass = $th.attr('class').split(' ')[0];
    
    // follow user
    if($th.hasClass('follow')) {
        $.get('/perfil/follow-user/', {userprofile_id: userid}, function(data){
            $('#followers_count').html(data);
            $('.'+myClass+'#follow_user').removeClass( 'follow' ).addClass( 'unfollow' ).addClass( 'active' ).html('Seguindo');
        });
    }
    
    // unfollow user
    else if ($th.hasClass('unfollow')) {
     $.get('/perfil/unfollow-user/', {userprofile_id: userid}, function(data){
            $('#followers_count').html(data);
            $('.'+myClass+'#follow_user').removeClass( 'unfollow' ).removeClass( 'active' ).addClass( 'follow' ).html('Seguir');
        });
    }
    
});


// Topic sugestions
$('#suggestion').keyup(function(){
        var query;
        query = $(this).val();
        $.get('/sugest-topic/', {suggestion: query}, function(data){
         $('#tops').html(data);
        });
});



}); // document ready