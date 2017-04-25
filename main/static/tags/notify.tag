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
    <p class="lead" if={ !future.length && !past.length }>
      You have no notifications
    </p>
    <div if={ future.length }>
      <h3>New Notifications</h3>
      <ul class={ uR.theme.list }>
        <li each={ future } class={ className }><a href={ url }>{ message }</a></li>
      </ul>
    </div>
    <div if={ past.length }>
      <h3>Past Notifications</h3>
      <ul class={ uR.theme.list }>
        <li each={ past } class={ className }><a href={ url }>{ message }</a></li>
      </ul>
    </div>
    <div if={ older }>
      <a onclick={ loadMore }>View Older...</a>
    </div>
  </div>
  <div class="col-sm-6" if={ follows }>
    <h3>Things You Are Following</h3>
    <ul class={ uR.theme.list }>
      <li each={ follows } class={ className }>
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
    this.ajax({
      url: "/api/notify/feed/",
      success: function(data) {
        self.data = data;
      },
    });
    this.ajax({
      url: "/api/notify/follow/",
      success: function(data) {
        self.follows = data;
      },
    });
  });
  this.on("update",function() {
    if (!this.follows || !this.data) { return; }
    this.ready = true;
    this.future = [];
    this.past = [];
    this.older = 0;
    uR.forEach(this.data || [],function(notification) {
      (moment(new Date(notification.expires))<moment()?this.past:this.future).push(notification);
      notification.className = (notification.target_type || "").replace(/\./g,"")+" "+uR.theme.list_item;
    }.bind(this));
    uR.forEach(this.follows,function(f) { f.className = uR.theme.list_item });
  });
  loadMore(e) {
    alert('not implmented');
  }
</ur-notify>
