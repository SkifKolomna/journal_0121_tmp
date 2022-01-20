$(document).ready(function () {
  // form.on('change', function (e) {
  var adr = $('#id_address');
  adr.change(function (e) {
    var adr = $('#id_address').val();
    e.preventDefault();
    var data = {};
    data.adr = adr;

    var csrf_token = $('#task_form [name="csrfmiddlewaretoken"]').val();
    // var csrf_token = $('#chart_form [name="csrfmiddlewaretoken"]').val();

    data["csrfmiddlewaretoken"] = csrf_token;
    // var url = form.attr("action");
    // var url = "/tasks/chart/return_count_adr/";
    var url = "/charts/chart/return_count_adr/";

    // console.log(adr);

    $.ajax({
      url: url,
      type: 'POST',
      data: data,
      cache: true,
      success: function (data) {
        // console.log(adr);
        // console.log(url);
        if (data.str_info !== '') {
          $('.info-items').removeClass('hidden');
          $('.info-items li').remove();
          $('.info-items span').append('<li>' + data.str_info + '</li>');
        } else {
          $('.info-items').addClass('hidden');
        }
      },
      error: function () {
        console.log("error");
        // console.log(adr);
        // console.log("error");
      }
    });
  });
})
;
