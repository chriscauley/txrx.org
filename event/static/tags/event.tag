<event-list>
  <h2 if={ _c }>{ _c } Upcoming Event{ _s }:</h2>
  <h2 if={ !_c }>No Upcoming Events:</h2>
  <event-occurrence each={ opts.occurrences }></event-occurrence>

  var that = this;
  this.on("update", function() {
    that._c = opts.occurrences.length;
    that._s = (that._c > 1)?"s":"";
    var user_reservations = that.opts.user_reservations || [];
    for (var i=0; i<opts.occurrences.length; i++) {
      var o = opts.occurrences[i];
      o.quantity = user_reservations[o.id] || 0;
    };
  });
</event-list>

<event-occurrence>
  <div class="well" name="loading-target">
    <a if={ admin_access } href="/admin/event/eventoccurrence/{{ id }}" class="admin-link fa fa-pencil-square"></a>
    <div class="dates">
      <div>{ start_string }</div>
    </div>
    <b class="full" if={ full }>This occurrence is full</b>
    <div if={ !full && authenticated }>
      <button class="btn btn-success rsvp" if={ !quantity } onclick={ makeRSVP }>RSVP for this event</button>
      <button class="btn btn-danger unrsvp" if={ quantity } onclick={ cancelRSVP }>Cancel RSVP</button>
    </div>
    <div if={ !full && !authenticated }>
      You must
      <a href="/accounts/login/?next={{ session.get_absolute_url|urlencode }}">Login</a>
      to RSVP
    </div>
  </div>

  var that = this;
  this.start_string = new Date(this.start).toString("ddd MMM d, yyyy h:mm tt");
  
  this.admin_access = window.TXRX.user.is_superuser;
  this.authenticated = window.TXRX.user.id;
  function updateRSVP(item,quantity) {
    item.quantity = quantity;
    var target = that['loading-target'];
    target.setAttribute("ur-loading","loading");
    $.get(
      '/event/rsvp/',
      {occurrence_id: item.id,quantity: quantity},
      function(data) {
        target.removeAttribute("ur-loading");
        that.parent.opts.user_reservations = data;
        that.parent.update();
      },
      "json"
    );
  }
  makeRSVP(e) {
    updateRSVP(e.item,e.item.quantity+1);
  }
  cancelRSVP(e) {
    updateRSVP(e.item,0);
  }
  this.on("update",function() {

  });
</event-occurrence>
