<comment-list>
  <comment each={ comments }></comment>
  this.comments = opts.comments;
  this.on('mount', function() {
    $(this.root).append($("<comment-form id='f0'></comment-form>"))
    riot.mount('#f0',{
      parent: this,
      form_url: "/can_comments/post/",
      object_pk: opts['data-object_pk'],
      content_type: opts['data-content_type']
    });
  })
</comment-list>
