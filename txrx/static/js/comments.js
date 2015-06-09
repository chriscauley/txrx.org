function commentEdit(pk) {
  $("#c"+pk+" > comment-form").addClass("loading");
  $.get(
    "/comments/"+pk+"/",
    function(data) {
      data.form_url = "/comments/edit/"+pk+"/";
      riot.mount("#c"+pk+" > comment-form",data);
    },
    "json"
  )
}

function commentPost(e,that) {
  form = e.target;
  $(form).addClass('loading');
  $.post(
    form.action,
    $(form).serializeArray(),
    function(data) {
      // #! TODO: don't push data, splice, update url, and change focus
      that.parent.comments.push(data);
      that.parent.update();
    },
    'json'
  )
}

$(function() {
  $("comment-list").each(function() {
    var params = {
      object_pk: this.dataset.object_pk,
      content_type: this.dataset.content_type
    };
    var that = this;
    $.get(
      "/comments/list/",
      params,
      function(data) {
        params.comments = data;
        params.form_url = "/comments/post/";
        riot.mount("comment-list",params);
      },
      "json"
    );
  });
});
