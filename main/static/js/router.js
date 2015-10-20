(function() {
  function mainMount(html,data) {
    var tag_name = /[\w-]+/g.exec(html)[0];
    document.getElementById("main").innerHTML = html;
    riot.mount(tag_name,data);
  }
  var _route = {
    checkout: function() {
      mainMount("<tool-checkout></tool-checkout>");
    },
    checkin: function() {
      mainMount("<modal><checkin></checkin></modal>");
    },
    toolmaster: function(search_term) {
      mainMount("<toolmaster></toolmaster>",{search_term:search_term});
    },
    "my-permissions": function() { mainMount('<badge>') },
    rfid: function() { mainMount("<set-rfid>"); },
    "week-hours": function() { mainMount("<week-hours>"); },
  };
  window.R = _route
  riot.route(function() {
    var page_name = arguments[0] || "home";
    if (! _route[page_name]) { return }
    _route[page_name].apply(this,Array.prototype.slice.call(arguments,1));
  });
  riot.route(window.location.hash.slice(1))
})();
