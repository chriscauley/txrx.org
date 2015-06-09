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
  <div class="comment_form"></div>
  <div class="comment_children">
    <comment each={ comments }></comment>
  </div>
  var that = this
  collapse(e) {
    $(e.target).closest('comment').toggleClass('collapsed');
  }
  /*reply(e) {
    form = this.tags['comment-form']
    this.form_data = form.data = 
    form.update()
  }*/
  function openForm(form_opts) {
    form_opts.parent = that
    $(that.root).find(">.comment_form").html("<comment-form id='f"+that.pk+"'></comment-form>");
    riot.mount("#f"+that.pk,form_opts)
  }
  reply(e) {
    var form_opts = {
      parent_pk: that.pk,
      form_url: "/comments/post/",
      comment: '',
    }
    openForm(form_opts);
  }
  edit(e) {
    $.get(
      "/comments/"+that.pk+"/",
      function(form_opts) {
        form_opts.form_url = "/comments/edit/"+that.pk+"/",
        openForm(form_opts);
      },
      "json"
    )
  }
  that.root.className = "comment_level_{ level } l{ l_mod } comment_expanded";
  that.root.id = "c{ pk }";
</comment>
