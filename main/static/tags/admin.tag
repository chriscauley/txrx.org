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
      <button class="btn-danger btn fa fa-trash" onclick={ ajaxPost } data-method="delete"></button>
    </div>
    <a href="/admin/membership/flag/{ pk }/">
      { subscription }<br />
      [{ date }]
    </a>
  </div>

  ajaxPost(e) {
    var action = e.target.dataset.action || "default";
    var method = e.target.dataset.method || "get";
    console.log(this);
    console.log(method);
    $.ajax({
      url: router[action](this),
      type: method.toUpperCase(),
    });
  }
  var router = {
    send: function(item) { return "/update_flag_status/"+item.pk+"/"; },
    default: function(item) { return "/api/membership/activeflag/"+item.pk+"/"; },
  }
</flag-row>
