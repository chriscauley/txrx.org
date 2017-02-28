uR.ready(function() {
  uR.addRoutes({
    "^/notify/$":function(path,data) { uR.mountElement("ur-notify",data); }
  });
});

<ur-notify>
  <p class="lead">
    Checkout <a href="/notify/settings/">notification settings</a> to control whether notifications are sent by email or text or not at all.
  </p>
  <div if={ unread && unread.length }>
    <h3>Unread Notifications</h3>
    <ul>
      <li each={ unread }><a href={ url }>{ message }</a></li>
    </ul>
  </div>
  <div if={ recent && recent.length }>
    <h3>Past Notifications</h3>
    <ul>
      <li each={ recent }><a href={ url }>{ message }</a></li>
    </ul>
  </div>
  <div if={ older }>
    <a onclick={ loadMore }>View Older...</a>
  </div>

  var self = this;
  this.on("mount",function() {
    uR.ajax({
      url: "/api/notify/feed/",
      success: function(data) {
        self.data = data;
        self.ready = false;
      },
      that: this
    })
  });
  this.on("update",function() {
    if (this.ready || !this.data) { return; }
    this.ready = true;
    this.unread = [];
    this.recent = [];
    this.older = 0;
    uR.forEach(self.data || [],function(notification) {
      (notification.read?self.recent:self.unread).push(notification);
    });
  });
  loadMore(e) {
    alert('not implmented');
  }
</ur-notify>
