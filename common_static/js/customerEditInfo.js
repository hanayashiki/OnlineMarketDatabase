$(document).ready(function () {
    var pw_len = 6;
    var username = $("#username").val();
    var password = $("#password").val();
    var repeat_password = $("#repeat_password").val();
    var address = $("#address").val();
    var telephone = $("#telephone").val();
    var email = $("#email").val();

    var back_addr = $.getUrlParam("from");
    if (back_addr === null) {
        back_addr = utils.home_page;
    }

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
            return false;
        }
        else if (password !== repeat_password) {
            alert("请确保两次输入的密码一致。");
            $("#repeat_password").val("");
            $("#repeat_password").focus();
            return false;
        }
        else if (username.trim().length === 0) {
            alert("用户名不能为空。");
            return false;
        }
        else if (address.trim().length === 0) {
            alert("地址不能为空。");
            $("#address").focus();
            return false;
        }
        else if (isNaN(parseInt(telephone, 10))) {
            alert("电话号码不合法。");
            return false;
        }
        else if (!utils.checkEmail(email)) {
            alert("邮箱不合法。");
            return false;
        }
        return true;
    }

    function getCustomerInfo() {
        $.getJSON("/getCustomerInfo", {}, function(data, status) {
            if (status === 'success') {
                $("#username").val(data["username"]);
                $("#address").val(data["address"]);
                $("#telephone").val(data["telephone"]);
                $("#email").val(data["email"]);
            }
        });
    }

    $("#user_edit_btn").click(function() {
        if (check_validity()) {
            $.getJSON("/editCustomerInfo/",
                {
                    "username": username,
                    "email": email,
                    "address": address,
                    "telephone": telephone,
                },
                function (data, status) {
                    if (status === "success") {
                        var info = data['info'];
                        if (info === "success") {
                            alert("修改成功！");
                            utils.navigateSafe(back_addr);
                        } else {
                            alert("您的用户名、邮箱或电话已经被注册了。");
                            $("#username").focus();
                        }
                    }
                });
        }
    });

    getCustomerInfo();
});