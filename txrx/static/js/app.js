var Comment = can.Model.extend({
  create: 'POST /can_comment/new/',
  update: 'POST /can_comment/{id}/',
  destroy: 'DELETE /can_comment/{id}/'
},{});

can.mustache.registerHelper('ifCurrentUser',function(value) {
  return window._USER_NUMBER == value;
});
can.mustache.registerHelper('if418',function(block) {
  return (window._418)?block.fn():block.inverse();
});
can.mustache.registerHelper('ifLoggedIn',function(block) {
  return (window._USER_NUMBER != "None")?block.fn():block.inverse();
});

function commentReply(pk) {
  // add to immediate child so child comments don't get form
  $("#c"+pk+" > .comment_actions").append(can.view("/static/mustache/new_comment.html",{parent_pk:pk}));
}

function commentNew(content_type,object_pk) {
  
}

function commentPost(form) {
  $(form).addClass('loading');
  $.post(
    '/can_comments/post/',
    $(form).serializeArray(),
    function(data) {
      $(form).replaceWith(can.view("/static/mustache/mptt_comment.html",data));
    },
    'json'
  )
}

$(function() {
  $("[data-mptt]").each(function() {
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
        $(that).replaceWith(can.view("/static/mustache/list_comments.html",params));
      },
      "json"
    );
  });
});
