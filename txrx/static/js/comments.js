function commentReply(pk) {
  // add to immediate child so child comments don't get form
  riot.mount("#c"+pk+" > comment-form",{parent_pk:pk});
}

function commentEdit(pk) {
  $("#c"+pk+" > comment-form").addClass("loading");
  $.get(
    "/can_comments/"+pk+"/",
    function(data) {
      data.form_url = "/can_comments/edit/"+pk+"/";
      riot.mount("#c"+pk+" > comment-form",data);
    },
    "json"
  )
}

function commentNew(content_type,object_pk) {
  data.form_url = "/can_comments/post/";
  riot.mount("#c"+pk+" > comment-form",{parent_pk:pk});
}

function commentPost(form) {
  $(form).addClass('loading');
  $.post(
    form.action,
    $(form).serializeArray(),
    function(data) {
      if ($("#c"+data.pk).length) {
        riot.mount("#c"+data.pk,data);
      } else {
      $(form).replaceWith(riot.mount(form,data));
      }
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
      "/can_comments/list/",
      params,
      function(data) {
        params.comments = data;
        params.form_url = "/can_comments/post/";
        riot.mount("comment-list",params);
      },
      "json"
    );
  });
});
