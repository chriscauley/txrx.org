(function() {
  var _route = {
    checkout: function() {
      document.getElementById("main").innerHTML = "<tool-checkout></tool-checkout>";
      riot.mount("tool-checkout");
    },
    checkin: function() {
      document.getElementById("main").innerHTML = "<modal><checkin></checkin></modal>";
      riot.mount("modal");
    }
  };
  riot.route(function() {
    if (! _route[arguments[0]]) { return }
    _route[arguments[0]].apply(Array.prototype.slice.call(arguments,1));
  });
})();
