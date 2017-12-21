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
    }
};

$(document).ready(function() {
    $(".dreamer, .logo").click(function() {
        $(location).attr('href', 'home.html');
    });
    $(".register").click(function() {
        $(location).attr('href', 'register.html');
    });
    utils.jumpAndLink($("#login_btn"), "login.html");
});
