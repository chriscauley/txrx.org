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
  $("#c"+pk).append(can.view("/static/mustache/new_comment.html",{pk:pk}));
}
function commentPost(form) {
  console.log($(form).serializeArray());
}

$(function() {
  $("[data-mptt]").each(function() {
    var params = {
      object_pk: this.dataset.object_pk,
      name: this.dataset.name,
      app: this.dataset.app
    };
    var that = this;
    $.get(
      "/can_comments/",
      params,
      function(data) {
        for (var i=0;i<data.length;i++) {
          $(that).append(can.view("/static/mustache/mptt_comment.html",data[i]));
        }
      },
      "json"
    );
  });
});
