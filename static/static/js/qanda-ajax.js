
// votes-up control
$('#upvote').click(function(){
    var perg_id;
    pergid = $(this).attr("data-pergid");
    var $th = $(this);
    
    // if it is active, turn off and remove 1 vote
    if($th.hasClass('active')) {
        $.get('/downvote/', {pergunta_id: pergid}, function(data){
            $('#votes_count').html(data);
            $('#upvote').removeClass( 'upvote-on' ).removeClass( 'active' ).addClass( 'upvote-off' );
        });
    }
    
    // if vote down is active, turn down off, turn up on and add 2 votes
    else if ($('#downvote').hasClass('active')) {
     $.get('/upvote/', {pergunta_id: pergid});
     $.get('/upvote/', {pergunta_id: pergid}, function(data){
            $('#votes_count').html(data);
            $('#downvote').removeClass( 'downvote-on' ).removeClass( 'active' ).addClass( 'downvote-off' );
            $('#upvote').addClass('active').addClass( 'upvote-on' );
            
        });
     
    }
    
    // if none of votes are active, turn on and add a vote
    else {
        $th.addClass('active');
        $.get('/upvote/', {pergunta_id: pergid}, function(data){
                   $('#votes_count').html(data);
                   $('#upvote').removeClass( 'upvote-off' ).addClass( 'upvote-on' );
                   $('#downvote').removeClass( 'downvote-on' ).removeClass( 'active' ).addClass( 'downvote-off' );
        });
    };
});


// down votes control
$('#downvote').click(function(){
    var perg_id;
    pergid = $(this).attr("data-pergid");
    var $th = $(this);
    
    // if is active, tur it off and remove one vote
    if($th.hasClass('active')) {
        $.get('/upvote/', {pergunta_id: pergid}, function(data){
            $('#votes_count').html(data);
            $('#downvote').removeClass( 'downvote-on' ).removeClass( 'active' ).addClass( 'downvote-off' );
        });
    }
    
    // if vote up is active, turn up off, turn down on and remove 2 votes
    else if ($('#upvote').hasClass('active')) {
     $.get('/downvote/', {pergunta_id: pergid});
     $.get('/downvote/', {pergunta_id: pergid}, function(data){
            $('#votes_count').html(data);
            $('#upvote').removeClass( 'upvote-on' ).removeClass( 'active' ).addClass( 'upvote-off' );
            $('#downvote').addClass('active').addClass( 'downvote-on' );
            
        });   
    }
    
    // if none is active, just turn down on and remove 1 vote.
    else {
    $th.addClass('active');
    $.get('/downvote/', {pergunta_id: pergid}, function(data){
               $('#votes_count').html(data);
               $('#downvote').removeClass( 'downvote-off' ).addClass( 'downvote-on' );
               $('#upvote').removeClass( 'upvote-on' ).removeClass( 'active' ).addClass( 'upvote-off' );
        });
    };
});