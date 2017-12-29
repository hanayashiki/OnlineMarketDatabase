$(document).ready(function() {
    function addOrderEntry(order_id, customer_name, customer_id,
        good_list, good_nums, status, submit_date, total) {
        var order_entry_node = $("<li></li>");
        order_entry_node.attr('class', 'complaint order_entry');
        {
            var order_id_node = $("<p></p>");
            order_id_node.attr('class', 'status');
            order_id_node.text("订单号：" + order_id);
            order_entry_node.append(order_entry_node);
        }
        {
            var customer_node = $("<p></p>");
            customer_node.attr('class', 'status');
            customer_node.append("下单客户：" + customer_name + utils.space(4) +
                "客户编号：" + customer_id);
            order_entry_node.append(customer_node)
        }
        {
            var button_node = $("<button></button>");
            button_node.attr({
                'class': 'info_btn',
                'id': 'user_complaint_btn',
                'order_id': order_id
            });
            button_node.text("修改订单状态");
            order_entry_node.append(button_node);
        }
        {
            var good_list_node = $("<p></p>");
            good_list_node.attr('class', 'status');
            var list_str = "商品：";
            list_str += utils.strVecAdd(good_list, " * ", good_nums).join("、");
            good_list_node.text(list_str);
            order_entry_node.append(good_list_node);
        }
        {
            var status_node = $("<p></p>");
            status_node.attr('class', 'status');
            status_node.attr('id', 'order_status');
            status_node.text("状态：" + utils.order_status_dict[status]);
            order_entry_node.append(status_node);
        }
        {
            var submit_date_node = $("<p></p>");
            submit_date_node.attr('class', 'status');
            submit_date_node.text("下单日期：" + submit_date);
            order_entry_node.append(submit_date_node);
        }
        {
            var total_node = $("<p></p>");
            total_node.attr('class', 'status');
            total_node.text("总金额：" + total + "￥");
            order_entry_node.append(total_node);
        }
        {
            var set_status_node = $("<p></p>");
            set_status_node.attr("class", "status");
            set_status_node.text("设置状态：");
            {
                var select_node = $("<select></select>");
                select_node.attr({
                    "title": "设置状态",
                    "class": "select"
                });
                for (var key in utils.order_status_dict) {
                    if (utils.order_status_dict.hasOwnProperty(key)) {
                        var option_node = $("<option></option>");
                        option_node.val(key);
                        option_node.text(utils.order_status_dict[key]);
                        select_node.append(option_node);
                    }
                }
                set_status_node.append(select_node);
            }
            order_entry_node.append(set_status_node);
        }
        button_node.click(function() {
            var selected_opt = set_status_node.find("option:selected");
            var val = selected_opt.attr("value");
            var id = $(this).attr('order_id');
            console.log(val);
            $.getJSON("/changeOrderStatus",
                {'order_id': id, 'target_status': val},
                function(data, status) {
                    if (status === "success" && data['info'] === "success") {
                        alert("处理成功！");
                        utils.navigate(window.location.href);
                    }
                });
        });
        $(".complaint_entry_main .complaint_entry_inner").append(order_entry_node);
    }

    addOrderEntry(123, "蔡壮忠", 193121, ["冲锋艇", "短校服"], [1, 2], "wait", "1931/1/1", 100);

    $.getJSON("/getOrderWork", {}, function(data, status) {
        if (status === "success") {
            $.each(data, function(idx, info) {
                addOrderEntry(
                    info['order_id'],
                    info['customer_name'],
                    info['customer_id'],
                    info['good_names'],
                    info['good_nums'],
                    info['status'],
                    info['submit_date'],
                    info['total']);
            });
        }
    });

    utils.seeOnPrivilege($("body"), "manager");

});