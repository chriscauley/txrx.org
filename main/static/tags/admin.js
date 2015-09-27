riot.tag('flag-list', '<div class="flag-group" each="{ opts.flagsets }" if="{ flags.length }"> <h4 class="italic-title">{ verbose }</h4> <flag-row each="{ flags }"></flag-row> </div>', function(opts) {

});

riot.tag('flag-row', '<div class="{ className } well"> <div class="pull-left"> <button class="btn-success btn fa fa-envelope" onclick="{ ajaxPost }" data-action="send"></button> <button class="btn-danger btn fa fa-trash" onclick="{ ajaxPost }" data-method="delete"></button> </div> <a href="/admin/membership/flag/{ pk }/"> { subscription }<br > [{ date }] </a> </div>', function(opts) {

  this.ajaxPost = function(e) {
    var action = e.target.dataset.action || "default";
    var method = e.target.dataset.method || "get";
    var that = this;
    that.className = "loading";
    $.ajax({
      url: router[action](this),
      type: method.toUpperCase(),
      success: function(data) {
        that.className = "";
        if (method == "delete") { that.className = "deleted"; }
        if (action == "send") { that.className = "sent"; }
        that.update();
      }
    });
  }.bind(this);
  var router = {
    send: function(item) { return "/update_flag_status/"+item.pk+"/"; },
    default: function(item) { return "/api/membership/activeflag/"+item.pk+"/"; },
  }

});
