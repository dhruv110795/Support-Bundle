var extendedUrl = "/service";
// var extendedUrl = ""

$(document).ready(function(){
    if(!$.cookie('sb_session_id')){
        $("#sb_content").load('sb-login.html',function(){
            setTimeout(function(){},3000);
            console.log('loggedin.....');
        });
    }else{
        $("#sb_content").load('pages/home.html',function(){
            setTimeout(function(){},2000);
            console.log('loaded.....');
        });
    }
});


$(document).off("click", "#sb_logout");
$(document).on("click", "#sb_logout", function(){
    $.alertable.confirm("Are you sure you want to sign out ? ").then(function(){
        setTimeout(function(){
            $.ajax({
                url: extendedUrl + "/sessions",
                type:"DELETE",
                success:function(data){
                    $.removeCookie('sb_username');
                    $.removeCookie('sb_loggedin-time');
                    $.removeCookie('sb_session_id');
                    $.removeCookie('sb_user_id');
                    $(".growl").remove();
                    $("#sb_content").load("sb-login.html");
                    
                },error: function(error) {
                    console.log('error...',error);
                }
            });
        }, 500);    
    }, function(){
        console.log("confirmation deleted");
    });    
});