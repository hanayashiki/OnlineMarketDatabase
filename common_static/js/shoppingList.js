$(document).ready(function () {
    function addShoppingListEntry(good_id, good_name, good_price, good_num) {
        var list_node = $(".shopping_list table");

        var good_entry_node = $("<tr></tr>");
        good_entry_node.attr('class', 'good_entry');

        {
            var good_id_col = $("<td></td>");
            good_id_col.attr('class', 'good_id');
            good_id_col.text("编号：" + good_id);
            good_entry_node.append(good_id_col);
        }
        {
            var good_name_col = $("<td></td>");
            good_name_col.attr('class', 'good_name');
            good_name_col.text("商品名：" + good_name + " * " + good_num);
            good_entry_node.append(good_name_col);
        }
        {
            var good_price_col = $("<td></td>");
            good_price_col.attr('class', 'good_price');
            good_price_col.text("单价：" + good_price + "￥");
            good_entry_node.append(good_price_col);
        }
        list_node.prepend(good_entry_node);
    }

    //addShoppingListEntry(114514, "昏睡红茶", 24)
    $('.shopping_list .total_entry .total').text("合计：" + 15 + "￥");
    function getShoppingListEntries() {
        $.getJSON('/getShoppingList', {}, function(data, status) {
            if (status === 'success') {
                var total = 0;
                $.each(data, function(idx, info) {
                    addShoppingListEntry(info['good_id'], info['name'], info['price'], info['good_num']);
                    total += info['price'];
                });
                $('.shopping_list .total_entry .total').text("合计：" + total + "￥");
            }
        });
    }

    getShoppingListEntries();
});