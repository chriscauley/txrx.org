<event-list>
  <h2 if={ _c }>{ _c } Upcoming Event{ _s }:</h2>
  <h2 if={ !_c }>No Upcoming Events</h2>
  <event-occurrence each={ occurrences } />

  this.event = this.opts.event;
  this.occurrences = this.event.upcoming_occurrences;
  this.user_reservations = opts.user_reservations || [];
  this.on("update", function() {
    this._c = this.event.upcoming_occurrences.length;
    this._s = (this._c > 1)?"s":"";
    uR.forEach(this.occurrences,function(o) { o.quantity = this.user_reservations[o.id] || 0; }.bind(this));
  });
</event-list>

<event-occurrence>
  <div class="well" name="ajax_target">
    <a if={ uR.auth.user.is_superuser } href="/event/orientations/{ start_slug }/"
       class="admin-link fa fa-pencil-square"></a>
    <a if={ uR.auth.user.is_staff && parent.event.allow_rsvp } href="/tools/master/event/rsvp/?object_id={ id }"
       class="admin-link fa fa-check-square-o" style="top: auto; bottom: 0;"></a>
    <div class="dates">
      <div>{ start_string }</div>
    </div>
    <b class="full" if={ full }>This occurrence is full</b>
    <div if={ !past && parent.event.allow_rsvp}>
      <div if={ !full && authenticated }>
        <button class="btn btn-success rsvp" if={ !quantity } onclick={ makeRSVP }>RSVP for this event</button>
        <button class="btn btn-danger unrsvp" if={ quantity } onclick={ cancelRSVP }>Cancel RSVP</button>
        <span if={ total_rsvp && uR.auth.user.is_superuser } data-reddot={ total_rsvp }></span>
      </div>
      <div if={ !full && !authenticated }>
        You must <a href={ uR.urls.auth.login }>Login</a> to RSVP
      </div>
    </div>
    <div if={ past }>
      <span class="btn btn-warning">You can no longer RSVP</span>
    </div>
  </div>

  var self = this;
  this.on('mount',function() {
    var start = moment(this.start);
    this.start_string = start.format("ddd MMM D, ");
    this.start_string += uR.formatTimeRange(this.start,this.end);
    this.start_slug = start.format("YYYY/MM/DD");

    uR.auth.ready(function() {
      this.authenticated = uR.auth.user;
      this.update();
    }.bind(this));
  });
  updateRSVP(item,quantity) {
    item.quantity = quantity;
    this.ajax({
      url: '/event/rsvp/',
      data: {occurrence_id: item.id,quantity: quantity},
      success: function(data) {
        this.parent.user_reservations = data;
        this.update();
        this.parent.update();
      },
      error: function(data) { uR.alert(data.error); }
    });
  }
  makeRSVP(e) {
    this.updateRSVP(e.item,e.item.quantity+1);
  }
  cancelRSVP(e) {
    this.updateRSVP(e.item,0);
  }
</event-occurrence>
