<event-list>
  <h2 if={ _c }>{ _c } Upcoming Event{ _s }:</h2>
  <h2 if={ !_c }>No Upcoming Events</h2>
  <event-occurrence each={ occurrences } />

  var that = this;
  that.occurrences = opts.occurrences;
  this.on("update", function() {
    that._c = that.occurrences.length;
    that._s = (that._c > 1)?"s":"";
    var user_reservations = opts.user_reservations || [];
    uR.forEach(that.occurrences,function(o) { o.quantity = user_reservations[o.id] || 0; });
  });
</event-list>

<event-occurrence>
  <div class="well" name="loading-target">
    <a if={ admin_access } href="/admin/event/eventoccurrence/{ id }" class="admin-link fa fa-pencil-square"></a>
    <div class="dates">
      <div>{ start_string }</div>
    </div>
    <b class="full" if={ full }>This occurrence is full</b>
    <div if={ !full && authenticated }>
      <button class="btn btn-success rsvp" if={ !quantity } onclick={ makeRSVP }>RSVP for this event</button>
      <button class="btn btn-danger unrsvp" if={ quantity } onclick={ cancelRSVP }>Cancel RSVP</button>
      <span if={ total_rsvp && admin_access } data-reddot={ total_rsvp }></span>
    </div>
    <div if={ !full && !authenticated }>
      You must
      <a href="/accounts/login/?next={ session.get_absolute_url|urlencode }">Login</a>
      to RSVP
    </div>
  </div>

  var self = this;
  this.on('mount',function() {
    this.start_string = moment(this.start).format("ddd MMM D, YYYY h:mm a");
    TXRX.ready(function() {
      self.admin_access = window.TXRX.user.is_superuser;
      self.authenticated = window.TXRX.user.id;
      self.update();
    });
  });
  function updateRSVP(item,quantity) {
    item.quantity = quantity;
    var target = self['loading-target'];
    target.setAttribute("ur-loading","loading");
    $.get(
      '/event/rsvp/',
      {occurrence_id: item.id,quantity: quantity},
      function(data) {
        target.removeAttribute("ur-loading");
        self.parent.opts.user_reservations = data;
        self.parent.update();
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
