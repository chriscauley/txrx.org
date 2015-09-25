<flag-list>
  <div class="flag-group" each={ opts.flagsets } if={ flags.length }>
    <h4 class="italic-title">{ verbose }</h4>
    <flag-row each={ flags }></flag-row>
  </div>
</flag-list>

<flag-row>
  <div class="well">
    <div class="pull-left">
      <button class="btn-success btn fa fa-envelope" onclick={ ajaxPost } data-action="send"></button>
      <button class="btn-danger btn fa fa-trash" onclick={ ajaxPost } data-action="delete"></button>
    </div>
    <a href="/admin/membership/userflag/{ pk }/">
      { subscription }<br />
      [{ date }]
    </a>
  </div>

  ajaxPost(e) {
    console.log(e)
    var action = e.target.dataset.action || "default";
    var url = router[action](this);
    console.log(url);
  }
  var router = {
    send: function(item) { return "/update_flag_status/"+item.pk+"/"; },
    default: function(item) { return "/api/membership/activeflags/"+item.pk+"/"; },
  }

</flag-row>
