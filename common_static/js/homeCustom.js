$(document).ready(function() {
    var complaint_length_limit = 25;
    var status_dict = {
        "wait": "<span style=\"color:blue\">未处理</span>",
        "done": "<span style=\"color:red\">已处理</span>"
    };
    
    $.getJSON("/customerInfoDisplay", function(data, status) {
        if (status === "success") {
            var name = data["name"];
            if (name.length > 0) {
                var customer_id = data["id"];
                $("#greetings").text("欢迎您！尊敬的" + name + "。");
                $("#customer_id").text("您的 id 是：" + customer_id + "。");
            } else {
                $("#greetings").text("欢迎您！您还没有登录。");
                $("#customer_id").append("请<a href='login.html'>登录</a>以获得更好的购物体验。");
            }
        }
    });

    $.getJSON("/complaintDisplay", function(data, status) {
        if (status === "success") {
            $.each(data, function(idx, info) {
                if (idx >= 5) return;
                var text = info["text"];
                var submit_date = info["submit_date"];
                var status = info["status"];
                var complaint_id = info["complaint_id"];

                if (text.length >= complaint_length_limit) {
                    text =　text.substring(0, complaint_length_limit - 3) + "..."
                }
                status = status_dict[status];
                console.log(status)

                addComplaintEntry(complaint_id, text, "/static/complaintEntry.html", submit_date, status);
            })
        }
    });

    $('#orders_btn').click(function (){
        if (utils.user_type === "customer") {
            utils.navigate("orders.html");
        } else if (utils.user_type === "manager") {
            alert("只有顾客才能查看订单。");
        } else {
            utils.navigateNext("login.html", "orders.html");
        }
    });

    $('#check_complaint_btn').click(function () {
        if (utils.user_type === "customer") {
            utils.navigate("allComplaintEntries.html");
        } else if (utils.user_type === "manager") {
            alert("只有顾客才能查看投诉信息。");
        } else {
            utils.navigateNext("login.html", "allComplaintEntries.html");
        }
    });

    $('#edit_info_btn').click(function () {
        if (utils.user_type === "customer") {
            utils.navigate("customerEditInfo.html");
        } else if (utils.user_type === "manager") {
            alert("只有顾客才能修改个人信息");
        } else {
            utils.navigateNext("login.html", "customerEditInfo.html");
        }
    });

    function addComplaintEntry(cmplt_id, text, link, date, status) {
        var new_node = $("<li></li>");
        new_node.attr({
            "class": "complaint_entry"
        });

        var new_table = $("<table></table>");
        new_table.attr({
            "border": 0
        });


        var new_line = $("<tr></tr>");

        var text_col = $("<td></td>");
        text_col.attr({
            "class": "text"
        });
        var new_link = $("<a></a>");
        new_link.attr({
            "href": "javascript:;",
            "cmplt_id": cmplt_id
        });
        new_link.click(function() {
            var id = $(this).attr("cmplt_id");
            window.location.href = link + "?" + "complaint_id=" + id;
        });
        new_link.append(text);
        text_col.append(new_link);
        new_line.append(text_col);

        var date_col = $("<td></td>");
        date_col.attr({
            "class": "date"
        });
        date_col.append(date);
        new_line.append(date_col);

        var status_col = $("<td></td>");
        status_col.attr({
            "class": "status"
        });
        status_col.append(status);
        new_line.append(status_col);

        new_table.append(new_line);

        new_node.append(new_table);

        $("#complaint_display").append(new_node);
    }

    addComplaintEntry(123, "是的，遍历处理data，可以是数组、DOM、...",
        "/static/complaintEntry.html", "2017/12/2", status_dict["done"]);

    //$.getJSON("")
});