$(document).ready(function () {
    var pw_len = 6;
    var username = $("#username").val();
    var password = $("#password").val();
    var repeat_password = $("#repeat_password").val();
    var address = $("#address").val();
    var telephone = $("#telephone").val();
    var email = $("#email").val();

    var back_addr = $.getUrlParam("from");
    function check_validity() {
        username = $("#username").val();
        password = $("#password").val();
        repeat_password = $("#repeat_password").val();
        address = $("#address").val();
        telephone = $("#telephone").val();
        email = $("#email").val();
        // check pw
        if (password.length < pw_len) {
            alert("密码不应短于 " + pw_len + " 位");
        }
        else if (password !== repeat_password) {
            alert("请确保两次输入的密码一致。");
            $("#repeat_password").val("");
            $("#repeat_password").focus();
        }
        else if (username.trim().length === 0) {
            alert("用户名不能为空。");
        }
        else if (address.trim().length === 0) {
            alert("地址不能为空。");
            $("#address").focus();
        }
        else if (isNaN(parseInt(telephone, 10))) {
            alert("电话号码不合法。");
        }
        else if (!utils.checkEmail(email)) {
            alert("邮箱不合法。");
        }
    }

    $("#user_register_btn").click(function() {
        check_validity();
        $.post("/register/",
            {
                "name": username,
                "email": email,
                "address": address,
                "telephone": telephone,
                "password": password,
                "confirm_password": password
            },
            function (data, status) {
                if (status === "success") {
                    var info = data['info'];
                    if (info === "success") {
                        alert("注册成功！");
                        $(location).attr('href', back_addr);
                    } else {
                        alert("该用户名已经被注册了。");
                        $("#username").focus();
                    }
                }
            });

    });
});