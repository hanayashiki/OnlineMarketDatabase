$(document).ready(function () {
    var min_len = 15;
    var max_len = 1000;
    var back_addr = $.getUrlParam("from");
    var text_area = $("#content");
    $("#complaint_btn").click(function () {
        var complaint_str = text_area.val();
        var len = complaint_str.length;
        if (len < min_len) {
            alert("请更加详细地描述一下您的状况。");
        } else if (len > max_len) {
            alert("您的投诉过长，请分段提交。");
        } else {
            $.post("/submitComplaint/", {"text": complaint_str},
                function(data, status) {
                    if (status === "success") {
                        if (data['info'] === "success") {
                            alert("提交成功！您的投诉我们将尽快处理！");
                            $(location).attr('href', back_addr);
                        }
                    }
                })
        }
    });
});