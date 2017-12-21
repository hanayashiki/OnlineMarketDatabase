utils = {
    jumpAndLink: function(node, dst) {
        console.log("jal");
        console.log(node.text());
        console.log(dst);
        node.click(function() {
            $(location).attr('href', dst + "?" + "from=" + window.location.href)
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
});
