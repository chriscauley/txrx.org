<flag-list>
  <div class="flag-group" each={ opts.flagsets } if={ flags.length }>
    <h4 class="italic-title">{ verbose }</h4>
    <flag-row each={ flags }></flag-row>
  </div>

</flag-list>

<flag-row>
  <div class="{ className } well">
    <div class="pull-left">
      <button class="btn-success btn fa fa-envelope" onclick={ ajaxPost } data-action="send"></button>
      <button class="btn-danger btn fa fa-trash" onclick={ ajaxPost } data-method="delete"></button>
      <a class="btn-primary btn fa fa-user" href="/admin/user/user/{user_id}/" target="_blank"></a>
    </div>
    <a href="/admin/membership/flag/{ pk }/">
      { subscription }<br />
      [{ date }] - <b>{status}</b>
    </a>
  </div>

  ajaxPost(e) {
    var action = e.target.dataset.action || "default";
    var method = e.target.dataset.method || "get";
    var that = this;
    that.className = "loading";
    JWT.loginRequired(function(){
      $.ajax({
        url: router[action](that),
        type: method.toUpperCase(),
        success: function(data) {
          that.className = "";
          if (method == "delete") { that.className = "deleted"; }
          if (action == "send") { that.className = "sent"; }
          that.update();
        }
      });
    })();
  }
  var router = {
    send: function(item) { return "/update_flag_status/"+item.pk+"/"; },
    default: function(item) { return "/api/membership/activeflag/"+item.pk+"/"; },
  }
</flag-row>
