// JWT decode functions

var JWT = (function() {
  function urlBase64Decode(str) {
    var output = str.replace(/-/g, '+').replace(/_/g, '/');
    if (output.length%4 == 1) { throw 'Illegal base64url string!'; }
    else if (output.length%4 == 2) { output += '=='; }
    else if (output.length%4 == 3) { output += '='; }
    return window.decodeURIComponent(escape(window.atob(output)));
  }

  function getToken() {
    var token = localStorage.getItem("jwt-token");
    var parts = token.split('.');
    if (parts.length !== 3) { throw new Error('JWT must have 3 parts'); }
    var decoded = urlBase64Decode(parts[1]);
    if (!decoded) { throw new Error('Cannot decode the token'); }

    return JSON.parse(decoded);
  }

  function getTokenExpirationDate() {
    var token = getToken();
    if(typeof token.exp === "undefined") { return null; }
    var d = new Date(0); // The 0 here is the key, which sets the date to the epoch
    d.setUTCSeconds(token.exp);
    return d;
  };

  function isTokenExpired(offsetSeconds) {
    var d = getTokenExpirationDate();
    offsetSeconds = offsetSeconds || 0;
    if (d === null) { return false; }

    // Token expired?
    return !(d.valueOf() > (new Date().valueOf() + (offsetSeconds * 1000)));
  };

  return {
    'getTokenExpirationDate': getTokenExpirationDate,
    'isTokenExpired': isTokenExpired,
  }
})()

function checkToken(data) {
  if (data) { var new_token = data['token']; }
  else { var new_token = readCookie('JWT-Token'); }
  if (new_token) { localStorage.setItem('jwt-token',new_token); }
}
checkToken();
