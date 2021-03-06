$(document).ready(function () {
    var complaint_seq_node = $(".complaint_entry_inner");
    var complaint_id = $.getUrlParam("complaintId");
    var last_complaint_id = complaint_id;


    function addComplaintNode(status, date, content, response) {
        var new_complaint_node = $("<li></li>");
        new_complaint_node.attr('class', 'complaint');

        var new_status_node = $("<p></p>");
        new_status_node.attr('class', 'status');
        new_status_node.text(utils.status_dict[status]+" "+date);
        new_complaint_node.append(new_status_node);

        var new_content_node = $("<p></p>");
        new_content_node.attr('class', 'content');
        new_content_node.text(content);
        new_complaint_node.append(new_content_node);

        if (status === "done") {
            var sep_node = $("<hr>");
            sep_node.attr('class', 'separator');
            new_complaint_node.append(sep_node);

            var reply_node = $('<p></p>');
            reply_node.attr('class', 'status');
            reply_node.text("回复：");
            new_complaint_node.append(reply_node);

            var reply_content_node = $('<p></p>');
            reply_content_node.attr('class', 'content');
            reply_content_node.text(response);
            new_complaint_node.append(reply_content_node);
        }
        complaint_seq_node.append(new_complaint_node);
    }

    /*
    addComplaintNode("done", "2017/11/7",
        "该网友称：“邹市明及妻子到达上海虹桥机场，但是小妖发现此次现身机场的邹市明，身体方面出现了一些问题。邹市明走路需要妻子冉莹颖和助理搀扶，在遇到一个柱子时，邹市明并没有发现前方有异物直接撞了上去，视力明显出了问题。”目前邹市明已经被送往上海长征医院。",
        "近日，杜江、霍思燕、嗯哼一家三口亮相机场，嗯哼坐在行李箱上，爸爸妈妈在一旁保驾护航。嗯哼小小年纪就派头十足简直是戏精本人啦，临走前还突然回头向记者问好，超会圈粉。");

    addComplaintNode("done", "2017/11/7",
        "该网友称：“邹市明及妻子到达上海虹桥机场，但是小妖发现此次现身机场的邹市明，身体方面出现了一些问题。邹市明走路需要妻子冉莹颖和助理搀扶，在遇到一个柱子时，邹市明并没有发现前方有异物直接撞了上去，视力明显出了问题。”目前邹市明已经被送往上海长征医院。",
        "近日，杜江、霍思燕、嗯哼一家三口亮相机场，嗯哼坐在行李箱上，爸爸妈妈在一旁保驾护航。嗯哼小小年纪就派头");
    */

    function getComplaintNodes() {
        $.getJSON("/getComplaintEntry/", {"complaint_id": complaint_id},
            function (data, status) {
                if (status === "success") {
                    $.each(data, function(idx, data) {
                        var entry_status = data['status'];
                        var date = data['submit_date'];
                        if (entry_status === "done") {
                            date = data['proceed_date'];
                        }
                        var text = data['text'];
                        var reply = data['reply'];

                        last_complaint_id = complaint_id;

                        addComplaintNode(entry_status, date, text, reply);
                    })
                }
            })
    }

    var text_area = $("#content");

    var min_len = 15;
    var max_len = 1000;
    $("#complaint_btn").click(function () {
        var complaint_str = text_area.val();
        var len = complaint_str.length;
        if (len < min_len) {
            alert("请更加详细地描述一下您的状况。");
        } else if (len > max_len) {
            alert("您的投诉过长，请分段提交。");
        } else {
            $.post("/addComplaint/", {"text": complaint_str, "complaint_id": last_complaint_id},
                function (data, status) {
                    if (status === "success") {
                        if (data['info'] === "success") {
                            alert("提交成功！您的投诉我们将尽快处理！");
                            window.location.reload();
                        }
                    }
                })
        }
    });

    getComplaintNodes();
});