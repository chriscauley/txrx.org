(function() {
  var _routes = {
    "^/redtape/(\\d+)/(.*)/": function(path,data) {
      uR.ajax({
        url: "/durf/redtape/document/"+data.matches[1]+"/",
        success: function(data) {
          uR.mountElement("ur-document",data);
        },
      });
    },
  }
  uR.addRoutes(_routes);
})();

<ur-document>
  <div class={ theme.outer }>
    <div class={ theme.header }><h3>{ opts.name }</h3></div>
    <div class={ theme.inner }>
      <div class="inner-content"></div>
      <ur-form method="POST" action="//"></ur-form>
    </div>
  </div>

  this.on("mount",function() {
    this.update();
    this.root.querySelector(".inner-content").innerHTML = this.opts.content;
  });
</ur-document>
