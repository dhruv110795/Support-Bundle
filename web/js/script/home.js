$(document).ready(function() {
    getProjectName();
    // getRecentDownloadInfo();
    $(".sb-schedule-data").hide();
    $("#sb_mongodump").prop("checked", true);
    $("#sb_app_logs").prop("checked", true);
    $("#sb_sys_logs").prop("checked",true);
    $("#sb_error").hide();


    $("#sb_download_bundle").off("click");
    $("#sb_download_bundle").on("click", function(){
        var downloadURL = "?project=" + $("#sb_project_name").val();
        if($("#sb_mongodump").is(":checked")){
            downloadURL = downloadURL + "&mongo_dump=true";
        }
        if($("#sb_sys_logs").is(":checked")){
            downloadURL = downloadURL + "&sys_log_dump=true";
        }
        if($("#sb_app_logs").is(":checked")){
            downloadURL = downloadURL + "&app_log_dump=true";
        }
        // console.log(extendedUrl + "/support_bundle" + downloadURL);
        // var $preparingFileModal = $("#preparing-file-modal");
        // $preparingFileModal.dialog({ 
        //     modal: true ,
        //     open: function(){
        //         $(".ui-dialog-titlebar-close").text("X").css({ "color": "#000", "padding": "0px" });
        //     }
        // });
        $(".sb-download-button-div").hide();
        $(".sb-loading-div").show();
        $("#sb_error").hide();
        $.fileDownload( extendedUrl + "/support_bundle" + downloadURL,{
            successCallback: function(url) {
                // $preparingFileModal.dialog('close');
                $(".sb-download-button-div").show();
                $(".sb-loading-div").hide();
                $("#sb_error").hide();
            },
            failCallback: function(responseHtml, url) {
                $(".sb-download-button-div").show();
                $(".sb-loading-div").hide();
                $("#sb_error").show();
            },
        });
        return false;
    });
});

function getProjectName(){
    $.ajax({
        type: "GET",
        url: extendedUrl +"/config",
        success: function(data){
            var clientName = data["config"]["client_name"];
            if(clientName){
                $("#sb_client").text(clientName);
            }
            var enabledProject = data["config"]['enabled_projects'];
            var projectDropdown = '';
            if(enabledProject){
                for(var i=0;i<enabledProject.length;i++){
                    var projectName = enabledProject[i];
                    projectDropdown += '<option value='+projectName+ '>'+projectName+'</option>';
                }

                $("#sb_project_name").html(projectDropdown);
                $("#sb_project_name").val($("#sb_project_name option:first").val());
            }
        },
        error: function(error){
            if(error.status == 401){
                $.removeCookie('sb_username');
                $.removeCookie('sb_loggedin-time');
                $.removeCookie('sb_session_id');
                $.removeCookie('sb_user_id');
                if(!$.cookie('sb_user_id')){
                    $("#sb_content").load('sb-login.html');
                }else{
                    $("#sb_content").load('pages/home.html');
                }
            }
        }
    });
}

// function getRecentDownloadInfo(){
//     $.ajax({
//         type: "GET",
//         url: extendedUrl + "/recent_dumps",
//         success: function(data){
//             var recentDownloadedDumpInfo = data["dumps"];
//             var recentDumpData = '';
//             if(recentDownloadedDumpInfo.length > 1){
//                 for(var i=0;i<recentDownloadedDumpInfo.length;i++){
//                     console.log(">>>>>>>>>>>>>>>>>>>>>>",recentDownloadedDumpInfo[i]);
//                     var recentDumpItem = recentDownloadedDumpInfo[i];
//                     recentDumpData +=  '<div class="sb-recent-item"><div class="col-md-1 sb-recent-item-div1"><span class="sb-project-name-label" id="sb_recent_project_name">'+ recentDumpItem["project"][0] +'</span></div><div class="col-md-11 sb-recent-item-div2" ><span class="sb-recent-filename" data-path="'+ recentDumpItem["path"]  +'">'+ recentDumpItem["file_name"]  +'</span></div><div class="sb-recent-item-div3"><div class="col-md-9" style="padding-left: 2% !important; margin: 0px;"><span id="sb_recent_time" style="padding-right: 3%;">'+  recentDumpItem["time"]  +'</span><span id="sb_recent_day">'+ recentDumpItem["day"]  +'</span></div><div class="col-md-2" style="padding: 0px;margin: 0px;"><span id="sb_recent_download">Download</span></div></div></div>';
//                 }
//                 $(".sb-recent-data").html(recentDumpData);
//             };
//         },
//     });
// }