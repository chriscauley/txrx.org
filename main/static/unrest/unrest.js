var uR = (function() {
  var uR = window.uR || {};
  uR.timeIt = function(f,name) {
    name = name || f.name
    return function() {
      var start = new Date();
      f.apply(this,arguments);
      console.log(name,"took",(new Date() - start)/1000);
    }
  }
  uR.Ready = function Ready(isReady,_ready) {
    isReady = isReady || function () { return false };
    _ready = _ready || [];
    function log() {
      //console.log.apply(this,arguments);
    }
    function error() {
      //console.error.apply(this,arguments);
    }
    var ready = function ready() {
      uR.forEach(arguments || [],function(f) {
        window.airbrake && f.name && window.airbrake.log("ready: " + f.name);
        if (typeof f == "function") { _ready.push(f); log('in queue',f.name); }
        else { log(f); }
      });
      var in_queue = _ready.length;
      while (isReady() && _ready.length) {
        log("doing it!");
        _ready.shift()();
      }
      error("Ready",in_queue,_ready.length);
    }
    ready._name = isReady.name;
    ready.start = function() {
      window.airbrake && window.airbrake.log("unrest starting");
      isReady = function() { return true };
      ready();
    }
    return ready;
  }

  uR.escapeHTML = function escapeHTML(s) { // taken from under-construction/lib/diff.js
    return s && s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }
  uR.serialize = function serialize(form) {
    var field, s = [];
    if (typeof form != 'object' && form.nodeName != "FORM") { return }
    var len = form.elements.length;
    for (var i=0; i<len; i++) {
      field = form.elements[i];
      if (!field.name || field.disabled || field.type == 'file' || field.type == 'reset' ||
          field.type == 'submit' || field.type == 'button') { continue }
      if (field.type == 'select-multiple') {
        for (j=form.elements[i].options.length-1; j>=0; j--) {
          if(field.options[j].selected)
            s[s.length] = encodeURIComponent(field.name) + "=" + encodeURIComponent(field.options[j].value);
        }
      } else if ((field.type != 'checkbox' && field.type != 'radio') || field.checked) {
        s[s.length] = encodeURIComponent(field.name) + "=" + encodeURIComponent(field.value);
      }
    }
    return s.join('&').replace(/%20/g, '+');
  }
  uR.getQueryParameter = function getQueryParameter(name,search) {
    var regexp = new RegExp("[\?&](?:"   +name+")=([^&]+)");
    var _sd = (search || window.location.search).match(regexp);
    if (_sd) { return unescape(_sd[1]); }
  }

  uR.getQueryDict = function(str) {
    str = str || window.location.search;
    var obj = {};
    str.replace(/([^=&?]+)=([^&]*)/g, function(m, key, value) {
      obj[decodeURIComponent(key)] = decodeURIComponent(value);
    });
    return obj
  }

  uR.cookie = {
    set: function (name,value,days) {
      var expires = "";
      if (days) {
        var date = new Date();
        date.setTime(date.getTime()+(days*24*60*60*1000));
        expires = "; expires="+date.toGMTString();
      }
      document.cookie = name+"="+value+expires+"; path=/";
    },
    get: function(name) {
      var nameEQ = name + "=";
      var ca = document.cookie.split(';');
      for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
      }
      return null;
    },
    delete: function (name) { this.set(name,"",-1); }
  }

  function isEmpty(obj) {
    for (var key in obj) { return false; }
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
    var target = opts.target || opts.form;  // default to body?
    var url = opts.url || form.action || '.';
    window.airbrake && window.airbrake.log("AJAX: "+url);
    var that = opts.that;
    if (that) {
      console.warn('"that" has been depracated in favor of "tag".');
    }
    var tag = that || opts.tag;
    var loading_attribute = opts.loading_attribute || (tag && tag.loading_attribute) || uR.config.loading_attribute;
    var success_attribute = opts.success_attribute || "";
    var success_reset = opts.success_reset || false;
    var success = (opts.success || function(data,request) {}).bind(tag);
    var error = (opts.error || function(data,request) {}).bind(tag);
    var filenames = opts.filenames || {};
    if (tag) {
      tag.messages = opts.messages || [];
      tag._ajax_busy = true;
      tag.form_error = undefined;
      if (!target && tag.target) { console.warn("Use of tag.target is depracated in favor of tag.ajax_target") }
      target = target || tag.target || tag.ajax_target;
      if (typeof target == "string") { target = tag.root.querySelector(target) || document.querySelector(target); }
    }

    // mark as loading
    if (target) {
      target.removeAttribute("data-success");
      target.setAttribute("data-loading",loading_attribute);
    }

    // create form_data from data or form
    if (!data && opts.form) {
      data = {};
      uR.forEach(opts.form.elements,function(element) {
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
    if (method=="POST" && data) {
      for (var key in data) {
        filenames[key]?form_data.append(key,data[key],filenames[key]):form_data.append(key,data[key]);
      };
    }
    if (method != "POST") {
      url += (url.indexOf("?") == -1)?"?":"&";
      for (key in data) { url += key + "=" + encodeURIComponent(data[key]) + "&" }
    }

    // create and send XHR
    var request = new XMLHttpRequest();
    request.open(method, url , true);
    var headers = uR.defaults(opts.headers || {}, {
      "X-Requested-With": "XMLHttpRequest",
    })
    for (var key in headers) { request.setRequestHeader(key,headers[key]); }

    if ("POSTDELETE".indexOf(method) != -1 && uR.cookie.get("csrftoken")) {
      request.setRequestHeader("X-CSRFToken",uR.cookie.get("csrftoken"));
    }
    request.onload = function(){
      try { var data = JSON.parse(request.response); }
      catch (e) {
          var data = {};
      }
      if (data.status == 401) {
        return uR.auth.loginRequired(function() { uR.ajax(opts); })();
      }
      if (target) { target.removeAttribute('data-loading'); }
      var errors = data.errors || {};
      if (data.error) { errors = { non_field_error: data.error }; }
      var non_field_error = errors.non_field_error || errors.__all__; // __all__ is django default syntax
      if (isEmpty(errors) && request.status != 200) {
        non_field_error = opts.default_error || "An unknown error has occurred";
      }
      if (tag && tag.form && tag.form.field_list) {
        uR.forEach(tag.form.field_list,function(field,i) {
          field.data_error = errors[field.name];
          if (field.data_error && data.html_errors && ~data.html_errors.indexOf(field.name)) {
            field.html_error = field.data_error
          }
          field.valid = !field.data_error;
          field.show_error = true;
        });
      }
      if (non_field_error) {
        // if there's no form and no error function in opts, alert as a fallback
        if (tag) {
          tag.non_field_error = non_field_error;
          if (data.html_errors && ~data.html_errors.indexOf("non_field_error")) { tag.non_field_html_error = true; }
        } else if (!opts.error) { uR.alert(non_field_error); }
      }
      var complete = (request.status == 200 && isEmpty(errors));
      (complete?success:error)(data,request);
      uR.pagination = data.ur_pagination || uR.pagination;
      if (target && complete && !data.messages) { target.setAttribute("data-success",success_attribute) }
      if (tag) {
        tag._ajax_busy = false;
        tag.messages = data.messages || [];
        tag.update();
      }
      uR.postAjax && uR.postAjax.bind(request)(request);
      if (data.ur_route_to) { uR.route(data.ur_route_to); }
    };
    request.send((headers['Content-Type'] == 'application/json')?JSON.stringify(data):form_data);
  }

  var AjaxMixin = {
    init: function() {
      this.ajax = function(options,e) {
        e = e || {};
        options.tag = options.tag || this;
        options.target = options.target || this.ajax_target || (this.theme && this.root.querySelector(this.theme.outer));
        options.target = options.target || e.target;
        options.success = options.success || this.ajax_success || uR.default_ajax_success;
        options.url = options.url || this.ajax_url;
        uR.ajax(options);
      };
    },
  };
  window.riot && riot.mixin(AjaxMixin);
  uR.default_ajax_success = function(data,request) {
    uR.extend(uR.data,data);
  }

  uR.debounce = function debounce(func, wait, immediate) {
    var timeout, wait = wait || 200;
    return function() {
      var context = this, args = arguments;
      var later = function() {
        timeout = null;
        if (!immediate) func.apply(context, args);
      };
      var callNow = immediate && !timeout;
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
      if (callNow) func.apply(context, args);
      return true;
    };
  }

  uR.dedribble = function dedribble(func, wait, end_bounce) {
    var timeout, wait = wait || uR.config.dribble_time || 200, end_bounce = (end_bounce !== undefined) && true ;
    var last = new Date();
    return function() {
      var context = this, args = arguments;
      if (end_bounce) {
        var later = function() {
          timeout = null;
          func.apply(context, args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
      }
      if (new Date() - last > wait) { func.apply(context, args); last = new Date(); }
    };
  };

  // this function may someday be replaced with rambdas map
  uR.forEach = function forEach(array,func,context) {
    if (context) { func = func.bind(context) }
    for (var i=0;i<array.length;i++) { func(array[i],i,array); }
  }

  // this function may someday be replaced with rambdas merge
  uR.extend = function(a,b) {
    for (var i in b) {
      if (b.hasOwnProperty(i)) { a[i] = b[i]; }
    }
  }

  uR.FALSE = "false";
  uR.REQUIRED = new Object();
  uR.DEFAULT_TRUE = new Object();
  uR.NotImplemented = (s) => "NotImplementedError: "+s;
  uR.depracated = function(f,old,alt) {
    return function() {
      console.warn(old,"is depracated in favor of",alt);
      return f.apply(this,arguments)
    }
  }
  uR.defaults = function(a,b) {
    // like extend but keeps the values of a instead of replacing them
    for (var i in b) {
      if (b.hasOwnProperty(i) && !a.hasOwnProperty(i)) { a[i] = b[i]; }
      if (a[i] == uR.REQUIRED) { throw "Attribute "+i+" is required on "+a; }
      if (a[i] == uR.DEFAULT_TRUE) { a[i] = true }
    }
    return a;
  }

  // uR.ready is a function for handling window.onload
  uR.ready = new uR.Ready(undefined,uR._ready);
  window.onload = function() {
    uR.ready.start();
    uR.route && uR.route(window.location.href);
    // #! dummy route function. This is so everything can use uR.route without router.js
    uR.route = uR.route || function route(path,data) { window.location = path }
  }

  uR.getSchema = function getSchema(url,callback) {
    uR.ajax({
      url: url,
      success: function(data) {
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

  uR.onBlur = uR.onBlur || function() {};
  uR.config = uR.config || {};
  uR.config.doPostAuth = function() {}
  uR.config.form = {};
  uR.config[404] = 'four-oh-four';
  uR.config.form.field_class = "input-field";
  uR.config.loading_attribute = uR.config.loading_attribute || 'fade';
  uR.config.loading_attribute = 'fade';
  uR.config.tag_templates = [];
  uR.config.input_overrides = {
    boolean: function() { return { tagname: 'select-input', choices: [[uR.FALSE,"No"],["true","Yes"]] } },
  };
  uR.config.text_validators = {};
  uR.config.mount_to = "#content";
  uR.config.mount_alerts_to = "#alert-div";
  uR.config.cancel_text = "Cancel";
  uR.config.success_text = "Submit";
  uR._var = {};
  uR.data = uR.data || {};
  uR.alert = function(s) { console.log(s) };//alert(s); }; // placeholder for future alert function
  uR.schema = {fields: {},__initial: {}};
  uR.urls = {};
  uR.slugify = function(s) {
    if (typeof s != "string") { s = s.toString() }
    return s.toLowerCase().replace(/(^[\s-]+|[\s-]+$)/g,"").replace(/[^\d\w -]+/g,"").replace(/[\s-]+/g,"-");
  };
  uR.unslugify = function(s) {
    if (typeof s != "string") { s = s.toString() }
    return s.replace(/-_/," ").replace(/^(.)|\s(.)/g, ($1) => $1.toUpperCase())
  }
  uR.reverseCamelCase = function(s) {
    if (typeof s == "function") { s = s.name }
    if (typeof s != "string") { s = s.toString() }
    s = s.replace( /([A-Z])/g, " $1" )
    return s.charAt(0).toUpperCase() + s.slice(1);
  }

  uR.formatTimeRange = function formatTimeRange(start,end) {
    var start = moment(start), end = moment(end);
    var start_format = start.minute()?"h:mm":"h";
    var end_format = end.minute()?"h:mm A":"h A";
    if (start.hour() < 12 && end.hour() > 12) { start_format += " A"; }
    return start.format(start_format) + " - " + end.format(end_format);
  }
  return uR;
})();
