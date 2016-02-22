// JWT decode functions

var JWT = (function() {
  function hasToken() {
    return !!localStorage.getItem("jwt-token");
  }
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
    if (!hasToken()) { return true; }
    var d = getTokenExpirationDate();
    offsetSeconds = offsetSeconds || 0;
    if (d === null) { return false; }

    // Token expired?
    return !(d.valueOf() > (new Date().valueOf() + (offsetSeconds * 1000)));
  };

  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("Authorization", "JWT "+ localStorage.getItem('jwt-token'));
      }
    }
  });

  function readCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
      var c = ca[i];
      while (c.charAt(0)==' ') c = c.substring(1,c.length);
      if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
  }

  function updateToken(data) {
    if (data) { var new_token = data['token']; }
    else { var new_token = readCookie('JWT-Token'); }
    if (new_token) { localStorage.setItem('jwt-token',new_token); }
  }
  updateToken()
  function startLogin(callback,args,params) {
    params = params || '';
    var modal = document.createElement("modal");
    modal.appendChild(document.createElement("login"));
    document.body.appendChild(modal);
    function success(pk) { callback.apply(this,args); }
    riot.mount("modal",{success:success,title: "Please login to continue"});
  }

  function loginRequired(func,params) {
    return function() {
      if (isTokenExpired()) { startLogin(func,arguments,params); }
      else { func.apply(this,arguments); }
    }
  }

  return {
    'getTokenExpirationDate': getTokenExpirationDate,
    'isTokenExpired': isTokenExpired,
    'updateToken': updateToken,
    'startLogin': startLogin,
    'loginRequired': loginRequired,
  }
})()

