<comment-list>
  <comment each={ comments }></comment>
  <comment-form></comment-form>
  this.comments = opts.comments;
  this.form_data = {
    form_url: "/can_comments/post/",
    object_pk: opts['data-object_pk'],
    content_type: opts['data-content_type']
  }
</comment-list>
