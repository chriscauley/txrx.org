<comment-list>
  <h2>Comments</h2>
  <div class="alert alert-danger reply-warning" if={ comments }>
    If you want to respond to a comment, please click "Post Reply" underneath that comment.
    This way the comment author will receive a notification of your response.
  </div>
  <comment each={ comments }></comment>
  <h2 class="section_title" if={ window._USER_NUMBER }>Post a new comment</h2>
  <div class="alert alert-warning" if={ !window._USER_NUMBER }>
    <a href="/accounts/login/?next={ window.location.pathname }">Login to reply to this comment</a>
  </div>
  this.comments = opts.comments;
  this.on('mount', function() {
    if (!window._USER_NUMBER) { return }
    $(this.root).append($("<comment-form id='f0'></comment-form>"))
    riot.mount('#f0',{
      parent: this,
      form_url: "/comments/post/",
      object_pk: opts['data-object_pk'],
      content_type: opts['data-content_type']
    });
  })
</comment-list>
