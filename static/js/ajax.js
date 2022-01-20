function ajaxPagination() {
  $('#pagination a.page-link').each((index, el) => {
    $(el).click((e) => {
      e.preventDefault();
      let page_url = $(el).attr('href');
      // console.log("page_url from static", page_url);
      $('#tasks_filter').attr("action", page_url);
      $('#tasks_filter').submit();
    })
  })
}

$(document).ready(function () {
  ajaxPagination()
});
