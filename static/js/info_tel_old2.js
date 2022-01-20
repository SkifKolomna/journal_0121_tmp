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
                    if (data.short_str_info !== undefined) {
                        shovingTaskComments(data.short_str_info)
                    }
                } else {
                    $('.info-items').addClass('hidden');
                }
                if (data.family !== '') {
                    $('#id_surname_name').val(data.family)
                }
                if (data.name !== '') {
                    $('#id_first_name').val(data.name)
                }
                if (data.patronim !== '') {
                    $('#id_patronymic_name').val(data.patronim)
                }
            },
            error: function () {
                console.log("error")
            }
        });
    }

    /* скрывает поле */
    function shovingInfo() {
        $('.info-items').toggleClass('hidden');
    }

    /* копирует строку в поле комментарий или добавляет данные к полю если оно не пусто  */
    function shovingTaskComments(short_str_info) {
        if ($('#id_comment_status').val() !== '') {
            short_str_info = $('#id_comment_status').val() + '\n' + short_str_info
        }
        $('#id_comment_status').val(short_str_info);
    }

    /* готовит данные дя запроса при изменении номера телефона и передаёт их */
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

    /* готовит данные дя запроса при изменении адреса и передаёт их */
    var adr = $('#id_address');
    adr.change(function (e) {
        e.preventDefault();
        var adr = $('#id_address').val();
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

    /* отправляет запрос рэу и заполняет строку рэу ответом */
    function doReuAjax(url, data) {
        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            cache: true,
            success: function (data) {
                if (data.adr_reu !== '') {
                    $('#id_reu').val(data.adr_reu);
                }
            },
            error: function () {
                console.log("error")
            }
        });
    }

    /* по клику на инфополе вызывает функцию скрытия поля */
    $('.info-items').on('click', function (e) {
        e.preventDefault();
        shovingInfo();
    });

    /* получает адрес и отправляет запрос для рэу */
    function get_reu(adr_reu) {
        var url = "/tasks/chart/return_adr_reu/";
        var data = {};
        data["csrfmiddlewaretoken"] = $('#task_form [name="csrfmiddlewaretoken"]').val();
        data.adr_reu = adr_reu;
        doReuAjax(url, data);
    }

    /* если выбирается/меняется значение строки адрес то запрашивается рэу */
    var adr_task = $('#id_address');
    adr_task.change(function (e) {
        e.preventDefault();
        adr_task = $(this).find("option:selected").text();
        // adr = $('#id_address_task').val(adr_task);
        // adr.change();
        get_reu(adr_task);
    });

    /* запрос возвращает data с подъездом, этажом, телефоном для адреса и заполняет поля если они пусты */
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

    /* при выборе/изменении квартиры если есть адрес дома вызывается ajax запрос "/tasks/tasks/return_tool/" */
    var apt = $('#id_apartment');
    apt.change(function (e) {
        e.preventDefault();
        var home = $('#id_address').val();
        if (home !== '') {
            var data = {};
            apt = $('#id_apartment').val();
            data.apt = apt;
            data.home = home;
            // console.log(apt, home);
            var csrf_token = $('#task_form [name="csrfmiddlewaretoken"]').val();
            data["csrfmiddlewaretoken"] = csrf_token;
            var url = "/tasks/tasks/return_tool/"; //подъезд, этаж, телефон // var url = form.attr("action"); // {% url 'return_count_tel' %}
            doToolAjax(url, data);
        }
    });


    function doCategory(data) {
        $.ajax({
            url: "/tasks/tasks/return_deadline/",
            type: 'POST',
            data: data,
            cache: true,
            success: function (data) {
                // console.log('data', data);
                descript(data);
            },
            error: function () {
                console.log("error doCategory")
            }
        });
    }

    function descript(data) {
        var description = $('#id_description');
        var old_description = description.val();
        var desc = data.name + '. Исполнить до ' + data.deadline + '.';
        // console.log(data.deadline)
        if (description.val() !== '') {
            description.val(desc + ' -- ' + old_description);
        } else {
            description.val(desc);
        }

    }


    /* если выбирается категория то текстовое значение копируется в верхнюю часть "Содержания заявки" */
    var category = $('#id_category');
    category.change(function (e) {
        e.preventDefault();
        // var str_category = $(this).find("option:selected").text();
        var data = {};
        data["csrfmiddlewaretoken"] = $('#task_form [name="csrfmiddlewaretoken"]').val()
        data.id_category = $(this).find("option:selected").val();
        // console.log('data', data);
        doCategory(data)
    });


    /*
        var category = $('#id_category');
        category.change(function (e) {
            e.preventDefault();
            var description = $('#id_description');
            var str_category = $(this).find("option:selected").text();
            var str_description = description.val();
            if (description.val() !== '') {
                description.val(str_category + ' -- ' + str_description);
            } else {
                description.text(str_category);
            }
        })
    */


    /* проверяет номер задачи если № текущей больше последней в базе вызывает reload */
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

    /* перезагружает страницу раз в 15 секунд если в пути /tasks/tasks/ */
    function reload() {
        $('#tasks_filter').submit();
    }

    var pagesWithScript = ["/tasks/tasks/"];
    if (pagesWithScript.indexOf(location.pathname) != -1) {
        setInterval(return_last_id, 15000);
    }
});
