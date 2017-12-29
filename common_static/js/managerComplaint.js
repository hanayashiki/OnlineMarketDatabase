$(document).ready(function () {
    function addComplaintNode(status, complaint_id, submit_date, customer_name, customer_id, content) {
        var complaint_node = $("<li></li>");
        complaint_node.attr('class', 'complaint');
        {
            var button_node = $("<button></button>");
            button_node.attr({
                'class': 'info_btn',
                'id': 'handle_btn'
            });
            button_node.text("处理");
            utils.jump(button_node, "managerComplaintEntry.html?" + "complaintId=" + complaint_id);
            complaint_node.append(button_node);
        }
        {
            var status_node = $("<p></p>");
            status_node.attr('class', 'status');
            status_node.text(utils.status_dict[status]);
            complaint_node.append(status_node);
        }
        {
            var complaint_id_node = $("<p></p>");
            complaint_id_node.attr('class', 'status');
            complaint_id_node.text("提交编号：" + complaint_id);
            complaint_node.append(complaint_id_node);
        }
        {
            var submit_date_node = $("<p></p>");
            submit_date_node.attr('class', 'status');
            submit_date_node.text("提交日期：" + submit_date);
            complaint_node.append(submit_date_node);
        }
        {
            var customer_node = $("<p></p>");
            customer_node.attr('class', 'status');
            customer_node.append("用户：" + customer_name + "&nbsp;&nbsp;&nbsp;&nbsp;编号：" + customer_id);
            complaint_node.append(customer_node);
        }
        {
            var separator_node = $("<hr>");
            complaint_node.append(separator_node);
        }
        {
            var content_node = $("<p></p>");
            content_node.attr('class', 'content');
            content_node.text(content);
            complaint_node.append(content_node);
        }
        $(".complaint_entry_main .complaint_entry_inner").append(complaint_node);
    }
    /*addComplaintNode("wait", 12345, "2017/1/1", "远野后辈", 810810,
        　"近年来，随着我国经济社会的快速发展，在办理经济犯罪案件中，涉案财物种类繁杂、数额巨大、涉及面广，处置难度在加大，也面临一些新问题。如何规范涉案财物处置程序，确保在严格依法办案的前提下，既保持打击犯罪的“力度”，又注重文明执法的“温度”，最高检、公安部在新规定中作出了明确要求。");
    */
    function getComplaintNodes() {
        $.getJSON("/getComplaintWork", {}, function(data, status) {
            if (status === "success") {
                $.each(data, function(idx, info) {
                    addComplaintNode(
                        info['status'],
                        info['complaint_id'],
                        info['submit_date'],
                        info['customer_name'],
                        info['customer_id'],
                        info['text']
                    );
                });
            }
        });
    }

    utils.seeOnPrivilege($("body"), "manager");

    getComplaintNodes();
});