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
    criterion: function(pk) {
      $.get(
        "/api/tool/criterion/"+pk+"/",
        function(data) {
          data.pk = pk;
          mainMount("<authorize-criterion></authorize-criterion>",data);
        },
        'json'
      );
    }
  };
  riot.route(function() {
    if (! _route[arguments[0]]) { return }
    _route[arguments[0]].apply(this,Array.prototype.slice.call(arguments,1));
  });
  riot.route(window.location.hash.slice(1))
})();
