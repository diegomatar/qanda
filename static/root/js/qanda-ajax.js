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



// answers votes-up control
$('#resp_upvote').click(function(){
console.log("print 1");
    respid = $(this).attr("data-respid");
    var $th = $(this);
console.log("print 2");
    
    // if it is active, turn off and remove 1 vote
    if($th.hasClass('active')) {    
console.log("print 3");
        $.get('/resp-downvote/', {resposta_id: respid}, function(data){
            $('#resp_votes_count').html(data);
            $('#resp_upvote').removeClass( 'upvote-on' ).removeClass( 'active' ).addClass( 'upvote-off' );
        });
    }
    
    // if vote down is active, turn down off, turn up on and add 2 votes
    else if ($('#resp_downvote').hasClass('active')) {
console.log("print 4");
     $.get('/resp-upvote/', {resposta_id: respid});
     $.get('/resp-upvote/', {resposta_id: respid}, function(data){
            $('#resp_votes_count').html(data);
            $('#resp_downvote').removeClass( 'downvote-on' ).removeClass( 'active' ).addClass( 'downvote-off' );
            $('#resp_upvote').addClass('active').addClass( 'upvote-on' );
            
        });
     
    }
    
    // if none of votes are active, turn on and add a vote
    else {
console.log("print 5");
        $th.addClass('active');
console.log("print 6");
        $.get('/resp-upvote/', {resposta_id: respid}, function(data){
console.log("print 7");
                   $('#resp_votes_count').html(data);
                   $('#resp_upvote').removeClass( 'upvote-off' ).addClass( 'upvote-on' );
                   $('#resp_downvote').removeClass( 'downvote-on' ).removeClass( 'active' ).addClass( 'downvote-off' );
        });
    };
});