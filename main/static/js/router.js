(function() {
  var _route = {
    checkout: function() {
      document.getElementById("main").innerHTML = "<tool-checkout></tool-checkout>";
      riot.mount("tool-checkout");
      for (var i=0; i<arguments.length;i++) { console.log('checkout'+arguments[i]); }
    }
  };
  riot.route(function() {
    _route[arguments[0]].apply(Array.prototype.slice.call(arguments,1));
    for (var i=0; i<arguments.length;i++) { console.log(arguments[i]); }
  });
  riot.route('checkout')
})();
