(function() {
  function mainMount(html,data) {
    var tag_name = /[\w-]+/g.exec(html)[0];
    document.getElementById("main").innerHTML = "<"+tag_name+">";
    riot.mount(tag_name,data);
  }
  function fromTemplate(template_name) {
    riot.compile(
      "/static/templates/"+template_name+".html",
      function(html) {
        mainMount(template_name);
      }
    );
  }
  var _route = {
    checkout: function() {
      mainMount("tool-checkout");
    },
    "checkin-home": function() {
      mainMount("checkin-home");
    },
    toolmaster: function(search_term) {
      mainMount("toolmaster",{search_term:search_term});
    },
    "my-permissions": function() { mainMount('badge') },
    rfid: function() { mainMount("set-rfid"); },
    "week-hours": function() { mainMount("week-hours"); },
    "needed-sessions": function() { fromTemplate("needed-sessions"); }
  };
  window.R = _route
  function route(name) {
    if (! _route[name]) { return }
    _route[name].apply(this,Array.prototype.slice.call(arguments,1));
  };
  TXRX.route = route;
  TXRX.mainMount = mainMount;
  pathpart = window.location.pathname.split("/")[2]
  route(pathpart);
})();
