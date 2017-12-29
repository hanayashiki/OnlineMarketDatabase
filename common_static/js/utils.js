utils = {
    jumpAndLink: function(node, dst) {
        console.log("jal");
        node.click(function() {
            $(location).attr('href', dst + "?" + "from=" + window.location.href);
        });
    },
    jump: function(node, dst) {
        console.log("j");
        node.click(function() {
            $(location).attr('href', dst);
        });
    },
    navigateLink: function(dst) {
        $(location).attr('href', dst + "?" + "from=" + window.location.href);
    },
    navigate: function(dst) {
        $(location).attr('href', dst);
    },
    navigateSafe: function(dst) {
        if (dst === null) {
            this.navigate("home.html");
        } else {
            this.navigate(dst);
        }
    },
    navigateNext: function(dst, next) {
        $(location).attr('href', dst + "?" + "from=" + next);
    },
    checkEmail: function(str) {
        var regExp = /\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*/;
        return regExp.test(str);
    },
    status_dict: {
        "wait": "未处理",
        "done": "已处理"
    },
    order_status_dict: {
        "unpaid": "未处理",
        "paid": "已付款",
        "sent": "已发货",
        "got": "已接收"
    },
    home_page: "home.html",
    user_type: "tourist",
    privilege_action_list: {"manager":[], "tourist": [], "customer": []},
    space: function (len) {
        return new Array(len + 1).join("&nbsp;");
    },
    getUserType: function() {
        var that = this;
        $.getJSON("/getPrivilege/", {}, function(data, status) {
            console.log("I am " + data['user_type']);
            console.log("manager_id: " + data['manager_id']);
            console.log("user_id: " + data['user_id']);
            that.user_type = data['user_type'];
            console.log(that.user_type);
            var action_list = that.privilege_action_list[that.user_type];
            for (var idx = 0; idx < action_list.length; idx++) {
                action_list[idx]();
            }
        });
    },
    seeOnPrivilege: function(node, user_type) {
        node.hide();
        this.privilege_action_list[user_type].push(function() {node.show()});
    },
    hideOnPrivilege: function(node, user_type) {
        node.hide();
        this.privilege_action_list[user_type].push(function() {node.hide()});
    },
    strVecAdd: function(str_vec1, mid, str_vec2) {
        var str_vec = [];
        for (var i = 0; i < str_vec1.length; i++) {
            str_vec.push(str_vec1[i] + mid + str_vec2[i]);
        }
        console.log(str_vec);
        return str_vec;
    }
};

$(document).ready(function() {

    var navigator = [
        '<header class="header">',
        '<div class="header-inner body-width">',
          '<a href=\"javascript:;\" class="logo"></a>',

          '<nav class=\"header-nav\">',
            '<ul>',
              '<li id="backend_order">',
                '<span class=\"line\"></span>',
                '<a href=\"javascript:;\" class=\"dreamer\">处理订单</a>',
              '</li>',
              '<li id="backend_cmplt">',
                '<span class=\"line\"></span>',
                '<a href=\"javascript:;\" class=\"dreamer\">处理投诉</a>',
              '</li>',
              '<li id=\"shopping_list\">',
                '<span class=\"line\"></span>',
                '<a href=\"javascript:;\" class=\"dreamer\" id=\"shopping_list\">查看购物车</a>',
              '</li>',
              '<li id=\"register\">',
                '<span class=\"line\"></span>',
                '<a href=\"#\" class=\"icon-text__pink register\">注册</a>',
              '</li>',
              '<li id=\"login\">',
                '<span class=\"line\"></span>',
                '<a href=\"javascript:;\" id=\"login_btn\">登录</a>',
              '</li>',
              '<li id=\"logout\">',
                '<span class=\"line\"></span>',
                '<a href=\"javascript:;\" id=\"logout_btn\">注销</a>',
              '</li>',
            '</ul>',
          '</nav>',
        '</div>',
        '<div class=\"header-shadow\"></div>',
      '</header>'].join('');

    $("body").prepend(navigator);

    var complaint_node = $("#backend_cmplt");
    var order_node = $("#backend_order");

    $(".logo").click(function() {
        $(location).attr('href', 'home.html');
    });
    $("#shopping_list").click(function() {
        $(location).attr('href', 'shoppingList.html');
    });
    complaint_node.click(function() {
        $(location).attr('href', 'managerComplaint.html');
    });
    order_node.click(function() {
        $(location).attr('href', 'managerOrder.html');
    });
    $(".register").click(function() {
        $(location).attr('href', 'register.html');
    });
    $("#logout_btn").click(function() {
        $.getJSON("/logout/", {}, function(data, status) {
            if (status === "success") {
                if (data['info'] === 'logout') {
                    alert("注销成功！");
                    $(location).attr('href', 'home.html');
                }
            }
        });
    });
    utils.jumpAndLink($("#login_btn"), "login.html");

    utils.seeOnPrivilege(complaint_node, "manager");
    utils.seeOnPrivilege(order_node, "manager");
    utils.seeOnPrivilege($("#logout"), "manager");
    utils.seeOnPrivilege($("#logout"), "customer");
    utils.seeOnPrivilege($("#shopping_list"), "customer");
    utils.seeOnPrivilege($("#register"), "tourist");
    utils.seeOnPrivilege($("#login"), "tourist");

    utils.getUserType();

});
