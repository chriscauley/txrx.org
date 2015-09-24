$(function() {
  if ($("flag-list").length) {
    $.get(
      "/api/active-flags/",
      function(data) {
        riot.mount("flag-list",data);
      },
      "json"
    )
  }
});
