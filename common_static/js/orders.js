$(document).ready(function () {

    function addOrderEntryNode(order_id, good_list, status, date, total) {
        var new_order_entry = $("<li></li>");
        new_order_entry.attr('class', 'complaint order_entry');

         var button_node = $("<button></button>");
        button_node.attr({
            'class': 'info_btn'});
        button_node.text("我要投诉");
        utils.jumpAndLink(button_node, "/static/complaint.html");
        new_order_entry.append(button_node);

        var new_id_node = $("<p></p>");
        new_id_node.attr('class', 'status');
        new_id_node.text('订单号：'+order_id);
        new_order_entry.append(new_id_node);

        var new_good_list_node = $("<p></p>");
        var good_str = "商品：";
        good_str += good_list.join("，")

        new_good_list_node.text(good_str);
        new_good_list_node.attr('class', 'status');
        new_order_entry.append(new_good_list_node);

        var status_node = $("<p></p>");
        var status_str = "状态：" + utils.order_status_dict[status];
        status_node.text(status_str);
        status_node.attr('class', 'status');
        new_order_entry.append(status_node);

        var date_node = $("<p></p>");
        date_node.text("下单日期：" + date);
        date_node.attr('class', 'status');
        new_order_entry.append(date_node);

        var total_node = $("<p></p>")
        total_node.text("总金额：" + total + "￥");
        total_node.attr('class', 'status');
        new_order_entry.append(total_node);

        $(".complaint_entry_inner").append(new_order_entry);
    }

    function getOrderEntryNodes() {
        console.log("get entries");
        $.getJSON("/orderEntry", {}, function(data, status) {
            if (status === "success") {
                console.log("list len:" + data.length);
                $.each(data, function(idx, info) {
                    addOrderEntryNode(info['order_id'], info['good_names'],
                        info['status'], info['submit_date'],
                        info['total']);
                    console.log(info['good_names']);
                    console.log(info['total']);
                })
            }
        });
    }

    getOrderEntryNodes();

    addOrderEntryNode(123456, ["手机", "电视", "大哥大"], "sent", "2016/1/1", 1000);
});