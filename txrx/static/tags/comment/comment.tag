<comment>
  <div class="comment_meta">
    <a href="javascript:;" onclick={ collapse } class="expand-link"></a>
    <span class="commented_by">{ username } - </span>
    <span class="commented_date">{ date_s }</span>
  </div>
  <div class="comment_content">{ comment }</div>
  <div class="comment_actions">
    <div if={ window._USER_NUMBER}>
      <a onclick={ reply } title="reply" href="#"><i class="fa fa-reply"></i> Post Reply</a>
      <!--| <a onclick="commentFlag({ pk });return false;" title="flag" href="#"><i class="fa fa-flag"></i> Flag</a>-->
      <a if={ user_pk == window._USER_NUMBER } onclick={ edit } title="reply"
         href="#"><i class="fa fa-pencil"></i> Edit</a>
      <a if={ window._418 } href="/admin/mptt_comments/mpttcomment/{ pk }/delete/"><i class="fa fa-close"></i> Delete</a>
    </div>
    <div if={ !window._USER_NUMBER }>
      <a href="/accounts/login/?next=/classes/42/woodworking-tools-i/#c265">Login to reply to this comment</a>
    </div>
  </div>
  <comment-form if={ form_data }></comment-form>
  <div class="comment_children">
    <comment each={ comments }></comment>
  </div>
  collapse(e) {
    $(e.target).closest('comment').toggleClass('collapsed');
  }
  reply(e) {
    form = this.tags['comment-form']
    this.form_data = form.data = {
      parent_pk: this.pk,
      form_url: "/can_comments/post/",
    };
    form.update()
  }
  edit(e) {
    var pk = this.pk, that = this;
    $.get(
      "/can_comments/"+pk+"/",
      function(data) {
        data.form_url = "/can_comments/edit/"+pk+"/";
        form = that.tags['comment-form']
        that.form_data = form.data = data
        form.update()
        that.update()
      },
      "json"
    )
  }
  this.root.className = "comment_level_{ level } l{ l_mod } comment_expanded";
  this.root.id = "c{ pk }";
</comment>
