$(document).ready(function() {
   var exclaiming_buy = "加入购物车！";
   var price_tag = "价格：￥";
   var remain_tag = "库存：";
   var info_dict = {
       "success": "成功",
       "failure": "失败"
   };
   var category_list = [
       "所有类别",
       "键盘",
       "鼠标",
       "电脑",
       "手机",
       "耳机",
       "音箱"
   ];

   function addGoodEntry(pic_src, good_name, good_id, price, remain) {
       var item_node = $("<li></li>");
       item_node.attr({
           "class": "item"
       });

       var img_node = $("<div></div>");

       img_node.css({
           "width": "224px",
           "height": "224px",
           "background": "url(" + pic_src + ")",
           "background-size": "cover",
           "background-repeat": "no-repeat"
       });

       item_node.append(img_node);


       var div_node = $("<div></div>");
       div_node.attr({
           "class": "info"
       });


       var title_node = $("<p></p>");
       title_node.text(good_name);
       title_node.attr({
           "class": "title"
       });
       div_node.append(title_node);

       var table_node = $("<table></table>");
       table_node.attr({
           "border": 0
       });


       var line_node = $("<tr></tr>");

       var price_node = $("<td></td>");
       price_node.text(price);
       price_node.attr({
           "class": "price"
       });
       var remain_node = $("<td></td>");
       remain_node.text(remain);
       remain_node.attr({
           "class": "remain"
       });
       line_node.append(price_node, remain_node);
       table_node.append(line_node);
       div_node.append(table_node);

       var btn_node = $("<button></button>");
       btn_node.text(exclaiming_buy);
       btn_node.attr({
           "good_name": good_name,
           "good_id": good_id,
           "type": "button",
           "class": "info_btn"
       });
       btn_node.click(function () {
           var good_id = $(this).attr("good_id");
           var good_name = $(this).attr("good_name");
           $.getJSON("/addGood", {"good_id": good_id}, function(data, status) {
              if (status === "success") {
                  alert("购买商品" + good_name + ": " + info_dict[data["info"]]);
              }
           });
       });
       div_node.append(btn_node);

       item_node.append(div_node);


       $(".main-contmain-cont .main-cont__list").append(item_node);
       console.log("New good display");
   }

   function loadGoods(category) {
       $.getJSON("/goodDisplay", {"category": category}, function(data, status) {
           if (status === "success") {
               clearGoods();
               $.each(data, function (infoIndex, info) {
                   var good_id = info["good_id"];
                   var name = info["name"];
                   var price = price_tag + info["price"];
                   var image_path = info["image_path"];
                   var remain = remain_tag + info["remain"];
                   addGoodEntry(image_path, name, good_id, price, remain);
               });

           }
       })
   }

   function clearGoods() {
       "use strict";
       $(".main-contmain-cont .main-cont__list").empty();
   }

   var select_node = $(".main-contmain-cont .main-cont__title .category .selector");
   select_node.empty();

   for (var idx = 0; idx < category_list.length; idx++) {
       var option_node = $("<option></option>");
       option_node.attr({
           "value": category_list[idx]
       });
       option_node.text(category_list[idx]);
       /*option_node.click(function() {
           "use strict";
           var val = $(this).attr("value");
           clearGoods();
           loadGoods(val);
       });*/
       select_node.append(option_node);
   }

   select_node.change(function() {
       var selected_opt = select_node.find("option:selected");
       var val = selected_opt.attr("value");
       loadGoods(val);
       $('html,body').animate({scrollTop:select_node.offset().top - select_node.width()},'slow');
       console.log($(window).scrollTop())
   });

   clearGoods();
   loadGoods(category_list[0]);

   $("#search_btn").click(function () {
       var keyword = $(".search .search-text").val();
       var selected_opt = select_node.find("option:selected");
       var category = selected_opt.attr("value");
       console.log(keyword);
       console.log(category);
       /*$.getJSON("/search", {"category": category, "keyword": keyword}, function(data, status) {
           "use strict";

       })*/
   })

   // addGoodEntry("/static/images/cont/main_img6.jpg", "野兽先辈", 123, "价格：￥114", "库存：514件");
   // loadGoods("xxx");
});