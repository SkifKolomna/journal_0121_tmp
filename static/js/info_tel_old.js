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
                if (data.family !== '') {
                    // if ($('#id_surname_name').val() == '') {
                        $('#id_surname_name').val(data.family)
                    // }

                }
                if (data.name !== '') {
                    // if ($('#id_first_name').val() == '') {
                        $('#id_first_name').val(data.name)
                    // }
                }
                if (data.patronim !== '') {
                    // if ($('#id_patronymic_name').val() == '') {
                        $('#id_patronymic_name').val(data.patronim)
                    // }
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


    /*
         var js_home = $('#id_home').select2();
         js_home.change(function (e) {
             e.preventDefault();
             var js_home_title = $(this).find("option:selected").text();
             var js_home_value = $(this).find("option:selected").val();
             // var ht = js_home.text();
             // var hv = js_home.val();

             // home = $(this).val();
             // console.log(js_home_title);
             // console.log(js_home_value);
             // console.log(ht);
             // console.log(hv);
         });
     */

    /*
        $('#id_home').select2({
            ajax: {
                url: '/tasks/select2/fields/auto.json'
            }
        });
    */

    /*
        var data = {
            id: $('#id_home').val(),
            text: $('#id_home').text(),
        };
        var newOption = new Option(data.text, data.id, true, true);
        console.log(data.id);
        console.log(data.text);
        $('#id_home').append(newOption).trigger('change');
    */


    // var adr_home = $('#id_home');
    // Set up the Select2 control
    /*
        $('#id_home').select2({
            ajax: {
                url: '/tasks/select2/fields/auto.json'
            }
        });
    */

    /*
        // Fetch the preselected item, and add to the control
        var home = $('#id_home');
        $.ajax({
            type: 'GET',
            // url: '/tasks/select2/fields/auto.json?term=83&field_id=MjA2MTkwODczMTQwMA:1ksjWX:_QfAYe8qoetcLiF7G9MbFlCXj2M'
        }).then(function (data) {
            // create the option and append to Select2
            console.log(home.val());
            console.log($('#id_home').text());
            data = {
                id: home.val(),
                text: $('#id_home').text(),
            };
            console.log(data.id);
            console.log(data.text);
            var option = new Option(data.text, data.id, true, true);
            // var option = new Option(js_home_title, js_home_value, true, true);
            // var option = new Option(home.find("option:selected").text(), home.find("option:selected").val(), true, true);
            home.append(option).trigger('change');
            console.log(option);
            // console.log(js_home_title)
            // console.log(js_home_value)

            // manually trigger the `select2:select` event
            home.trigger({
                type: 'select2:select',
                params: {
                    data: data
                }
            });
        });
    */

    // adr_home.change(function (e) {
    // e.preventDefault();
    // console.log($(this));
    // console.log(adr_home.find("option[value='" + data.id + "']").length);
    // Set the value, creating a new option if necessary
    // if ($(this).find("option[value='" + data-select2-id.id + "']").length) {
    //     console.log('есть значение')
    //     $(this).val(data.id).trigger('change');
    // } else {
    //     Create a DOM Option and pre-select by default
    // var newOption = new Option(data.text, data.id, true, true);
    // Append it to the select
    // console.log('нет значения')
    // $(this).append(newOption).trigger('change');
    // }
    // adr_home = $(this).val();
    // adr_home = $(this).find("option:selected");
    // adr = $('#id_address_task').val(adr_task);
    // adr.change();
    // get_reu(adr_task);
    // console.log(adr_home);
    // adr_home.text('ул. Дзержинского, д.83');
    // $('#adr_home').val(null).trigger('change');
    // adr_home.val('75');
    // adr_home.change();
    // adr_home.trigger('change');
    // console.log(adr_home.val(), adr_home.text())
    // console.log(adr_home)
    // });


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
                    source_task.val("житель");
                }
                if (status_task.val() == '') {
                    status_task.val("в работе");
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
            var url = "/tasks/tasks/return_tool/"; //подъезд, этаж, телефон // var url = form.attr("action"); // {% url 'return_count_tel' %}
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
    });


    var old_id;

    function return_last_id(data) {
        $.ajax({
            url: '/tasks/tasks/return_last_id/',
            type: 'GET',
            data: data,
            cache: true,
            success: function (data) {
                if (old_id < data.id) {
                    reload()
                }
                old_id = data.id;
            },
            error: function () {
                console.log('error')
            }
        });
    }


    function reload() {
        // $('tasks-list').html('').load(
        //     "{% url '/tasks/tasks-list' %}"
        // );
        $('#tasks_filter').submit();
    }

    var pagesWithScript = ["/tasks/tasks/"];

    if (pagesWithScript.indexOf(location.pathname) != -1) {
        setInterval(return_last_id, 15000);
        // console.log(location.pathname);
        // console.log(location.href);
    }

});
