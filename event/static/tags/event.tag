<event-owner>
  <div if={ is_owner }>
    <h3>You are an organizer of this event</h3>
    <button onclick={ click } action="disown" class={ uR.config.btn_cancel }>Stop Organizing</button>
  </div>
  <div if={ !is_owner && parent.event.owner_ids.length }>
    <h3>This event has an organizer</h3>
    <p>
      If you want to become organizer, email <a href="mailto:{ uR.config.support_email }">{ uR.config.support_email }</a>
    </p>
  </div>
  <div if={ !parent.event.owner_ids.length } onclick={ ownIt }>
    <h3>This event has no organizer</h3>
    <button onclick={ click } action="own" class={ uR.config.btn_success }>Become Organizer</button>
  </div>

this.on("mount",function() {
  uR.auth.ready(function() {
    this.update();
  }.bind(this));
});

this.on("update",function() {
  if (uR.auth.user) {
    this.is_owner = this.parent.event.owner_ids.indexOf(uR.auth.user.id) != -1;
  }
})
click(e) {
  this.ajax({
    url: "/event/"+ e.target.getAttribute('action')+"/"+this.parent.event.id+"/",
    success: function (data) { this.parent.event.owner_ids = data.owner_ids; },
    method: "POST",
  });
}
</event-owner>
    

<event-list>
  <!--<event-owner if={ uR.auth.user.is_staff }></event-owner>-->
  <h2 if={ _c }>{ _c } Upcoming Event{ _s }:</h2>
  <h2 if={ !_c }>No Upcoming Events</h2>
  <event-occurrence each={ occurrences } />

  var that = this;
  that.event = that.opts.event;
  that.occurrences = that.event.upcoming_occurrences;
  this.on("update", function() {
    that._c = that.event.upcoming_occurrences.length;
    that._s = (that._c > 1)?"s":"";
    var user_reservations = opts.user_reservations || [];
    uR.forEach(that.occurrences,function(o) { o.quantity = user_reservations[o.id] || 0; });
  });
</event-list>

<event-occurrence>
  <div class="well" name="loading-target">
    <a if={ uR.auth.user.is_superuser } href="/event/orientations/{ start_slug }/"
       class="admin-link fa fa-pencil-square"></a>
    <div class="dates">
      <div>{ start_string }</div>
    </div>
    <b class="full" if={ full }>This occurrence is full</b>
    <div if={ !past }>
      <div if={ !full && authenticated }>
        <button class="btn btn-success rsvp" if={ !quantity } onclick={ makeRSVP }>RSVP for this event</button>
        <button class="btn btn-danger unrsvp" if={ quantity } onclick={ cancelRSVP }>Cancel RSVP</button>
        <span if={ total_rsvp && uR.auth.user.is_superuser } data-reddot={ total_rsvp }></span>
      </div>
      <div if={ !full && !authenticated }>
        You must
        <a href="/accounts/login/?next={ session.get_absolute_url|urlencode }">Login</a>
        to RSVP
      </div>
    </div>
    <div if={ past }>
      <span class="btn btn-warning">You can no longer RSVP</span>
    </div>
  </div>

  var self = this;
  this.on('mount',function() {
    this.start_string = moment(this.start).format("ddd MMM D, YYYY h:mm a");
    this.start_slug = moment(this.start).format("YYYY/MM/DD");

    uR.auth.ready(function() {
      self.authenticated = uR.auth.user;
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
