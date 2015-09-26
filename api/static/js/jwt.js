// JWT decode functions

var JWT = (function() {
  function urlBase64Decode(str) {
    var output = str.replace(/-/g, '+').replace(/_/g, '/');
    if (output.length%4 == 1) { throw 'Illegal base64url string!'; }
    else if (output.length%4 == 2) { output += '=='; }
    else if (output.length%4 == 3) { output += '='; }
    return window.decodeURIComponent(escape(window.atob(output)));
  }
})()
