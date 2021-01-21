$(document).ready(function () {
	$(document).off("keypress");
	$(document).on("keypress", function (event) {
		if (event.keyCode == 13) {
			$("#sb-login_btn").click();
		};
	});

});


$("#sb-login_btn").off("click");
$("#sb-login_btn").on("click", function () {
	var postData = {};
	postData['username'] = $('#sb-username').val();
	postData['password'] = $('#sb-password').val();

	if (postData.username && postData.password) {
		$.ajax({
			url: extendedUrl + "/sessions",
			type: "POST",
			data: JSON.stringify(postData),
			success: function (data) {
				$.cookie('sb_username', data.username);
				$.cookie('sb_loggedin-time', moment().format());
				$.cookie('sb_user_id', data._id);
				$.cookie('sb_session_id', data.session_id);
                $('#sb_content').load('pages/home.html');
				localStorage.setItem('loginItem', "supportbundle");
			},
			error: function (xhr) {
				$.alertable.alert("username or password  are invalid");
				return false;
			}
		});
	} else if (postData.username == "" && postData.password == "") {
		$.alertable.alert("Empty Username and Password");
	} else if (postData.username == "" && postData.password != "") {
		$.alertable.alert("Empty Username");
	} else {
		$.alertable.alert("Empty Password");
	}
});





