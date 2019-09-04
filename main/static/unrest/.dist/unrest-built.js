'use strict';

// https://jsfiddle.net/warpech/8dyx615f/
(function loadURLShim() {
  var airbrake = window.airbrake || { log: function log(e) {
      console.error(e);
    } };
  try {
    new URL(window.location.href, window.location.origin);
    new URL(window.location.href, undefined);
    return;
  } catch (e) {
    airbrake.log("Reason for using url shim:", e);
    airbrake.log(e);
  }
  window.URL = function shimURL(url, base) {
    var iframe = document.createElement('iframe');
    iframe.style.display = 'none';
    document.body.appendChild(iframe);
    iframe.contentWindow.document.write('<base href="' + base + '"><a href="' + url + '"></a>');
    var a = iframe.contentWindow.document.querySelector('a');
    document.body.removeChild(iframe);
    return a;
  };
})();
// ie11 polyfill
if (!String.prototype.startsWith) {
  String.prototype.startsWith = function (searchString, position) {
    position = position || 0;
    return this.indexOf(searchString, position) === position;
  };
}
"use strict";

var _typeof = typeof Symbol === "function" && typeof Symbol.iterator === "symbol" ? function (obj) { return typeof obj; } : function (obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; };

var uR = function () {
  var uR = window.uR || {};
  uR.timeIt = function (f, name) {
    name = name || f.name;
    return function () {
      var start = new Date();
      f.apply(this, arguments);
      console.log(name, "took", (new Date() - start) / 1000);
    };
  };
  uR.Ready = function Ready(isReady, _ready) {
    isReady = isReady || function () {
      return false;
    };
    _ready = _ready || [];
    function log() {
      //console.log.apply(this,arguments);
    }
    function error() {
      //console.error.apply(this,arguments);
    }
    var ready = function ready() {
      uR.forEach(arguments || [], function (f) {
        window.airbrake && f.name && window.airbrake.log("ready: " + f.name);
        if (typeof f == "function") {
          _ready.push(f);log('in queue', f.name);
        } else {
          log(f);
        }
      });
      var in_queue = _ready.length;
      while (isReady() && _ready.length) {
        log("doing it!");
        _ready.shift()();
      }
      error("Ready", in_queue, _ready.length);
    };
    ready._name = isReady.name;
    ready.start = function () {
      window.airbrake && window.airbrake.log("unrest starting");
      isReady = function isReady() {
        return true;
      };
      ready();
    };
    return ready;
  };

  uR.serialize = function serialize(form) {
    var field,
        s = [];
    if ((typeof form === "undefined" ? "undefined" : _typeof(form)) != 'object' && form.nodeName != "FORM") {
      return;
    }
    var len = form.elements.length;
    for (i = 0; i < len; i++) {
      field = form.elements[i];
      if (!field.name || field.disabled || field.type == 'file' || field.type == 'reset' || field.type == 'submit' || field.type == 'button') {
        continue;
      }
      if (field.type == 'select-multiple') {
        for (j = form.elements[i].options.length - 1; j >= 0; j--) {
          if (field.options[j].selected) s[s.length] = encodeURIComponent(field.name) + "=" + encodeURIComponent(field.options[j].value);
        }
      } else if (field.type != 'checkbox' && field.type != 'radio' || field.checked) {
        s[s.length] = encodeURIComponent(field.name) + "=" + encodeURIComponent(field.value);
      }
    }
    return s.join('&').replace(/%20/g, '+');
  };
  uR.getQueryParameter = function getQueryParameter(name, search) {
    var regexp = new RegExp("[\?&](?:" + name + ")=([^&]+)");
    var _sd = (search || window.location.search).match(regexp);
    if (_sd) {
      return unescape(_sd[1]);
    }
  };

  uR.getQueryDict = function (str) {
    str = str || window.location.search;
    var obj = {};
    str.replace(/([^=&?]+)=([^&]*)/g, function (m, key, value) {
      obj[decodeURIComponent(key)] = decodeURIComponent(value);
    });
    return obj;
  };

  uR.cookie = {
    set: function set(name, value, days) {
      var expires = "";
      if (days) {
        var date = new Date();
        date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
        expires = "; expires=" + date.toGMTString();
      }
      document.cookie = name + "=" + value + expires + "; path=/";
    },
    get: function get(name) {
      var nameEQ = name + "=";
      var ca = document.cookie.split(';');
      for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
          c = c.substring(1, c.length);
        }if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
      }
      return null;
    },
    delete: function _delete(name) {
      this.set(name, "", -1);
    }
  };

  function isEmpty(obj) {
    for (var key in obj) {
      return false;
    }
    return true;
  }

  uR.ajax = function ajax(opts) {
    // create default options
    // note: !!form is always true, opts.form can be undefined (falsey)
    // but form.some_property will always be false if there is no form!
    // #! TODO: Everythin on tag should be moved to AjaxMixin
    var form = opts.form || {};
    var method = (opts.method || form.method || "GET").toUpperCase();
    var data = opts.data;
    var target = opts.target || opts.form; // default to body?
    var url = opts.url || form.action || '.';
    window.airbrake && window.airbrake.log("AJAX: " + url);
    var that = opts.that;
    if (that) {
      console.warn('"that" has been depracated in favor of "tag".');
    }
    var tag = that || opts.tag;
    var loading_attribute = opts.loading_attribute || tag && tag.loading_attribute || uR.config.loading_attribute;
    var success_attribute = opts.success_attribute || "";
    var success_reset = opts.success_reset || false;
    var success = (opts.success || function (data, request) {}).bind(tag);
    var error = (opts.error || function (data, request) {}).bind(tag);
    var filenames = opts.filenames || {};
    if (tag) {
      tag.messages = opts.messages || [];
      tag._ajax_busy = true;
      tag.form_error = undefined;
      if (!target && tag.target) {
        console.warn("Use of tag.target is depracated in favor of tag.ajax_target");
      }
      target = target || tag.target || tag.ajax_target;
      if (typeof target == "string") {
        target = tag.root.querySelector(target) || document.querySelector(target);
      }
    }

    // mark as loading
    if (target) {
      target.removeAttribute("data-success");
      target.setAttribute("data-loading", loading_attribute);
    }

    // create form_data from data or form
    if (!data && opts.form) {
      data = {};
      uR.forEach(opts.form.elements, function (element) {
        if (element.type == "file") {
          data[element.name] = element.files[0];
          filenames[element.name] = element.files[0].name;
        } else {
          data[element.name] = element.value;
        }
      });
    }
    // POST uses FormData, GET uses query string
    var form_data = new FormData(opts.form);
    if (method == "POST" && data) {
      for (var key in data) {
        filenames[key] ? form_data.append(key, data[key], filenames[key]) : form_data.append(key, data[key]);
      };
    }
    if (method != "POST") {
      url += url.indexOf("?") == -1 ? "?" : "&";
      for (key in data) {
        url += key + "=" + encodeURIComponent(data[key]) + "&";
      }
    }

    // create and send XHR
    var request = new XMLHttpRequest();
    request.open(method, url, true);
    request.setRequestHeader("X-Requested-With", "XMLHttpRequest");

    if ("POSTDELETE".indexOf(method) != -1 && uR.cookie.get("csrftoken")) {
      request.setRequestHeader("X-CSRFToken", uR.cookie.get("csrftoken"));
    }
    request.onload = function () {
      try {
        var data = JSON.parse(request.response);
      } catch (e) {
        var data = {};
      }
      if (data.status == 401) {
        return uR.auth.loginRequired(function () {
          uR.ajax(opts);
        })();
      }
      if (target) {
        target.removeAttribute('data-loading');
      }
      var errors = data.errors || {};
      if (data.error) {
        errors = { non_field_error: data.error };
      }
      var non_field_error = errors.non_field_error || errors.__all__; // __all__ is django default syntax
      if (isEmpty(errors) && request.status != 200) {
        non_field_error = opts.default_error || "An unknown error has occurred";
      }
      if (tag && tag.form && tag.form.field_list) {
        uR.forEach(tag.form.field_list, function (field, i) {
          field.data_error = errors[field.name];
          if (field.data_error && data.html_errors && ~data.html_errors.indexOf(field.name)) {
            field.html_error = field.data_error;
          }
          field.valid = !field.data_error;
          field.show_error = true;
        });
      }
      if (non_field_error) {
        // if there's no form and no error function in opts, alert as a fallback
        if (tag) {
          tag.non_field_error = non_field_error;
          if (data.html_errors && ~data.html_errors.indexOf("non_field_error")) {
            tag.non_field_html_error = true;
          }
        } else if (!opts.error) {
          uR.alert(non_field_error);
        }
      }

      var complete = request.status == 200 && isEmpty(errors);
      (complete ? success : error)(data, request);
      uR.pagination = data.ur_pagination || uR.pagination;
      if (target && complete && !data.messages) {
        target.setAttribute("data-success", success_attribute);
      }
      if (tag) {
        tag._ajax_busy = false;
        tag.messages = data.messages || [];
        tag.update();
      }
      uR.postAjax && uR.postAjax.bind(request)(request);
      if (data.ur_route_to) {
        uR.route(data.ur_route_to);
      }
    };
    request.send(form_data);
  };

  var AjaxMixin = {
    init: function init() {
      this.ajax = function (options, e) {
        e = e || {};
        options.tag = options.tag || this;
        options.target = options.target || this.ajax_target || this.theme && this.root.querySelector(this.theme.outer);
        options.target = options.target || e.target;
        options.success = options.success || this.ajax_success || uR.default_ajax_success;
        options.url = options.url || this.ajax_url;
        uR.ajax(options);
      };
    }
  };
  window.riot && riot.mixin(AjaxMixin);
  uR.default_ajax_success = function (data, request) {
    uR.extend(uR.data, data);
  };

  uR.debounce = function debounce(func, wait, immediate) {
    var timeout,
        wait = wait || 200;
    return function () {
      var context = this,
          args = arguments;
      var later = function later() {
        timeout = null;
        if (!immediate) func.apply(context, args);
      };
      var callNow = immediate && !timeout;
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
      if (callNow) func.apply(context, args);
      return true;
    };
  };

  uR.dedribble = function dedribble(func, wait, end_bounce) {
    var timeout,
        wait = wait || uR.config.dribble_time || 200,
        end_bounce = end_bounce !== undefined && true;
    var last = new Date();
    return function () {
      var context = this,
          args = arguments;
      if (end_bounce) {
        var later = function later() {
          timeout = null;
          func.apply(context, args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
      }
      if (new Date() - last > wait) {
        func.apply(context, args);last = new Date();
      }
    };
  };

  // this function may someday be replaced with rambdas map
  uR.forEach = function forEach(array, func, context) {
    if (context) {
      func = func.bind(context);
    }
    for (var i = 0; i < array.length; i++) {
      func(array[i], i, array);
    }
  };

  // this function may someday be replaced with rambdas merge
  uR.extend = function (a, b) {
    for (var i in b) {
      if (b.hasOwnProperty(i)) {
        a[i] = b[i];
      }
    }
  };

  // uR.ready is a function for handling window.onload
  uR.ready = new uR.Ready(undefined, uR._ready);
  window.onload = function () {
    uR.ready.start();
    uR.route && uR.route(window.location.href);
    // #! dummy route function. This is so everything can use uR.route without router.js
    uR.route = uR.route || function route(path, data) {
      window.location = path;
    };
  };

  uR.getSchema = function getSchema(url, callback) {
    uR.ajax({
      url: url,
      success: function success(data) {
        uR.schema[url] = data.schema;
        uR.schema[url].form_title = data.form_title;
        uR.schema[url].rendered_content = data.rendered_content;
        if (window.markdown && window.markdown.toHTML && data.markdown && !data.rendered_content) {
          uR.schema[url].rendered_content = markdown.toHTML(data.markdown);
        }
        uR.schema.__initial[url] = data.initial;
        uR.pagination = data.ur_pagination;
        callback && callback();
      }
    });
  };

  uR.onBlur = uR.onBlur || function () {};
  uR.config = uR.config || {};
  uR.config.doPostAuth = function () {};
  uR.config.form = {};
  uR.config[404] = 'four-oh-four';
  uR.config.form.field_class = "input-field";
  uR.config.loading_attribute = uR.config.loading_attribute || 'fade';
  uR.config.loading_attribute = 'fade';
  uR.config.select_class = 'browser-default';
  uR.config.tag_templates = [];
  uR.config.input_overrides = {};
  uR.config.text_validators = {};
  uR.config.mount_to = "#content";
  uR.config.mount_alerts_to = "#alert-div";
  uR.config.btn_primary = "btn blue";
  uR.config.btn_success = "btn green";
  uR.config.btn_cancel = "btn red";
  uR.config.btn_warning = "btn yellow";
  uR.config.cancel_text = "Cancel";
  uR.config.success_text = "Submit";
  uR.config.alert_success = "alert alert-success card card-content"; // bootstrap
  uR._var = {};
  uR.data = uR.data || {};
  uR.alert = function (s) {
    console.log(s);
  }; //alert(s); }; // placeholder for future alert function
  uR.schema = { fields: {}, __initial: {} };
  uR.urls = {};
  uR.slugify = function (s) {
    if (typeof s != "string") {
      s = s.toString();
    }
    return s.toLowerCase().replace(/(^[\s-]+|[\s-]+$)/g, "").replace(/[^\d\w -]+/g, "").replace(/[\s-]+/g, "-");
  };
  uR.icon = {
    admin: 'fa fa-pencil-square-o'
  };
  uR.theme = {
    modal: {
      outer: "card",
      header: "card-title",
      content: "card-content",
      footer: "card-action"
    },
    default: {
      outer: "card",
      header: "card-title",
      content: "card-content",
      footer: "card-action"
    },
    error_class: "card red white-text"
  };
  uR.formatTimeRange = function formatTimeRange(start, end) {
    var start = moment(start),
        end = moment(end);
    var start_format = start.minute() ? "h:mm" : "h";
    var end_format = end.minute() ? "h:mm A" : "h A";
    if (start.hour() < 12 && end.hour() > 12) {
      start_format += " A";
    }
    return start.format(start_format) + " - " + end.format(end_format);
  };
  return uR;
}();
"use strict";

(function () {
  uR.static = function (s) {
    return uR.config.STATIC_URL + s;
  };
  uR.config.STATIC_URL = "/static/";
})();
"use strict";

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

(function () {
  var Storage = function () {
    function Storage(prefix) {
      _classCallCheck(this, Storage);

      this.PREFIX = prefix || "";
      this.META = this.PREFIX + "META/";
      this.EXIPIRY = '__expiry/'; // Key used for expiration storage
      this.default_expire_ms = 10 * 60 * 1000; // ten minutes
      this.defaults = {}; // table with default values
      this.times = {};
      if (!this.test_supported()) {
        console.warn("Storage not supported, falling back to dummy storage");
        this.FAKE_STORAGE = {};
        this.set = function (key, value) {
          this.FAKE_STORAGE[key] = value;
        };
        this.get = function (key) {
          return this.FAKE_STORAGE[key];
        };
        this.has = function (key) {
          this.FAKE_STORAGE.hasOwnProperty(key);
        };
        this.remove = function (key) {
          delete this.FAKE_STORAGE[key];
        };
      }
      //this.times = this.get(this.META+"times") || {};
    }

    _createClass(Storage, [{
      key: "get",
      value: function get(k) {
        // pull a json from local storage or get an object from the defaults dict
        var key = this.PREFIX + k;
        var value;
        if (localStorage.hasOwnProperty(key)) {
          try {
            value = JSON.parse(localStorage.getItem(key));
          } catch (e) {} // we only allow JSON here, so parse errors can be ignored
        } else if (this.defaults.hasOwnProperty(key)) {
          value = this.defaults[key];
        }
        return value;
      }
    }, {
      key: "set",
      value: function set(k, value) {
        // store stringified json in localstorage
        var key = this.PREFIX + k;
        if (!value && value !== 0) {
          localStorage.removeItem(key);return;
        }
        localStorage.setItem(key, JSON.stringify(value));
        this.times[key] = new Date().valueOf();
        this._saveTime();
      }
    }, {
      key: "has",
      value: function has(key) {
        return localStorage.hasOwnProperty(key);
      }
    }, {
      key: "remove",
      value: function remove(k) {
        var key = this.PREFIX + k;
        localStorage.removeItem(key);
        delete this.times[key];
        this._saveTime();
      }
    }, {
      key: "_saveTime",
      value: function _saveTime() {
        localStorage.setItem(this.META + 'times', JSON.stringify(this.times));
      }
    }, {
      key: "test_supported",
      value: function test_supported() {
        // incognito safari and older browsers don't support local storage. Use an object in ram as a dummy
        try {
          localStorage.setItem('test', '1');
          localStorage.removeItem('test');
          return true;
        } catch (e) {}
      }

      // below this is the api for the timebomb remote data store, which isn't used anywhere yet.
      // a dummy version of this would just allways execute a remote lookup and then callback.

    }, {
      key: "isExpired",
      value: function isExpired(key) {
        var expire_ms = this.get(this.EXPIRY + key) || this.setExpire(key);
        return expire_ms < new Date().valueOf();
      }
    }, {
      key: "setExpire",
      value: function setExpire(key, epoch_ms) {
        epoch_ms = epoch_ms || this.default_expire_ms + new Date().valueOf();
        this.set(this.EXPIRY + key, epoch_ms);
        return epoch_ms;
      }
    }, {
      key: "remote",
      value: function remote(url, callback) {
        var stored = this.get(url);
        if (stored && !this.isExpired(url)) {
          callback(stored);return;
        }
        uR.ajax({
          url: url,
          success: function (data) {
            this.set(url, data);
            this.setExpire(url);
            callback(data);
          }.bind(this)
        });
      }
    }]);

    return Storage;
  }();

  uR.storage = new Storage();
  uR.Storage = Storage;
})();
"use strict";

(function () {
  uR.mountElement = function mountElement(names, options) {
    options = options || {};
    if (options.ur_modal) {
      options.mount_to = options.mount_to || uR.config.mount_alerts_to;
    }
    var mount_to = options.mount_to || uR.config.mount_to;
    var target = document.querySelector(mount_to);
    var children = target.childNodes;
    var i = target.childNodes.length;
    while (i--) {
      target.removeChild(children[i]);
    }

    if (typeof names == "string") {
      names = [names];
    }
    var _t = [];
    uR.forEach(names, function (name) {
      name = name.replace(/\//g, ''); // Some tags pass in tag name for path like /hello-world/
      var element = document.createElement(name);
      if (options.innerHTML) {
        element.innerHTML = options.innerHTML;
      }
      target.appendChild(element);
      _t.push(mount_to + " " + name);
    });
    riot.mount(_t.join(","), options);
  };

  uR.alertElement = function alertElement(name, options) {
    options = options || {};
    if (!options.hasOwnProperty("ur_modal")) {
      options.ur_modal = true;
    }
    uR.mountElement(name, options);
  };

  function pushState(path, data) {
    if (window.location.pathname == path) {
      return;
    }
    // #! TODO the empty string here is the page title. Need some sort of lookup table
    history.replaceState({ path: path }, "" || document.title, path);
  }

  uR.pushState = uR.debounce(pushState, 100);

  uR.route = function route(href, data) {
    var new_url = new URL(href, href.match("://") ? undefined : window.location.origin);
    var old_url = new URL(window.location.href);
    var pathname = (new_url.pathname || href).replace(window.location.origin, "");

    uR.forEach(uR._on_routes, function (f) {
      f(pathname, data);
    });
    data = data || {};
    for (var key in uR._routes) {
      var regexp = new RegExp(key);
      var path_match = pathname.match(regexp);
      if (path_match) {
        uR.STALE_STATE = true;
        data.matches = path_match;
        uR._routes[key](pathname, data);
        document.body.dataset.ur_path = pathname;
        uR.pushState(href);
      } else if (new_url.hash && key.indexOf("#") != -1) {
        data.matches = new_url.hash.match(regexp);
        if (data.matches) {
          data.ur_modal = true;
          data.cancel = function () {
            window.location.hash = "";
            this.unmount();
          };
          uR.STALE_STATE = true;
          uR._routes[key](pathname, data);
          uR.pushState(href);
        }
      }
    }
    if (data.matches) {
      return;
    }
    // uR.config.do404();

    // #! TODO The following is used for django pages + back button
    // We're not in the single page app, reload if necessary
    if (uR.STALE_STATE) {
      window.location = href;
    }
    uR.STALE_STATE = true;
  };

  function onClick(e) {
    // Borrowed heavily from riot
    // this will stop links from changing the page so I can use href instead of onclick
    if (e.which != 1 // not left click
    || e.metaKey || e.ctrlKey || e.shiftKey // or meta keys
    || e.defaultPrevented // or default prevented
    ) return;

    var el = e.target,
        loc = window.history.location || window.location;
    if (el && el.nodeName) {
      var selector = el.nodeName;
      if (el.id) {
        "#" + el.id;
      }
      if (el.className) {
        selector += "." + el.className;
      }
      if (el.name) {
        selector += "[name=" + el.name + "]";
      }
      window.airbrake && window.airbrake.log("clicked: " + selector);
    }
    while (el && el.nodeName != 'A') {
      el = el.parentNode;
    }if (!el || el.nodeName != 'A' // not A tag
    || el.hasAttribute('download') // has download attr
    || !el.hasAttribute('href') // has no href attr
    || el.target && el.target != '_self' // another window or frame
    || el.href.indexOf(loc.href.match(/^.+?\/\/+[^\/]+/)[0]) == -1 // cross origin
    ) return;

    /*if (el.href != loc.href && (
      el.href.split('#')[0] == loc.href.split('#')[0] // internal jump
        || el.href.startsWith("#") // hash only
        || base[0] != '#' && getPathFromRoot(el.href).indexOf(base) !== 0 // outside of base
        || base[0] == '#' && el.href.split(base)[0] != loc.href.split(base)[0] // outside of #base
        || !go(getPathFromBase(el.href), el.title || document.title) // route not found
    )) return*/
    e.preventDefault();
    uR.route(el.href);
  }

  uR.addRoutes = function (routes) {
    uR.extend(uR._routes, routes);
  };
  uR.startRouter = function () {
    document.addEventListener('click', onClick);
    // window.popstate = function(event) { console.log("pop",window.location.href); uR.route(window.location.href,event.state,false); };
  };

  uR.config.do404 = function () {
    uR.mountElement("four-oh-four");
  };
  uR._routes = uR._routes || {};
  uR._on_routes = [];
  uR.onRoute = function (f) {
    uR._on_routes.push(f);
  };
  uR.router = {
    routeElement: function routeElement(element_name) {
      return function (pathname, data) {
        return uR.mountElement(element_name, data);
      };
    }
  };
})();
"use strict";

var _slicedToArray = function () { function sliceIterator(arr, i) { var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"]) _i["return"](); } finally { if (_d) throw _e; } } return _arr; } return function (arr, i) { if (Array.isArray(arr)) { return arr; } else if (Symbol.iterator in Object(arr)) { return sliceIterator(arr, i); } else { throw new TypeError("Invalid attempt to destructure non-iterable instance"); } }; }();

(function () {
  String.lunch = {
    moment_cache: {},
    s2_cache: {},

    date: "YYYYMMDD",
    time: "Hmm",
    datetime: "",

    hdate: "MMM Do, YYYY",
    hdate_no_year: "MMM Do",
    htime_hour: "H? A",
    htime_minute: ":mm"
  };

  var Sl = String.lunch;
  String.prototype.moment = function moment() {
    if (String.lunch.moment_cache[this]) {
      return String.lunch.moment_cache[this];
    }
    var s1 = this,
        m1,
        s2,
        m2;
    if (s1.indexOf("||") != -1) {
      var _s1$split = s1.split("||");

      var _s1$split2 = _slicedToArray(_s1$split, 2);

      s1 = _s1$split2[0];
      s2 = _s1$split2[1];
    }
    if (this.match(/^\d\d?:\d\d/)) {
      // passing in time with no date, set date to today
      m1 = window.moment(window.moment().format("YYYY-MM-DD ") + s1);
    } else {
      var m1 = window.moment(s1.toString());
    }
    if (s2 && s2.match(/^\d\d?:\d\d/)) {
      s2 = m1.format(Strin.lunch.date) + " " + s2;
      m2 = window.moment(s2);
      if (m2 < m1) {
        m2 = m2.add(1, 'days');
      }
    }
    String.lunch.moment_cache[this] = m1;
    String.lunch.s2_cache[this] = s2;
    return m1;
  };
  String.prototype.format = function (s) {
    return this.moment().format(s);
  };
  String.prototype.calendar = function calendar(s) {
    return this.moment().calendar(s);
  };
  String.prototype.range = function (format) {
    this.moment();
    return this.hdate() + " - " + Sl.s2_cache[this].hdate();
  };
  String.prototype.htimerange = function (format) {
    this.moment();
    var m1 = this.moment();
    var m2 = Sl.s2_cache[this].moment();
    var time1 = m1.format(m1.minute() ? "h:mm" : "h"); // 12 or 12:45
    if (m1.hour() >= 12 != m2.hour() >= 12) {
      time1 += m1.format(" A");
    } // add am/pm if am/pm changes from time1 to time2
    return time1 + " - " + Sl.s2_cache[this].htime(); // h(:mm)? (am|pm)? - h(:mm)? am|pm
  };

  String.prototype.date = function date() {
    return this.moment().format(Sl.date);
  };
  String.prototype.time = function time() {
    return this.moment().format(Sl.time);
  };
  String.prototype.datetime = function datetime() {
    return this.moment().format(Sl.datetime);
  };

  String.prototype.hdate = function () {
    var now = window.moment();
    var m = this.moment();
    var diff = m - now;
    if (Math.abs(diff) < 1000 * 3600 * 24 * 60) {
      // less than two months away from now
      if (now.month() == m.month() && now.date() == m.date()) {
        return "Today";
      }
      if (diff > 0) {
        if (diff < 1000 * 3600 * 24) {
          return "Tomorrow";
        }
      }
      return m.format(String.lunch.hdate_no_year);
    }
    return m.format(String.lunch.hdate);
  };
  String.prototype.htime = function htime() {
    var m = this.moment();
    return m.format('h? A').replace("?", m.minutes() ? m.format(":mm") : "");
  };
  String.prototype.hdatetime = function () {
    return this.hdate() + " at " + this.htime();
  };
  String.prototype.itime = function () {
    return parseInt(this.time());
  };
  String.prototype.unixtime = function () {
    return this.moment() + 0;
  };
})();
"use strict";

var _typeof = typeof Symbol === "function" && typeof Symbol.iterator === "symbol" ? function (obj) { return typeof obj; } : function (obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; };

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

(function () {
  uR.auth = uR.auth || {};
  uR.auth.loginRequired = function loginRequired(func, data) {
    if (typeof func == "string") {
      var tagname = func;
      func = function func(path, data) {
        uR.mountElement(tagname, data);
      };
    }
    data = data || {};
    function wrapped() {
      var args = arguments;
      uR.auth.ready(function () {
        function success(data) {
          if (data) {
            uR.auth.setUser(data.user);
          }
          func.apply(this, args);
        }
        if (!uR.auth.user || data.force) {
          uR.AUTH_SUCCESS = success;
          data.next = window.location.href;
          uR.route(uR.urls.auth.login, data);
        } else {
          success();
        }
      });
    }
    wrapped.login_required = true;
    return wrapped;
  };
  uR.auth.setUser = function setUser(user) {
    uR.storage.set('auth.user', user || null); // JSON.stringify hates undefined
    uR.auth.user = user;
    uR.auth.postAuth();
    riot.update(uR.auth.tag_names);
  };
  uR.auth.postAuth = function () {};
  uR.auth._getLinks = function () {
    return [{ url: "/accounts/logout/", icon: "sign-out", text: "Log Out" }];
  };
  uR.auth.getLinks = uR.auth._getLinks;
  uR.auth.auth_regexp = /\/auth\//;

  uR.schema.auth = {
    login: [{ name: 'username', label: 'Username or Email' }, { name: 'password', type: 'password' }],
    register: [{ name: 'email', label: 'Email Address', type: "email" }, { name: 'password', type: 'password' }],
    'password-reset': [{ name: 'email', label: 'Email Address', type: "email" }]
  };
  uR.urls.auth = {
    login: "#/auth/login/",
    register: "#/auth/register/",
    password_reset: "#/auth/forgot-password/"
  };
  uR.urls.api = uR.urls.api || {};
  uR.urls.api.login = "/auth/login_ajax/";
  uR.urls.api.register = "/api/register/"; // #! TODO
  uR.urls.api['password-reset'] = "/api/password-reset/"; // #! TODO
  uR.auth.tag_names = 'auth-dropdown,auth-modal';
  uR.addRoutes({
    "[?#]?/auth/(login|register|forgot-password)/": function authLoginRegisterForgotPassword(path, data) {
      uR.alertElement("auth-modal", data);
    },
    "[?#]?/auth/logout/": function authLogout(path, data) {
      uR.auth.setUser(null);
      uR.route("/accounts/logout/");
    }
  });

  uR.auth.user = uR.storage.get("auth.user");
  uR.ready(function () {
    riot.mount(uR.auth.tag_names);
    !uR.config.no_auth && uR.auth.reset();
  });
  var _ready = [];
  uR.auth.ready = function (f) {
    _ready.push(f);
  };
  uR.auth.reset = function (callback) {
    if (!uR.auth_enabled) {
      return;
    }
    callback = callback || function () {};
    uR.ajax({
      url: "/user.json",
      success: function success(data) {
        if (data.user != uR.auth.user) {
          uR.auth.setUser(data.user);
        }
        callback();
        uR.auth.ready = function (f) {
          f();
        };
        uR.forEach(_ready, uR.auth.ready);
      }
    });
  };
})();

riot.tag2('auth-modal', '<div class="{theme.outer}"> <div class="{theme.header}"> <h3>{title}</h3> </div> <div class="{theme.content}"> <div class="social" if="{slug != \'fogot_password\' && uR.auth.social_logins.length}"> <a class="btn btn-block btn-{icon}" href="{url}?next={next}" each="{uR.auth.social_logins}"> <i class="fa fa-{icon}"></i> Connect with {name}</a> <center>- or {slug} using your email address -</center> </div> <ur-form schema="{schema}" action="{url}" method="POST" ajax_success="{opts.success}"></ur-form> <center if="{slug == \'login\'}"> <a href="{urls.register}?next={next}">Create an Account</a><br> <a href="{urls.password_reset}?next={next}">Forgot Password?</a> </center> <center if="{slug == \'register\'}"> Already have an account? <a href="{urls.login}?next={next}">Login</a> to coninue </center> <center if="{slug == \'password_reset\'}"> Did you suddenly remember it? <a href="{urls.login}?next={next}">Login</a> </center> </div> </div>', '', '', function (opts) {
  var self = this;
  this.ajax_success = function (data, request) {
    (uR.AUTH_SUCCESS || function () {
      var path = self.next || window.location.pathname;
      if (path.match(uR.auth.auth_regexp)) {
        path = "/";
      }
      uR.route(path);
    })(data, request);
    self.unmount();
    uR.AUTH_SUCCESS = undefined;
  }.bind(this);
  this.on("mount", function () {
    if (uR.auth.user) {
      this.ajax_success({ user: uR.auth.user });
    }
    this.next = uR.getQueryParameter("next");
    this.slug = this.opts.slug || this.opts.matches[1];
    this.url = uR.urls.api[this.slug];
    this.schema = uR.schema.auth[this.slug];
    this.title = {
      login: "Please Login to Continue",
      register: "Create an Account",
      'forgot-password': "Request Password Reset"
    }[this.slug];
    this.update();
  });
  this.on("update", function () {

    this.urls = uR.urls.auth;
    if (window.location.pathname.match(uR.auth.auth_regexp)) {
      this.urls = {};
      for (var key in uR.urls.auth) {
        this.urls[key] = uR.urls.auth[key].replace("#", "");
      }
    }
    if (uR.auth.user) {
      self.ajax_success({ user: uR.auth.user });
    }
  });
  this.cancel = function (e) {
    if (window.location.pathname.match(uR.auth.auth_regexp)) {
      uR.route("/");
    }
    window.location.hash = "";
    this.unmount();
  }.bind(this);
});

riot.tag2('auth-dropdown', '<li if="{!uR.auth.user}"> <a href="{url}?next={window.location.pathname}"><i class="{icon}"></i> {text}</a> </li> <li if="{uR.auth.user}"> <a onclick="{toggle}">{uR.auth.user.username}</a> <ul class="dropdown-content"> <li each="{links}"><a href="{url}"><i class="fa fa-{icon}"></i> {text}</a></li> </ul> </li>', '', '', function (opts) {

  this.on("update", function () {
    if (uR.auth.user) {
      this.links = uR.auth.getLinks();
    } else {
      this.url = uR.auth.login_url || uR.urls.auth.login;
      this.icon = uR.auth.login_icon || "fa fa-user";
      this.text = uR.auth.login_text || "Login or Register";
    }
  });
  this.toggle = function (e) {
    this.root.classList[this.root.classList.contains("open") ? "remove" : "add"]("open");
  }.bind(this);
});

(function () {
  var DialogMixin = {
    init: function init() {
      if (this.opts.ur_modal) {
        this.theme = this.opts.theme || uR.theme.modal;
        var e = document.createElement('div');
        this.cancel = this.cancel || this.opts.cancel || function () {
          this.unmount();
        };
        e.addEventListener("click", function () {
          this.cancel();
        }.bind(this));
        e.setAttribute("ur-mask", true);
        if (this.root.childNodes.length) {
          this.root.insertBefore(e, this.root.childNodes[0]);
        } else {
          this.root.appendChild(e);
        }
      } else {
        this.theme = this.opts.theme || uR.theme[this.root.tagName] || uR.theme.default;
      }
    }
  };

  riot.mixin(DialogMixin);

  uR.alert = function (text, data) {
    data = data || {};
    data.close_text = data.close_text || "Close";
    data.innerHTML = "<center style='margin-bottom: 1em;'>" + text + "</center>";
    uR.alertElement("ur-modal", data);
  };
  uR.confirm = function (text, data) {
    if (typeof data == 'function') {
      data = { success: data };
    }
    data = data || {};
    data.buttons = data.buttons || [];
    data.close_text = data.close_text || "No";
    data.buttons.push({
      onclick: data.success,
      className: uR.config.btn_success,
      text: data.success_text || "Yes"
    });
    data.innerHTML = "<center style='margin-bottom: 1em;'>" + text + "</center>";
    uR.alert(text, data);
  };
})();

riot.tag2('ur-modal', '<div class="{theme.outer}"> <div class="{theme.content}"> <div class="inner-content"></div> <yield></yield> <center> <button onclick="{close}" class="{uR.config.btn_primary}">{close_text}</button> <button each="{opts.buttons}" class="{className}" onclick="{_onclick}">{text}</button> </center> </div> </div>', '', '', function (opts) {

  var self = this;
  this.close_text = this.opts.close_text || "Close";
  this.on("mount", function () {
    uR.forEach(this.opts.buttons || [], function (b) {
      b._onclick = function (e) {
        b.onclick(e);self.unmount();
      };
    });
    self.update();
  });
  this.close = function (e) {
    this.opts.cancel && this.opts.cancel();
    this.unmount();
  }.bind(this);
});

(function () {
  uR.form = {};
  uR.theme['UR-FORM'] = uR.theme.default;
  uR.ready(function () {
    if (uR.config.form_prefix != undefined) {
      var _routes = {};
      _routes[uR.config.form_prefix + "/([\\w\\.]+[\\w]+)/(\\d+)?/?$"] = function (path, data) {
        var url = "/api/schema/" + data.matches[1] + "/";
        if (data.matches[2]) {
          url += data.matches[2] + "/";
        }
        uR.form.current_form = data.matches[1];
        data.schema = url + (location.search || "?ur_page=0");
        data.method = "POST"; // #! TODO this should be an option tied to python schema
        uR.mountElement("ur-form", data);
      };
      uR.addRoutes(_routes);
    }
  });
  uR.__START = new Date().valueOf();
  uR._t = function (s) {
    console.log(new Date().valueOf() - uR.__START, s);
  };
  uR.form.parseChoices = function (choices) {
    // #! TODO This should eventually accomodate groupings as well like:
    // choices = [["group_name",[choice1,choice2,choice3]...],group2,group3]
    return choices.map(function (c) {
      if (typeof c == "string") {
        return [c, c];
      }
      return c;
    });
  };
  riot.mixin({ // anything with a ur-input like tag needs the following
    init: function init() {
      if (!this.opts.is_ur_input) {
        return;
      }
      this.field = this.opts.field;
      this.on("mount", function () {
        setTimeout(this.field.reset.bind(this.field), 0);
      });
    }
  });
  uR.form.URForm = function () {
    function URForm(ur_form) {
      _classCallCheck(this, URForm);

      this.form_tag = ur_form;
      this.opts = ur_form.opts;
      this.messages = [];
      this.prepSchema();
    }

    _createClass(URForm, [{
      key: "prepSchema",
      value: function prepSchema() {
        var tag = this.form_tag;
        var _schema = tag.opts.schema || tag._parent.opts.schema || tag._parent.schema;
        this.action = tag.opts.action;
        if (typeof _schema == "string") {
          this.schema_url = _schema;
          this.action = this.action || this.schema_url;
          if (uR.schema[this.schema_url]) {
            _schema = uR.schema[this.schema_url];
          } else {
            var url = _schema;
            uR.getSchema(url, this.prepSchema.bind(this));
            this._needs_update = true;
            _schema = [];
            return;
          }
        }
        this.empty_initial = uR.schema.__initial[this.schema_url] || this.form_tag.opts.initial || {};
        this.initial = uR.storage.get(this.form_tag.action) || this.empty_initial || {};

        tag.form_title = this.opts.form_title || _schema.form_title;
        tag.rendered_content = _schema.rendered_content;
        this.schema = _schema.map(function (field) {
          if (typeof field == "string") {
            field = { name: field };
          }
          var f = {};
          for (var k in field) {
            f[k] = field[k];
          }
          return f;
        });
        this.field_list = [];
        this.fields = {};
        uR.forEach(this.schema, function (field, i) {
          field.tagname = uR.config.input_overrides[field.type] || "ur-input";
          field._field_index = this.field_list.length;
          var cls = uR.form.fields[field.tagname] || uR.form.fields["ur-input"];
          this.field_list.push(new cls(this, field));
          this.fields[field.name] = this.field_list[this.field_list.length - 1];
        }.bind(this));
        if (this._needs_update) {
          this.form_tag.update();
          this.form_tag.update();
        };
        /*
        this.update();
        this.update();
        if (this.fields.length && !opts.no_focus) {
          setTimeout(function() {
            var f = self.root.querySelector("input:not([type=hidden]),select,textarea");
            f && f.focus();
            (self.opts.post_focus || function() {})(self);
          },0)
          }
        */
      }
    }, {
      key: "renderFields",
      value: function renderFields() {
        if (this._fields_rendered) {
          return;
        }
        this._fields_rendered = true;
        var targets = this.form_tag.root.querySelectorAll(".ur-input");
        uR.forEach(this.field_list, function (field, i) {
          targets[i].insertBefore(field.field_tag.root, targets[i].firstElementChild);
        });
        this.opts.onload && this.opts.onload.bind(this)();
        this.active = true; // form can now show errors
      }
    }]);

    return URForm;
  }();

  uR.form.URInput = function () {
    function URInput(form, options) {
      _classCallCheck(this, URInput);

      this.tag_name = this.tag_name || "ur-input"; // can be overridden by sub-classes
      this.form = form;
      if (typeof options == "string") {
        var name = options;
        if (uR.schema.fields[options]) {
          options = uR.schema.fields[options];
          options.name = name;
        } else {
          options = { name: name, type: 'text' };
        }
      }
      for (var k in options) {
        this[k] = options[k];
      }
      this.required = this.required == undefined || this.required; // defaults to true!

      this.name = this.name || this.type;
      if (_typeof(this.name) == "object") {
        // can't remember when this is used
        console.warn("look at me!");
        this.name = _typeof(this.name) == "object" ? this.name[0] : this.name;
      }
      this.value = this.initial_value = this.value || (this.form.initial || {})[this.name];
      this.valid = true;
      // verbose_name is useful for error messages, other generated text
      this.verbose_name = this.verbose_name || this.label || this.placeholder;
      if (!this.verbose_name) {
        var replace = function replace(s) {
          return s.charAt(0).toUpperCase() + s.substr(1).toLowerCase();
        };
        this.verbose_name = (this.name || "").replace(/[-_]/g, " ").replace(/\w\S*/g, replace);
      }
      this.label = this.label || this.verbose_name;
      this.id = this.id || "id_" + this.name + this.form.form_tag.suffix;
      this.input_tagname = this.input_tagname || this.type == "textarea" ? this.type : "input";
      this.input_type = this.type || "text";

      // if there's a validator, use type=text to ignore browser default
      if (uR.config.text_validators[this.name]) {
        this.validate = uR.config.text_validators[this.name];
        this.input_type = "text";
      }

      // It's easier to have an empty function than undefined, also make bouncy
      this.validate = this.validate || function () {
        return true;
      };
      //#! TODO: rethink bouncy validators as some kind of promise
      //this.validate = (this.bounce)?uR.debounce(this.validate.bind(f),this.bounce):this.validate;
      this.keyUp = this.keyUp || function () {};
      this.keyUp = this.bounce ? uR.debounce(this.keyUp.bind(f), this.bounce) : this.keyUp;

      // universal choice parser, maybe move to uR.form?
      if (this.choices) {
        this.choices_map = {};
        this.choices = uR.form.parseChoices(this.choices).map(function (choice_tuple, index) {
          this.choices_map[choice_tuple[0]] = choice_tuple[1];
          return {
            label: choice_tuple[1],
            id: this.id + "__" + index,
            value: uR.slugify(choice_tuple[0])
          };
        }.bind(this));
      }
      this.className = this.name + " " + this.type + " " + uR.config.form.field_class;
      var element = document.createElement(this.tagname);
      this.field_tag = riot.mount(element, { field: this, parent: this.form, is_ur_input: true })[0];
    }

    _createClass(URInput, [{
      key: "onKeyUp",
      value: function onKeyUp(e) {
        if (this.no_validation) {
          return;
        }
        if (e.type == "keyup") {
          self.active = true;
        }
        this.value = e.value || e.target && e.target.value || ""; // e.value is a way to fake events
        this.changed = this.last_value == this.value;
        this.last_value = this.value;
        this.empty = !this.value.length;
        var invalid_email = !/[^\s@]+@[^\s@]+\.[^\s@]+/.test(this.value);
        if (!this.required && !this.value) {
          invalid_email = false;
        }
        var was_valid = this.valid;
        this.valid = false;
        if (!this.required && this.empty) {
          this.valid = true;
        } else if (this.required && this.empty) {
          this.data_error = "This field is required.";
        } else if (this.value.length < this.minlength) {
          var type = ["number", "tel"].indexOf(this.type) == -1 ? " characters." : " numbers.";
          this.data_error = this.verbose_name + " must be at least " + this.minlength + type;
        } else if (this.maxlength && this.value.length > this.maxlength) {
          var type = ["number", "tel"].indexOf(this.type) == -1 ? " characters." : " numbers.";
          this.data_error = this.verbose_name + " cannot be more than " + this.maxlength + type;
        } else if (this.type == "email" && invalid_email) {
          this.data_error = "Please enter a valid email address.";
        } else if (!this.validate(this.value, this)) {} //everything is handled in the function
        else {
            this.valid = true;
          }
        if (was_valid != this.valid) {
          this.form.form_tag.update();
        }
        this.form.form_tag.onChange(e);
        //#! if (!this.data_error) { this.opts.ur_form.keyUp(this) }
        //#! if (!this.data_error && e.type == "blur") { this._validate(this.value,this); }
      }
    }, {
      key: "onFocus",
      value: function onFocus(e) {
        // activate and show error for last field (if not first)
        this.activated = true;
        var last = this.form.field_list[this._field_index - 1];
        if (last) {
          last.show_error = true;
        }
        this.form.form_tag.update();
      }
    }, {
      key: "onBlur",
      value: function onBlur(e) {
        // deactivate, force reevaluation, show errors
        uR.onBlur(this);
        this.activated = false;
        this.last_value = undefined; // trigger re-evaluation
        this.onChange(e);
        this.form.form_tag.update();
      }
    }, {
      key: "onChange",
      value: function onChange(e) {
        if (this.form.active) {
          this.show_error = true;
        }
        this.form.onChange && this.form.onChange(e, this);
        this.onKeyUp(e);
      }
    }, {
      key: "reset",
      value: function reset() {
        this.show_error = false;
        this.value = this.initial_value || "";
        var target;
        if (this.field_tag && this.input_tagname) {
          target = this.field_tag.root.querySelector(this.input_tagname);
          target.value = this.value;
        }
        this.onKeyUp({ target: target });
        this.activated = this.value != "";
        this.field_tag.update();
      }
    }]);

    return URInput;
  }();
  uR.form.fields = {
    'ur-input': uR.form.URInput
  };
})();

riot.tag2('image-input', '<img if="{initial_value}" riot-src="{initial_value}"> <input type="file" name="{name}" onchange="{onChange}">', '', '', function (opts) {
  this.on("mount", function () {
    this.name = this.opts.parent._name;
    this.update();
  });
  this.onChange = function (e) {
    var files = e.target.files;
    this.opts.parent.onChange(e);
  }.bind(this);
});

riot.tag2('ur-input', '', '', '', function (opts) {

  var self = this;

  this.on("mount", function () {
    this._input = document.createElement(this.field.input_tagname);
    if (this.field.input_tagname != "textarea") {
      this._input.type = this.field.input_type;
    }
    this._input.name = this.field.name;
    this._input.id = this.field.id;
    this._input.addEventListener("change", this.field.onChange.bind(this.field));
    this._input.addEventListener("focus", this.field.onFocus.bind(this.field));
    this._input.addEventListener("blur", this.field.onBlur.bind(this.field));
    this._input.addEventListener("keyup", this.field.onKeyUp.bind(this.field));
    this._input.classList.add(uR.theme.input);
    if (this.field.input_type == "header") {
      this._input.style.display = "none";
      this.field.required = false;
    }
    if (this.input_type == "hidden") {
      this.root.style.display = "none";
      this.label = "";
    }
    this.root.appendChild(this._input);

    var i_tries = 0;
    var interval = setTimeout(function () {
      var e = document.querySelector("#" + self.id);
      i_tries += 1;
      if (e && (i_tries++ > 5 || e.value)) {
        clearInterval(interval);
        self.onKeyUp({ target: e });
      }
    }, 1000);
    this.field.onMount && setTimeout(this.field.onMount.bind(this.field), 0);
    if (this.extra_attrs) {
      for (k in this.extra_attrs) {
        this.root.querySelector("input").setAttribute(k, this.extra_attrs[k]);
      }
    }
    this.update();
  });
});

riot.tag2('ur-form', '<div class="{theme.outer}"> <div class="{theme.header}" if="{form_title}"><h3>{form_title}</div> <div class="{theme.content}"> <div class="rendered_content"></div> <form autocomplete="off" onsubmit="{submit}" name="form_element" class="{opts.form_class}" method="{opts.method}"> <yield from="pre-form"></yield> <div each="{form.field_list}" class="{className} {empty: empty, invalid: !valid && show_error, active: activated || !empty} ur-input" data-field_id="{id}"> <div class="help_click" if="{help_click}" onclick="{help_click.click}" title="{help_click.title}">?</div> <label for="{id}" if="{label}" class="{required: required}" onclick="{labelClick}" data-success="{data_success}">{label}</label> <div class="{uR.theme.error_class}">{data_error}</div> <div class="help_text" if="{help_text}"><i class="fa fa-question-circle-o"></i> {help_text}</div> </div> <div if="{non_field_error}" class="non_field_error" data-field_id="non_field_error"> <div class="{uR.theme.error_class}">{non_field_error}</div> <p if="{uR.config.support_email}" style="text-align: center;"> If you need assistance contact <a href="mailto:{uR.config.support_email}">{uR.config.support_email}</a> </p> </div> <div class="button_div"> <yield from="button_div"></yield> <button class="{btn_success} {disabled: !valid}" id="submit_button" onclick="{submit}"> {success_text}</button> <button class="{btn_cancel}" if="{opts.cancel_function}" onclick="{opts.cancel_function}"> {cancel_text}</button> </div> <ul class="messagelist" if="{messages.length}"> <li class="{level}" each="{messages}">{body}</li> </ul> </form> <ur-pagination></ur-pagination> </div> </div>', '', '', function (opts) {

  var self = this;
  this.btn_success = this.opts.btn_success || uR.config.btn_success;
  this.btn_cancel = this.opts.btn_cancel || uR.config.btn_cancel;
  this.cancel_text = this.opts.cancel_text || uR.config.cancel_text;
  this.success_text = this.opts.success_text || "Submit";
  this.onChange = this.opts.onChange;
  this.suffix = this.opts.suffix || "";

  this.submit = function (e, _super) {
    if (this._ajax_busy || !this.form.field_list.length) {
      return;
    }
    if (!this.valid) {
      uR.forEach(this.form.field_list, function (field) {
        field.show_error = true;
      });
      this.update();
      return;
    }

    this.non_field_error = undefined;
    var alt_submit = this.opts.submit || this.parent && this.parent.submit;
    if (!_super && alt_submit) {
      if (alt_submit == "noop") {
        var form = this.root.querySelector("form");
        if (form.method == "POST" && document.querySelector("[name=csrfmiddlewaretoken]")) {
          var e = document.createElement('input');
          e.type = "hidden";
          e.name = "csrfmiddlewaretoken";
          e.value = document.querySelector("[name=csrfmiddlewaretoken]").value;
          form.appendChild(e);
        }
        form.submit();
      } else {
        alt_submit(this);
      }
    } else {
      uR.ajax({
        url: this.form.action,
        method: this.opts.method,
        data: this.getData(),
        success: this.ajax_success,
        success_attribute: this.opts.success_attribute,
        error: this.ajax_error,
        tag: self
      });
    }
  }.bind(this);

  this.clear = function () {
    this.initial = this.empty_initial;
    uR.storage.set(this.form.action, null);
    uR.forEach(this.form.field_list, function (field) {
      field.initial_value = self.initial[field.name];
      field.child && field.child.clear && field.child.clear();
      field.reset();
    });
    this.messages = [];
    self.active = false;
    setTimeout(function () {
      var f = self.root.querySelector("input:not([type=hidden]),select,textarea");f && f.focus();
    }, 0);
  }.bind(this);

  this.getData = function () {
    var data = {};
    uR.forEach(this.form.field_list, function (f) {
      data[f.name] = f.value || "";
    });
    return data;
  }.bind(this);

  this.on("mount", function () {
    var _parent = this.parent || {};
    _parent.ur_form = this;
    _parent.opts = _parent.opts || {};
    this.ajax_success = this.opts.ajax_success || _parent.opts.ajax_success || _parent.ajax_success || function () {};
    if (this.opts.success_redirect) {

      this._ajax_success = this.ajax_success;
      this.ajax_success = function () {
        self._ajax_success();window.location = this.opts.success_redirect;
      };
    }
    this.ajax_error = this.opts.ajax_error || _parent.opts.ajax_error || _parent.ajax_error || function () {};
    this.ajax_target = this.opts.ajax_target || this.submit_button;
    this.form = new uR.form.URForm(this);
    this.update();
    this.update();
    this.root.style.opacity = 1;
    if (this.opts.autosubmit) {
      this.root.querySelector("#submit_button").style.display = "none";
      this.opts.autosubmit == "first" && this.onChange({}, true);
    }
  });

  this.onChange = function (e, force) {
    if (this._ajax_busy) {
      return;
    }
    if (!this.opts.autosubmit) {
      return;
    }
    var changed;
    uR.forEach(this.form.field_list || [], function (field) {
      changed = changed || field.changed;
      field.changed = false;
    });
    if (changed || force) {
      this.update();
      this.submit();
    }
  }.bind(this);

  this.on("update", function () {
    if (this.root.querySelectorAll(".ur-input").length == 0) {
      return;
    }
    this.form.renderFields();
    if (this._multipart) {
      this.form_element.enctype = 'multipart/form-data';
    }
    this.valid = true;
    if (!this.form.field_list) {
      return;
    }
    uR.forEach(this.form.field_list, function (field, i) {
      if (field.html_error) {
        var error_element = this.root.querySelector("[data-field_id=" + field.id + "] .error");
        if (field.id && error_element) {
          error_element.innerHTML = field.html_error;
        }
      }
      if (field.no_validation) {
        return;
      }
      self.valid = self.valid && field.valid;
    }.bind(this));
    if (self.non_field_error && self.non_field_html_error) {
      setTimeout(function () {
        if (self.root.querySelector("[data-field_id=non_field_error]")) {
          self.root.querySelector("[data-field_id=non_field_error]").innerHTML = self.non_field_error;
        }
      }, 0);
    }
    this.opts.autosave && this.autoSave();
    if (this.rendered_content) {

      this.root.querySelector(".rendered_content").innerHTML = this.rendered_content;
      this.rendered_content = undefined;
    }
  });

  this.autoSave = uR.dedribble(function () {

    var new_data = this.getData();

    uR.storage.set(this.form.action, new_data);
  }.bind(this), 1000);
});

riot.tag2('ur-formset', '<ur-form each="{form,i in forms}" suffix="{⁗_⁗+i}" success_text="Add"> <div class="message font-20" if="{next}"> <b>{name}</b> has been successfully added!<br> Add more children or click <b>Next</b> to continue. </div> </ur-form> <button class="{uR.config.btn_primary}" disabled="{!valid}">Next</button>', '', '', function (opts) {
  var self = this;
  this.forms = [];
  this.on("mount", function () {
    this.forms.push({ schema: this.opts.schema });
    this.update();
  });
  this.submit = function (element) {
    var form_data = {};
    for (var key in element.inputs) {
      form_data[key] = element.inputs[key].value;
    }
    uR.ajax({
      method: "POST",
      url: this.form.action,
      data: form_data,
      target: element.root,
      self: element,
      loading_attribute: "mask",
      success: function success(data) {
        element.name = form_data.name;self.update();
      }
    });
  }.bind(this);
});

(function () {
  uR.config.input_overrides.checkbox = uR.config.input_overrides["checkbox-input"] = "checkbox-input";
  uR.config.input_overrides.radio = uR.config.input_overrides["radio-input"] = "checkbox-input";
  uR.form.fields['checkbox-input'] = function (_uR$form$URInput) {
    _inherits(CheckboxInput, _uR$form$URInput);

    function CheckboxInput(form, options) {
      _classCallCheck(this, CheckboxInput);

      var _this = _possibleConstructorReturn(this, (CheckboxInput.__proto__ || Object.getPrototypeOf(CheckboxInput)).call(this, form, options));

      if (_this.type == "checkbox-input") {
        _this.type = "checkbox";
      }
      _this.initial = _this.initial_value;
      if (typeof _this.initial == "string") {
        _this.initial = _this.initial.split(",");
      }
      _this.last_value = _this.initial;
      if (!(_this.choices && _this.choices.length)) {
        _this.choices = [{
          label: _this.label,
          id: _this.id + "__" + 0,
          value: "true"
        }];
        _this.field_tag.root.classList.add("no-label");
      }
      return _this;
    }

    _createClass(CheckboxInput, [{
      key: "reset",
      value: function reset() {
        this.show_error = false;
        this.value = this.initial || [];
        var target;
        uR.forEach(this.value, function (slug) {
          var cb = this.field_tag.root.querySelector("[value=" + slug + "]");
          if (cb) {
            cb.checked = true;target = cb;
          }
        }.bind(this));
        this.onKeyUp({ target: target });
        this.field_tag.update();
      }
    }, {
      key: "onKeyUp",
      value: function onKeyUp(e) {
        this.changed = false;
        this.valid = true;
        this.value = [];
        this.last_value = this.last_value || [];
        uR.forEach(this.field_tag.root.querySelectorAll("[name=" + this.name + "]"), function (input) {
          this.changed = this.changed || this.last_value.indexOf(input.value) != -1 !== input.checked;
          if (input.checked) {
            this.value.push(input.value);
          }
        }.bind(this));
        if (this.required && !this.value.length) {
          this.data_error = "This field is required.";
          this.valid = this.value.length;
        }
        this.show_error = true;
        this.last_value = this.value;
        this.form.form_tag.update();
        this.form.form_tag.onChange();
      }
    }]);

    return CheckboxInput;
  }(uR.form.URInput);
})();

riot.tag2('checkbox-input', '<div each="{field.choices}" class="choice"> <input type="{parent.field.type}" id="{id}" riot-value="{value}" onchange="{onKeyUp}" onblur="{onKeyUp}" name="{parent.field.name}"> <label for="{id}">{label}</label> </div>', '', '', function (opts) {

  var self = this;
  this.onKeyUp = function (e) {
    this.field.onKeyUp(e);
  }.bind(this);
});

(function () {
  uR.config.input_overrides.select = uR.config.input_overrides["select-input"] = "select-input";
  uR.form.fields['select-input'] = function (_uR$form$URInput2) {
    _inherits(SelectInput, _uR$form$URInput2);

    function SelectInput(form, options) {
      _classCallCheck(this, SelectInput);

      options.input_tagname = "select";
      return _possibleConstructorReturn(this, (SelectInput.__proto__ || Object.getPrototypeOf(SelectInput)).call(this, form, options));
    }

    return SelectInput;
  }(uR.form.URInput);
})();

riot.tag2('select-input', '<select id="{field.id}" onchange="{onChange}" onblur="{onBlur}" class="browser-default" name="{field.name}"> <option each="{field.choices}" riot-value="{value}">{label}</option> </select>', '', '', function (opts) {

  this.onBlur = function (e) {
    this.field.onBlur(e);
  }.bind(this);
  this.onChange = function (e) {
    this.field.onChange(e);
  }.bind(this);

  this.on("mount", function () {
    this.update();
  });
});

riot.tag2('ur-pagination', '<div class="flex-row" each="{uR.pagination.results}"> <div class="col1"> <a href="{url}" class="fa fa-link" if="{url}"></a> <a href="{ur_admin}" class="{uR.icon.admin}" if="{ur_admin}"></a> </div> <div class="col4" each="{field in fields}">{field}</div> </div>', '', '', function (opts) {

  this.on("update", function () {
    uR.pagination && uR.forEach(uR.pagination.results, function (result) {
      result.ur_admin = uR.config.form_prefix.replace("^#?", "") + "/" + uR.form.current_form + "/" + result.id + "/";
    });
  });
});

uR.mount_tabs = true;
uR.ready(function () {
  if (uR._mount_tabs) {
    riot.mount("ur-tabs");
  }
});
riot.tag2('ur-tabs', '<div class="tab-wrapper"> <div class="tab-anchors"> <a onclick="{showTab}" each="{tab,i in tabs}" title="{tab.title}" class="{active: i == this.active}"> {tab.title}</a> </div> <yield></yield> </div>', '', '', function (opts) {

  this.showTab = function (e) {
    this.active = e.item.i;
  }.bind(this);

  this.on("mount", function () {

    this.tabs = this.tags['ur-tab'] || [];
    if (!Array.isArray(this.tabs)) {
      this.tabs = [this.tabs];
    }
    uR.forEach(this.opts.tabs || [], function (tab) {
      var e = document.createElement('ur-tab');
      this.root.querySelector(".tab-wrapper").appendChild(e);
      tab.parent = this;
      this.tabs.push(riot.mount(e, tab)[0]);
    }.bind(this));
    uR.forEach(this.tabs, function (tab, i) {
      tab.index = i;
    });
    this.active = 0;
    if (uR.config.default_tabs) {
      this.root.classList.add("default");
    }
    this.update();
  });
});

riot.tag2('ur-tab', '<yield></yield>', '', '', function (opts) {

  this.title = this.opts.title || this.title;

  this.show = function () {
    this.root.classList.remove("hidden");
    if (this.opts.href && !this.loaded) {
      return this.ajax({
        url: this.opts.href,
        success: function success(data, response) {
          this.root.innerHTML = data.content || response.response;this.loaded = true;
        }
      });
    }
    this.opts.click && this.opts.click();
  }.bind(this);

  this.hide = function () {
    this.root.classList.add("hidden");
  }.bind(this);

  this.on("mount", function () {
    this._parent = this.parent || this.opts.parent;
    if (this.opts.innerHTML) {
      this.root.innerHTML = this.opts.innerHTML;
    }
  });

  this.on("update", function () {
    if (!this.parent || this._parent.active == undefined) {
      return;
    }
    (this._parent.active == this.index ? this.show : this.hide)();
  });
});

riot.tag2('markdown', '<yield></yield>', '', '', function (opts) {
  this.on("mount", function () {
    var content = this.content || this.opts.content || this.root.innerHTML;
    if (this.opts.url && !content) {
      uR.ajax({
        url: this.opts.url,
        success: function (data, request) {
          this.opts.content = request.responseText;
          this.mount();
        }.bind(this)
      });
      return;
    }
    this.root.innerHTML = markdown.toHTML(content.replace("&amp;", "&"));
  });
  this.setContent = function (content) {
    this.content = content;
    this.mount();
  }.bind(this);
});

uR.config.input_overrides['multi-file'] = uR.config.input_overrides["multi-file"] = "multi-file";
uR.config.tmp_file_url = "/media_files/private/";
uR.form.fields['multi-file'] = function (_uR$form$URInput3) {
  _inherits(MultiFileInput, _uR$form$URInput3);

  function MultiFileInput(form, options) {
    _classCallCheck(this, MultiFileInput);

    return _possibleConstructorReturn(this, (MultiFileInput.__proto__ || Object.getPrototypeOf(MultiFileInput)).call(this, form, options));
  }

  return MultiFileInput;
}(uR.form.URInput);

riot.tag2('multi-file', '<form action="{action}" method="POST" if="{can_upload}"> <label class="{uR.config.btn_primary}"> <input type="file" onchange="{validateAndUpload}" style="display:none;" name="file"> {upload_text} </label> </form> <div each="{files}" class="file {uR.config.alert_success}"> <div> <div class="name">{name}</div> <div class="content_type">{content_type}</div> </div> <div onclick="{parent.deleteFile}" class="fa fa-trash"></div> </div> <div if="{error_msg}" class="{uR.theme.error_class}">{error_msg}</div>', '', '', function (opts) {

  var self = this;
  this.validateAndUpload = function (e) {
    var form = this.root.querySelector("form");
    this.error_msg = undefined;
    this.ajax({
      form: form,
      success: function success(data) {
        this.files.push(data);
        uR.storage.set(this.action + "__files", this.files);
      },
      error: function error(data) {
        self.error_msg = "An unknown error has occurred.";
      }
    });
    this.root.querySelector("[type=file]").value = "";
  }.bind(this);
  this.clear = function () {
    this.value = "";
    this.files = [];
    uR.storage.set(this.action + "__files", undefined);
    this.update();
  }.bind(this);
  this.deleteFile = function (e) {
    uR.forEach(this.files, function (f, i) {
      if (f.id == e.item.id) {
        self.files.splice(i, 1);
      }
    });
    uR.storage.set(this.action + "__files", this.files);
  }.bind(this);
  this.on("mount", function () {
    this.max_files = this.field.max_files || Infinity;
    this.action = opts.action || uR.config.tmp_file_url;
    this.files = uR.storage.get(this.action + "__files") || [];
    this.update();
  });
  this.on("update", function () {
    if (this.files && this.files.length) {
      this.upload_text = opts.parent.upload_another_text || opts.parent.upload_text || "Upload another file";
      this.field.value = this.files.map(function (f) {
        return f.id;
      }).join(",");
    } else {
      this.upload_text = this.field.upload_text || 'Upload a file';
      this.value = "";
    }
    this.can_upload = !(this.files && this.files.length >= this.max_files);
  });
});

riot.tag2('ez-file', '<input type="file" id="{_id}" onchange="{cropIt}" name="{slug}" if="{can_edit}"> <yield> <label if="{!done}" for="{_id}" class="btn-danger btn">Add {name}</label> <button if="{done && !bg}" class="btn btn-success" onclick="{edIt}">{opts.success_text || ⁗Edit⁗}</button> <div if="{bg}" class="image" riot-style="background-image: url({bg})" onclick="{edIt}"></div> <button if="{done}" onclick="{clear}" class="{uR.config.btn_cancel} fa fa-trash"></button> </yield> <form action="{opts.url}" method="POST"> <input type="hidden" name="user_id" riot-value="{opts.user_id}"> <input type="hidden" name="blob"> </form>', 'ez-file { display: block; position: relative; } ez-file input[type=file], ez-file form { display: none; } ez-file .image { cursor: pointer; display: inline-block; width: 100%; } ez-file .image:before { content: ""; display: block; margin-top: 100%; } ez-file .fa-trash { bottom: 0; left: 0; position: absolute; }', '', function (opts) {

  var self = this;
  this.on("mount", function () {
    this.slug = (this.opts.name || "").replace(" ", "_").toLowerCase();
    this.name = this.opts.name || "File";
    this.done = this.opts.done;
    this.type = this.opts.type;
    this.can_edit = this.opts.can_edit || this.opts.can_edit == undefined;
    this.show_preview = !this.opts.no_preview;
    this._id = "file__" + this.slug + "__" + this.opts.user_id;
    this.update();
  });
  this.on("update", function () {
    if (this.done && this.show_preview) {
      this.bg = this.done;
    }
  });
  this.clear = function (e) {
    if (!e.target.innerHTML) {
      e.target.innerHTML = "?";
      setTimeout(function () {
        e.target.innerHTML = "";
      }, 2000);
      return;
    }
    this.uploadFile(e, { action: 'delete', user_id: opts.user_id });
  }.bind(this);
  this.cropIt = function (e) {
    var file = this.root.querySelector("[type=file]").files[0];

    var img = document.createElement("img");
    var reader = new FileReader();
    reader.onload = function (e) {
      if (this.opts.type == "img") {
        img.src = e.target.result;
      } else {
        this.root.querySelector("[name=blob]").value = e.target.result;
        this.uploadFile(e);
      }
    }.bind(this);
    reader.readAsDataURL(file);

    img.onload = function () {
      uR.alertElement("resize-image", { img: img, parent: self });
    };
  }.bind(this);
  this.edIt = function (e) {
    if (!this.can_edit) {
      return;
    }
    img = document.createElement("img");
    img.onload = function () {
      uR.alertElement("resize-image", { img: img, parent: self });
    };
    img.src = this.done;
  }.bind(this);
  this.uploadFile = function (e, data) {
    var form = this.root.querySelector("form");
    this.ajax({
      url: this.opts.url,
      method: "POST",
      data: data,
      form: form,
      success: function success(data) {
        this.done = data.done;
      },
      error: function error() {
        uR.alert("an unknown error has occurred. Go bug Chris!");
      }
    });
  }.bind(this);
});
riot.tag2('resize-image', '<div class="{theme.outer}"> <div class="{theme.content}"> <center> <canvas></canvas> <div class="burtons"> <button onclick="{doZoom}" class="{uR.config.btn_primary}"> {zoom}x <i class="fa fa-search-plus"></i></button> <button onclick="{doRotate}" class="{uR.config.btn_primary}"><i class="fa fa-rotate-right"></i></button> <label for="{opts.parent._id}" class="{uR.config.btn_success}"><i class="fa fa-camera"></i></label> </div> <button onclick="{done}" class="{uR.config.btn_success}">Save</button> <button onclick="{cancel}" class="{uR.config.btn_cancel}">Cancel</button> </center> </div> </div>', 'resize-image .btn { font-size: 1.5em; margin: 0 5px; } resize-image .burtons .btn { margin-bottom: 10px; }', '', function (opts) {

  this.on("mount", function () {
    this.canvas = this.root.querySelector("canvas");
    this.ctx = this.canvas.getContext("2d");
    this.img = this.opts.img;
    this.ratio = this.img.width / this.img.height;
    var max_width = this.canvas.parentElement.clientWidth;
    this.canvas.width = max_width;
    this.canvas.height = max_width / this.ratio;
    this.zoom = 1;
    this.rotate = 0;
    this.file = this.opts.parent.root.querySelector("[type=file]");
    this.blob = this.opts.parent.root.querySelector("[name=blob]");
    this.file.value = "";
    this.blob.value = "";
    this.update();
  });
  this.on("update", function () {
    if (!this.img) {
      return;
    }
    var canvas = this.canvas;
    var dx = (this.zoom - 1) * canvas.width;
    var dy = (this.zoom - 1) * canvas.height;
    this.ctx.clearRect(0, 0, canvas.width, canvas.height);
    this.ctx.drawImage(this.opts.img, -dx, -dy, canvas.width + 2 * dx, canvas.height + 2 * dy);

    var img = document.createElement('img');
    img.src = canvas.toDataURL("image/png");
    img.onload = function () {
      this.ctx.clearRect(0, 0, canvas.width, canvas.height);
      this.ctx.save();
      this.ctx.translate(canvas.width / 2, canvas.height / 2);
      this.ctx.rotate(this.rotate * Math.PI);
      this.ctx.drawImage(img, -canvas.width / 2, -canvas.height / 2);
      this.ctx.restore();
    }.bind(this);
  });
  this.cancel = function (e) {
    this.unmount();
  }.bind(this);
  this.doZoom = function (e) {
    this.zoom += 0.5;
    if (this.zoom > 3) {
      this.zoom = 1;
    }
  }.bind(this);
  this.doRotate = function (e) {
    this.rotate += 0.5;
  }.bind(this);
  this.done = function (e) {
    this.blob.value = this.canvas.toDataURL();
    this.opts.parent.uploadFile();
    this.unmount();
  }.bind(this);
});

uR.ready(function () {
  riot.mount("ur-nav");
});

riot.tag2('ur-nav', '<nav> <div class="nav-wrapper"> <a href="/about/" class="brand-logo" style="height: 100%;"> <img riot-src="{uR.config.logo || \'logo.png\'}" style="height: 100%"> </a> <ul id="nav-mobile" class="right hide-on-med-and-down"> <yield></yield> <auth-dropdown></auth-dropdown> </ul> </div> </nav>', '', '', function (opts) {});
//# sourceMappingURL=unrest-built.js.map
