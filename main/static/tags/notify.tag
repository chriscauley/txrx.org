uR.ready(function() {
  uR.addRoutes({
    "^/notify/$":uR.auth.loginRequired(function(path,data) { uR.mountElement("ur-notify",data); }),
  });
});

<ur-notify>
  <p class="lead col-sm-12">
    Change your <a href="/notify/settings/">notification settings</a> to choose to be notified by text, email, or none.
  </p>
  <div class="col-sm-6">
    <p class="lead" if={ !unread.length && !recent.length }>
      You have no notifications
    </p>
    <div if={ unread.length }>
      <h3>Unread Notifications</h3>
      <ul class={ uR.theme.list }>
        <li each={ unread } class={ uR.theme.list_item }><a href={ url }>{ message }</a></li>
      </ul>
    </div>
    <div if={ recent.length }>
      <h3>Past Notifications</h3>
      <ul class={ uR.theme.list }>
        <li each={ recent } class={ uR.theme.list_item }><a href={ url }>{ message }</a></li>
      </ul>
    </div>
    <div if={ older }>
      <a onclick={ loadMore }>View Older...</a>
    </div>
  </div>
  <div class="col-sm-6" if={ follows }>
    <h3>Things You Are Following</h3>
    <ul class={ uR.theme.list }>
      <li each={ follows } class={ uR.theme.list_item }>
        <a href={ url }>{ name }</a>
        <a class="{ uR.theme.list_right } fa fa-close" href={ unfollow_url } if={ !deleted }> </a>
      </li>
      <li if={ follows.length > 1 } class={ uR.theme.list_item_danger }>
        <a href="/notify/unsubscribe/notify_course/{ uR.auth.user.id }">Unfollow All</a>
      </li>
    </ul>
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
    });
    uR.ajax({
      url: "/api/notify/follow/",
      success: function(data) {
        self.follows = data;
      },
      that: this
    });
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
