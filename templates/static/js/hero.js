// 登陆
$(document).on("submit", "#signin_form", function (ev) {
    ev.preventDefault();
    $.ajax({
        url: '/',
        type: "post",
        data: $(this).serialize(),
        success: function (msg) {
            if (msg == "verify_success") {
                window.location = "/index/"
            }
            else {
                alert(msg)
            }
        }

    })

});

//元素管理--公用
function ele_manager(uri, pro_id) {
    $("#right_bar").empty();
    var url = uri + pro_id;
    console.log(url)
    $.get(url, function (data) {
		$("#right_bar").append(data)
    })
}
//点击元素管理
$(document).on("click", ".element_manager", function () {
    var pro_id = $(this).attr("name");
    ele_manager('/element/?pro_id=', pro_id);
});
//点击用例管理
$(document).on("click", ".case_list", function () {
    var pro_id = $(this).attr("name");
    ele_manager('/case_list/?pro_id=', pro_id)
});
//用例编辑页面点击返回按钮返回用例列表
$(document).on("click", "#back", function () {
    var pro_id = $("#pro_id").val();
    ele_manager('/case_list/?pro_id=', pro_id)
});

//点击执行列表(测试场景)
$(document).on("click", ".case_scenario", function () {
    var pro_id = $(this).attr("name");
    ele_manager('/scenario_list/?pro_id=', pro_id)
});


//点击项目管理
$(document).on("click", ".project_manager", function () {
    //var pro_id = $(this).attr("name");
    ele_manager('/project', '')
});




//排序函数
function Sort_tr() {
    var tr_list = $("#sortable tr");
    for (i = 0; i < tr_list.length; i++) {
        tr_list.eq(i).children().eq(1).text(i + 1);
    }

}

//编号排序
$(document).on("click", "#sort_number", function () {
    Sort_tr();
});


//增加步骤
$(document).on("click", "#add_step", function () {
	console.log("lang")
    $.get("/ajax_html?action=add_case_step", function (data) {
        $("#sortable").append(data);
        Sort_tr();
    })
});
//删除步骤
$(document).on("click", "#delete_step", function () {
    var check_list = $(".checkbox_step:checked");
    if (check_list.length == 0) {
        alert("请勾选要删除的步骤");
    }
    else {
        for (i = 0; i < check_list.length; i++) {
            check_list.eq(i).parents("tr").remove()
        }
        Sort_tr()
    }
});


//新增用例-保存用例
$(document).on("submit", "#add_case_form", function (ev) {
    ev.preventDefault();
    $.ajax({
        url: '/add_case/',
        type: 'post',
        data: $(this).serialize(),
        success: function (data) {
            alert(data);
            if (data == '保存成功') {
                var pro_id = $("#project_id").val();
                ele_manager('/case_list/?pro_id=', pro_id);
            }
        }
    })
});

//编辑用例--保存用例

$(document).on("submit", "#edit_case_form", function (ev) {
    ev.preventDefault();//阻止元素发生默认的行为（例如，当点击提交按钮时阻止对表单的提交）
    $.ajax({
        url: '/edit_case/',
        type: 'post',
        data: $(this).serialize(),
        success: function (data) {
            alert(data);
            if (data == '保存成功') {
                var pro_id = $("#pro_id").val();
                ele_manager('/case_list/?pro_id=', pro_id);
            }
        }
    })
});
//删除用例
$(document).on("click", "#del_case", function () {
    var check_list = $(".checkbox:checked");
    var del_list = [];
    for (i = 0; i < check_list.length; i++) {
        check_list.eq(i).parents("tr").remove();
        del_list.push(check_list.eq(i).attr("name"));
    }
    $.post("/case_list/", {"action": "del_case", "del_list": del_list}, function (data) {
        alert(data)
    })
});

//增加元素--保存  还有编辑元素保存
$(document).on("submit", "#add_element_form", function (ev) {
    ev.preventDefault();
    $.ajax({
        url: '/element/',
        type: 'post',
        data: $(this).serialize(),//获取页面上所有有name属性的元素传给后台处理 key:name value:值 类似于字典
        // var tyoe= data["action"]
		// console.log(tyoe)
		success: function (data) {
            alert(data);
            if (data == "保存成功") {
                var pro_id = $("#pro_id").val();
                ele_manager('/element/?pro_id=', pro_id);
                $(".modal-backdrop").hide();
                $(this).reset();
            }

        }
    })
});

//新增元素
$(document).on("click", "#add_element", function () {
    $("#reset_form").trigger("click");
    $("#add_ele_Modal").modal("show");
    $("#myModalLabel").text("新增元素");
});

//编辑元素
$(document).on("click", "#edit_ele", function () {
    var check_list = $(".checkbox:checked");
    if (check_list.length != 1) {
        alert("请勾选要编辑的一个元素")
    }
    else {
        ele_id = check_list.eq(0).attr("name");//function (data)是系统处理过从后传来
        $.post("/element/", {"ele_id": ele_id, "action": "get_element"}, function (data) {
            $("#opertion_method").val("edit_element");//修改元素value属性的值
            $("#myModalLabel").text("编辑元素");
            //根据回传的json写入值到编辑框中
            $("#ele_id").val(ele_id);
            var element_obj = data.element_data;
            var first_content = data.first_content;
            var second_content = data.second_content;
            $("#ele_name").val(element_obj.name);
            $("#ele_desc").val(element_obj.desc);
            
            
            
            
            var first_select = $("#first_method option");
            for (i = 0; i < first_select.length; i++) {
                if (first_content.method == first_select.eq(i).val()) {
                    $("#first_method").get(0).selectedIndex = i;
                }
            }

            var second_select = $("#second_method option");
            for (i = 0; i < second_select.length; i++) {
                if (second_content.method == second_select.eq(i).val()) {
                    $("#second_method").get(0).selectedIndex = i;
                }
            }
            $("#first_value").val(first_content.content);
            $("#second_vlaue").val(second_content.content);
        });
        $("#add_ele_Modal").modal("show")
    }
});

//删除元素
$(document).on("click", "#del_element", function () {
    var checked_list = $(".checkbox:checked");
    if (checked_list.length == "") {
        alert("请勾选要删除的元素")
    }
    else {
        //删除前段页面
        var del_conf = confirm("确认删除元素吗?");
        if (del_conf == true) {
            var id_list = [];
            for (i = 0; i < checked_list.length; i++) {
                var ele_content_id = checked_list.eq(i).attr("name");
                id_list.push(ele_content_id);
                checked_list.eq(i).parents("tr").remove();
            }
            ;
            $.post("/element/", {"id_list": id_list, "action": "delete_element"}, function (data) {
                if (data != "successful") {
                    alert(data)
                }
                else {
                    alert("删除成功")
                }
            })
        }
    }
});


//新增用例  先get到用例列表 
$(document).on("click", "#add_case", function () {
    var pro_id = $(this).attr("name");
    ele_manager("/add_case/?action=add_case&pro_id=", pro_id)
});

//新增场景
$(document).on("click", "#add_scenario", function () {
    var pro_id = $(this).attr("name");
    ele_manager("/add_scenario/?pro_id=", pro_id)
});

//编辑场景
$(document).on("click", "#edit_scenario", function () {
    var check_box = $(".checkbox:checked");
    if (check_box.length > 1) {
        alert("只能同时编辑一个测试场景")
    }
    if (check_box.length == 0) {
        alert("请勾选要编辑的测试场景")
    }
    else {
        var scenario_id = check_box.attr("name");
        var pro_id = $(this).attr("name");
        ele_manager("/edit_scenario?id=" + scenario_id + "&pro_id=", pro_id);
    }
});

//删除场景
$(document).on("click", "#del_scenario", function () {
    var check_list = $(".checkbox:checked");
    var del_list = [];
    for (i = 0; i < check_list.length; i++) {
        del_list.push(check_list.eq(i).attr("name"))
    }

    $.post("/scenario_list/", {"action": "del_scenario", "data": del_list}, function (data) {
        for (i = 0; i < check_list.length; i++) {
            check_list.eq(i).parents("tr").remove();
        }
        alert(data)
    })
});
//编辑用例
$(document).on("click", "#edit_case", function () {
    var check_list = $(".checkbox:checked");
	console.log(check_list)
    if (check_list.length != 1) {
        alert("请勾选一条用例")
    }
    else {
        var case_id = check_list.attr("name");
        ele_manager("/edit_case/?id=", case_id);
    }
});
//点击name进入编辑用例
$(document).on("click", "#edi", function () {
    var case_id = $(this).parent().siblings().eq(0).children("input").attr("name");
	var type = $(this).parent().siblings().eq(0).children("input").attr("t");

    if (type == "case") {
        ele_manager("/edit_case/?id=", case_id);
    }
    else {
		console.log("fail");
    }
});


//新增用例--点击选择元素   绑定id为show_element的onclick事件
$(document).on("click", ".show_element", function () {
    var number = $(this).parents("tr").children().eq(1).text();//步骤编号
	console.log(number);
    $("#sortable").attr("name", number);//赋值class为sortable元素的name属性，在select_element元素中使用
    $("#select_element").modal("show");//打开edit_case id为select_element的bootstrap的模态框
});

//Use元素按钮
$(document).on("click", "#use_element", function () {
    var checked_list = $(".select_element:checked");
    if (checked_list.length == 0) {
        $("#select_element").modal("hide")
    }
    if (checked_list.length > 1) {
        alert("只能使用一个元素")
    }
    if (checked_list.length == 1) {
        // 取元素id和name
        var ele_id = checked_list.attr("name");
        var ele_name = checked_list.attr("value");
        // 取步骤编号
        var number = $("#sortable").attr("name").trim();
        var tr_list = $("#sortable tr");//获取sortable下tr元素
        for (i = 0; i < tr_list.length; i++) {
            var td_number = tr_list.eq(i).children().eq(1);//步骤编号
            if (td_number.text().trim() == number) {
                td_number.siblings().eq(2).children("input").val(ele_id);
                td_number.siblings().eq(2).children("a").text(ele_name);
            }
        }
        //关闭弹出框
        $("#select_element").modal("hide");
        //取消勾选框
        $(".select_element").attr("checked", false)
    }
});

//查看元素
$(document).on("click", ".look_element", function () {
    // 判断隐藏元素ele_id是否为空,不为空开始取元素内容
    var ele_id = $(this).parent().siblings().eq(3).children("input").val();
    if (ele_id == '') {
        alert("请先选取元素");
    }
    else {
        $.post("/case/", {"ele_id": ele_id, "action": 'look_element'}, function (data) {
            var input_list = $("#look_element_modal input");
            input_list.eq(1).val(data.name);
            input_list.eq(2).val(data.desc);
            input_list.eq(3).val(data.first.method);
            input_list.eq(4).val(data.second.method);
            input_list.eq(5).val(data.first.content);
            input_list.eq(6).val(data.second.content);

            $("#look_element_modal").modal("show")
        })
    }
});

//执行测试用例
$(document).on("click", ".action_case", function () {
    var case_id = $(this).attr("name");
    alert("开始执行测试用例");
    $.post("/case_list/", {"id": case_id, 'action': 'action_case'}, function (data) {
        alert(data)
    })
});

//执行测试套件
$(document).on("click", ".action_suite", function () {
    var suite_id = $(this).attr("name");
    alert("开始执行测试套件");
    $.post("/scenario_list/", {"suite_id": suite_id, "action": "run_suite"}, function (data) {
        alert(data);
    })
});

//导入
$(document).on("click", "#import_case", function () {
    $("#import_case_modal").modal("show");
});

//导入用例-Use
$(document).on("click", "#import_case_button", function () {
    var check_list = $(".import_case_checkbox:checked");
    if (check_list.length != 1) {
        alert("只能导入一个用例");
    }
    else {
        var case_id = check_list.attr("name");
        $(".import_case_checkbox").attr("checked", false);
        $.get("/ajax_html?action=import_case&id=" + case_id, function (data) {
            $("#sortable:last").append(data);
        });


    }
});

//测试执行--增加用例--弹出modal
$(document).on("click", "#add_case_scenario", function () {
    $("#add_case_modal").modal("show");
});

//测试执行--增加用例--删除用例
$(document).on("click", "#delete_case_scenario", function () {
    var check_list = $(".checkbox_case:checked");
    for (i = 0; i < check_list.length; i++) {
        check_list.eq(i).parents("tr").remove()
    }
});

//测试执行--增加用例--确定
$(document).on("click", "#sure_scenario", function () {
    $("#add_case_modal").modal("hide");
    var check_list = $(".checkbox:checked");
    var case_list = [];
    for (i = 0; i < check_list.length; i++) {
        var case_id = check_list.eq(i).attr("name");
        case_list.push(case_id)
    }
    $.get("/ajax_html?action=add_case_scenario&case_list=" + case_list, function (data) {
        $("#scenario_case_body:last").append(data)
    });
    check_list.attr("checked", false);

});


//测试执行--新增测试执行--保存
$(document).on("submit", "#add_scenario_form", function (ev) {
    ev.preventDefault();
    $.ajax({
        url: '/add_scenario/',
        type: 'post',
        data: $(this).serialize(),
        success: function (data) {
            alert(data);
            if (data == '保存成功') {
                var pro_id = $("#project_id").val();
                ele_manager('/scenario_list/?pro_id=', pro_id)
            }
            else {
                alert("保存失败")
            }
        }
    })
});

//测试执行--编辑测试执行--保存
$(document).on("submit", "#edit_scenario_form", function (ev) {
    ev.preventDefault();
    $.ajax({
        url: '/edit_scenario/',
        type: 'post',
        data: $(this).serialize(),
        success: function (data) {
            alert(data);
            if (data == '保存成功') {
                var pro_id = $("#project_id").val();
                ele_manager('/scenario_list/?pro_id=', pro_id)
            }
            else {
                alert("保存失败")
            }
        }
    })
});

//导入步骤-Use
$(document).on("click", "#import_step_button", function () {
    var check_list = $(".import_case_checkbox:checked");
    if (check_list.length != 1) {
        alert("只能导入一个用例");
    }
    else {
        var case_id = check_list.attr("name");
        $(".import_case_checkbox").attr("checked", false);
        $.get("/ajax_html?action=import_step&id=" + case_id, function (data) {
            $("#sortable:last").append(data);
        });

    }
});

// 编辑用例--导入步骤edit_case_import_step
$(document).on("click", "#edit_case_import_step", function () {
    var check_list = $(".import_case_checkbox:checked");
    if (check_list.length != 1) {
        alert("只能导入一个用例");
    }
    else {
        var case_id = check_list.attr("name");
        $(".import_case_checkbox").attr("checked", false);
        $.get("/ajax_html?action=edit_case_import_step&id=" + case_id, function (data) {
            $("#sortable:last").append(data);
        });

    }
});

//查看用例/套件报告
$(document).on("click", ".look_case_report", function () {
    var name = $(this).attr("name");
    $.get("/is_html_path?name=" + name, function (data) {
        if (data == "True") {
            //window.location = "/report?name=" + name;
            window.open("/report?name=" + name);
        }
        else {
            alert("报告未生成")
        }
    });

});