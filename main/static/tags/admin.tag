<flag-list>
  <div class="flag-group" each={ opts.flagsets } if={ flags.length }>
    <h4 class="italic-title">{ verbose }</h4>
    <flag-row each={ flags }></flag-row>
  </div>
</flag-list>

<flag-row>
  <div class="pull-left">
    <button class="btn-success btn" onclick={ ajaxPost } data-action="send">
      <i class="icon-envelope"></i></button>
    <button class="btn-warning btn" onclick={ parent.parent.ajaxPost } data-action="delete">
      <i class="icon-trash"></i></button>
  </div>
  <a href="/admin/membership/userflag/{ pk }/">
    { subscription }
    <br/>{ reason_display } [{ datetime }]
  </a>

  ajaxPost(e) {
  }
</flag-row>
