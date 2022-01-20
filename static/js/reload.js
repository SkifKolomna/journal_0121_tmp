$(document).ready(function () {
    /* проверяет номер задачи если № текущей больше последней в базе вызывает reload */
    let old_id;

    function return_last_id(data) {
        $.ajax({
            url: '/tasks/return_last_id/',
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

    // var pagesWithScript = ["/tasks/"];
    let pagesWithScript = ["/tasks/"];
    if (pagesWithScript.indexOf(location.pathname) != -1) {
        setInterval(return_last_id, 30000);
    }
});
