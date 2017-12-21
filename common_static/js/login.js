$(document).ready(function () {
    var name_node = $("#name");
    var pw_node = $("#password");
    var btn_node = $("#user_login_btn");
    var name = name_node.val();
    var pw = pw_node.val();

    var back_addr = $.getUrlParam("from");
    var server_flag = false;
    console.log(back_addr);
    btn_node.click(function() {
        $.post("/login/", {"name": name, "password": pw}, function(data, status) {
            server_flag = true;
            if (status === "success") {
                var info = data["info"];
                if (info === "success") {
                    alert("登录成功！");
                    $(location).attr('href', back_addr);
                } else {
                    alert("用户名或密码错误。");
                }
            } else {
                alert("登录失败。");
            }
            console.log(back_addr);
        })
    });
});