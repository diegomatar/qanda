$(document).ready(function() {


// initialize all popovers on page
$(function () {
  $('[data-toggle="popover"]').popover({html:true})
});

/*
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
*/


// New question votes control

// question votes-up control
$('a.perg_upvote').click(function(){
    pergid = $(this).attr("data-pergid");
    var $th = $(this);
    var myId = $(this).attr('id');
    
    // if it is active, turn off and remove 1 vote
    if($th.hasClass('active')) {    
        $.get('/downvote/', {pergunta_id: pergid}, function(data){
            $('p#'+myId).html(data);
            $('.perg_upvote#'+myId).removeClass( 'upvote-on' ).removeClass( 'active' ).addClass( 'upvote-off' );
        });
    }
    
    // if vote down is active, turn down off, turn up on and add 2 votes
    else if ($('.perg_downvote#'+myId).hasClass('active')) {
     $.get('/upvote/', {pergunta_id: pergid});
     $.get('/upvote/', {pergunta_id: pergid}, function(data){
            $('p#'+myId).html(data);
            $('.perg_downvote#'+myId).removeClass( 'downvote-on' ).removeClass( 'active' ).addClass( 'downvote-off' );
            $('.perg_upvote#'+myId).addClass('active').addClass( 'upvote-on' );
            
        });
     
    }    
    
    // if none of votes are active, turn on and add a vote
    else {
        $th.addClass('active');
        $.get('/upvote/', {pergunta_id: pergid}, function(data){
                   $('p#'+myId).html(data);
                   $('.perg_upvote#'+myId).removeClass( 'upvote-off' ).addClass( 'upvote-on' );
                   $('.perg_downvote#'+myId).removeClass( 'downvote-on' ).removeClass( 'active' ).addClass( 'downvote-off' );
        });
    };
});



// question down votes control
$('a.perg_downvote').click(function(){
    pergid = $(this).attr("data-pergid");
    var $th = $(this);
    var myId = $(this).attr('id');
    console.log(myId)
    
    // if is active, tur it off and remove one vote
    if($th.hasClass('active')) {
        $.get('/upvote/', {pergunta_id: pergid}, function(data){
            $('p#'+myId).html(data);
            $('.perg_downvote#'+myId).removeClass( 'downvote-on' ).removeClass( 'active' ).addClass( 'downvote-off' );
        });
    }
    
    // if vote up is active, turn up off, turn down on and remove 2 votes
    else if ($('.perg_upvote#'+myId).hasClass('active')) {
     $.get('/downvote/', {pergunta_id: pergid});
     $.get('/downvote/', {pergunta_id: pergid}, function(data){
            $('p#'+myId).html(data);
            $('.perg_upvote#'+myId).removeClass( 'upvote-on' ).removeClass( 'active' ).addClass( 'upvote-off' );
            $('.perg_downvote#'+myId).addClass('active').addClass( 'downvote-on' );
            
        });   
    }
    
    // if none is active, just turn down on and remove 1 vote.
    else {
    $th.addClass('active');
    $.get('/downvote/', {pergunta_id: pergid}, function(data){
               $('p#'+myId).html(data);
               $('.perg_downvote#'+myId).removeClass( 'downvote-off' ).addClass( 'downvote-on' );
               $('.perg_upvote#'+myId).removeClass( 'upvote-on' ).removeClass( 'active' ).addClass( 'upvote-off' );
        });
    };
});







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
$('a.follow_user').click(function(){
    var $th = $(this);
    userid = $th.attr("data-userid");
    var myId = $(this).attr('id');
    
    // follow user
    if($th.hasClass('follow')) {
        $.get('/perfil/follow-user/', {userprofile_id: userid}, function(data){
            $('.followers_count#'+myId).html(data);
            $('.follow_user#'+myId).removeClass( 'follow' ).addClass( 'unfollow' ).addClass( 'active' ).html('Seguindo');
        });
    }
    
    // unfollow user
    else if ($th.hasClass('unfollow')) {
     $.get('/perfil/unfollow-user/', {userprofile_id: userid}, function(data){
            $('.followers_count#'+myId).html(data);
            $('.follow_user#'+myId).removeClass( 'unfollow' ).removeClass( 'active' ).addClass( 'follow' ).html('Seguir');
        });
    }
    
});


// follow and unfollow questions control
$('.follow_quest').click(function(){
    questid = $(this).attr("data-questid");
    var $th = $(this);
    
    // if is active, tur it off and unfollow question
    if($th.hasClass('active')) {
        $.get('/unfollow-question/', {pergunta_id: questid}, function(data){
            $th.removeClass( 'active' ).html('Seguir');
        });
    }
    // tur it on and follow question
    else {
        $.get('/follow-question/', {pergunta_id: questid}, function(data){
            $th.addClass( 'active' ).html('Seguindo');
        });
    };
});




// Toggle answer icon
$('#responder').click(function(){
    $(this).find('i').toggleClass('fa-toggle-on fa-toggle-off')
});



// Sugests questions
$(function(){
    $("#collapseQsts").hide();
    $("#newquestion").hide();
    $("#collapseDetails").hide();
    $("div#newquestion").on("click", function(){
        $("#collapseQsts, #collapseDetails").toggle();
        $(this).hide();
    });
    $("#entendi1").on("click", function(){
        $("div#dicas").hide();
    });
    $("#entendi2").on("click", function(){
        $("div#dicas").hide();
    });
});

$('#id_titulo').keyup(function(){
    var query;
    query = $(this).val();
    $('#collapseQsts').show();
    $("#newquestion").show();
    $("#collapseDetails").hide();
    $.get('/sugerir-pergunta/', {suggestion: query}, function(data){
    $('#collapseQsts').html(data);
    });
});




// Ask to answer
$('.ask-answer').click(function(){
    questid = $(this).attr("data-questid");
    userid = $(this).attr("data-userid");
    var $th = $(this);

    $.get('/pedir-resposta/', {pergunta_id: questid, user_id: userid}, function(data){
            $th.addClass( 'active' ).html('Feito!');
        });
});


// add or remove topics in user knowledge
$('body').on('click', '.add_topic_know', function(){
    var topicid = $(this).attr("data-topicid");
    var $th = $(this);
    
    // if it is to add, remove warning class and add success
    if($th.hasClass('btn-default')) {
        $.get('/perfil/add-topic-known/', {topic_id: topicid}, function(data){
            $th.parent().hide();
        });
        $.get('/conhecimentos-atuais/', {}, function(data){
             $('#currentTopics').html(data);
        });
        $.get('/atualiza-sugestoes/', {}, function(data){
            $('#topicsSuggestions').html(data);
        });
    }
    // if is to remove, add warning class and remove success
    else {
        $.get('/perfil/remove-topic-known/', {topic_id: topicid}, function(data){
            $th.parent().hide();
        });
        $.get('/conhecimentos-atuais/', {}, function(data){
            $('#currentTopics').html(data);
        });
        $.get('/atualiza-sugestoes/', {}, function(data){
            $('#topicsSuggestions').html(data);
        });
    };
});



// Sugest topics of knowledge
$(function(){
    $("#topicSearch").hide();
});

$('#searchTopic').keyup(function(){
    var query;
    query = $(this).val();
    $('#topicSearch').show();
    $.get('/buscar-topicos/', {suggestion: query}, function(data){
        $('#topicSearch').html(data);
        $('#newTopic').html(query);
    });
});


// Create new topic and add to user knowledge
$('body').on('click', '.create_new_topic_known', function(){
    var topic = $('#newTopic').text();
    var $th = $(this);
    $.get('/criar-topico-conhecimento/', {topic_name: topic}, function(data){
        $th.parent().hide();
    });
    $.get('/conhecimentos-atuais/', {}, function(data){
        $('#currentTopics').html(data);
    });
    $.get('/atualiza-sugestoes/', {}, function(data){
        $('#topicsSuggestions').html(data);
    });

});







}); // document ready