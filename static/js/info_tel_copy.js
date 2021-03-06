$(document).ready(function () {
    function doAjax(url, data) {
        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            cache: true,
            success: function (data) {
                if (data.str_info !== '') {
                    $('.info-items').removeClass('hidden');
                    $('.info-items li').remove();
                    $('.info-items span').append('<li>' + data.str_info + '</li>');
                    if (data.str_comment !== undefined) {
                        // console.log(data.str_comment)
                        shovingTaskComments(data.str_comment)
                    }
                    // console.log(data.short_str_info)
                    // shovingTaskComments(data.short_str_info)
                    if (data.short_str_info !== undefined) {
                        shovingTaskComments(data.short_str_info)
                    }
                } else {
                    $('.info-items').addClass('hidden');
                }
            },
            error: function () {
                console.log("error")
            }
        });
    }

    function shovingInfo() {
        $('.info-items').toggleClass('hidden');
    }

    function shovingTaskComments(short_str_info) {
        // if (short_str_info !== 'undefined') {
        // $('.info-items').toggleClass('hidden');
        // adr = $('#id_address_task').val(adr_task);
        if ($('#id_comment_status').val() !== '') {
            short_str_info = $('#id_comment_status').val() + '\n' + short_str_info
        }
        // console.log(old_comment);
        $('#id_comment_status').val(short_str_info);
        // console.log(short_str_info);
        // }
    }


    var tel = $('#id_phone');
    tel.change(function (e) {
        e.preventDefault();
        tel = $('#id_phone').val();
        var data = {};
        data.tel = tel;
        var csrf_token = $('#task_form [name="csrfmiddlewaretoken"]').val();
        data["csrfmiddlewaretoken"] = csrf_token;
        var url = "/tasks/tasks/return_count_tel/"; // var url = form.attr("action"); // {% url 'return_count_tel' %}
        // shovingTaskComments(tel)
        doAjax(url, data);
    });


    var adr = $('#id_address_task');
    adr.change(function (e) {
        e.preventDefault();
        var adr = $('#id_address_task').val();
        // console.log('var ', adr)
        var data = {};
        data.adr = adr;
        var csrf_token = $('#task_form [name="csrfmiddlewaretoken"]').val();
        if (csrf_token == undefined) {
            csrf_token = $('#chart_form [name="csrfmiddlewaretoken"]').val();
        }
        data["csrfmiddlewaretoken"] = csrf_token;
        var url = "/tasks/chart/return_count_adr/";
        doAjax(url, data);
    });


    function doReuAjax(url, data) {
        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            cache: true,
            success: function (data) {
                var sub_reu = data.adr_reu;
                var reu = $('#id_reu');
                if (sub_reu !== '') {
                    reu.val(sub_reu);
                }
            },
            error: function () {
                console.log("error")
            }
        });
    }

    $('.info-items').on('click', function (e) {
        e.preventDefault();
        shovingInfo();
    });

    function get_reu(adr_reu) {
        var csrf_token = $('#task_form [name="csrfmiddlewaretoken"]').val();
        var url = "/tasks/chart/return_adr_reu/";
        var data = {};
        data["csrfmiddlewaretoken"] = csrf_token;
        data.adr_reu = adr_reu;
        doReuAjax(url, data);
    }

    var adr_task = $('#id_address');
    adr_task.change(function (e) {
        e.preventDefault();
        adr_task = $(this).find("option:selected").text();
        adr = $('#id_address_task').val(adr_task);
        adr.change();
        get_reu(adr_task);
    });


    function doToolAjax(url, data) {
        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            cache: true,
            success: function (data) {
                var porch = data.porch;
                var floor = data.floor;
                var phone = data.phone;
                var phn = $('#id_phone');
                if (porch !== '') {
                    $('#id_porch').val(porch);
                }
                if (floor !== '') {
                    $('#id_floor').val(floor);
                }
                if (floor !== '') {
                    phn.val(phone).change();
                }
                var source_task = $('#id_source_task');
                var status_task = $('#id_status_task');
                if (source_task.val() == '') {
                    source_task.val("????????????");
                }
                if (status_task.val() == '') {
                    status_task.val("?? ????????????");
                }
            },
            error: function () {
                console.log("error")
            }
        });
    }

    var apt = $('#id_apartment');
    apt.change(function (e) {
        e.preventDefault();
        var home = $('#id_address').val();
        if (home !== '') {
            apt = $('#id_apartment').val();
            var data = {};
            data.apt = apt;
            data.home = home;
            // console.log(apt, home);
            var csrf_token = $('#task_form [name="csrfmiddlewaretoken"]').val();
            data["csrfmiddlewaretoken"] = csrf_token;
            var url = "/tasks/tasks/return_tool/"; //??????????????, ????????, ?????????????? // var url = form.attr("action"); // {% url 'return_count_tel' %}
            doToolAjax(url, data);
        }
    });

    var category = $('#id_category');
    category.change(function (e) {
        e.preventDefault();
        var description = $('#id_description');
        var str_category = $(this).find("option:selected").text();
        var str_description = description.val();
        if (description.val() !== '') {
            description.val(str_category + ' --- ' + str_description);
            // description.val(str_category + '\n' + '[ ' + str_description + ' ]');
        } else {
            description.text(str_category);
        }
    })
});
