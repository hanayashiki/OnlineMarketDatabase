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
    checkEmail: function(str){
        var regExp = /\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*/;
        return regExp.test(str);
    },
    status_dict: {
        "wait": "未处理",
        "done": "已处理"
    },
    order_status_dict: {
        "wait": "未处理",
        "paid": "已付款",
        "sent": "已发货",
        "received": "已接收"
    },
    space: function (len) {
        return new Array(len + 1).join("&nbsp;");
    },
    seeOnPrivilege: function(node, user_type) {

        node.hide();

        $.getJSON("/getPrivilege/", {}, function(data, status) {
            console.log("I am " + data['user_type']);
            if (status === "success" && data['user_type'] === user_type) {
                node.show();
            }
        });
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
              '<li>',
                '<span class=\"line\"></span>',
                '<a href=\"javascript:;\" class=\"dreamer\" id=\"shopping_list\">查看购物车</a>',
              '</li>',
              '<li>',
                '<span class=\"line\"></span>',
                '<a href=\"#\" class=\"icon-text__pink register\">注册</a>',
              '</li>',
              '<li>',
                '<span class=\"line\"></span>',
                '<a href=\"javascript:;\" id=\"login_btn\">登录</a>',
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
    utils.jumpAndLink($("#login_btn"), "login.html");

    utils.seeOnPrivilege(complaint_node, "manager");
    utils.seeOnPrivilege(order_node, "manager");



});
