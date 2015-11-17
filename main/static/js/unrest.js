var uR = (function() {
  function serialize(form) {
    var field, s = [];
    if (typeof form != 'object' && form.nodeName != "FORM") { return }
    var len = form.elements.length;
    for (i=0; i<len; i++) {
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

  function ajax(opts) {
    opts.type = opts.type || "GET";
    opts.data = opts.data || {};
    opts.success = opts.success || function(data) {};
    opts.error = opts.error || function(jxqhr) {};
    that = opts.that;
    if (opts.form) { form.setAttribute("loading","loading"); }
    $.ajax({
      url: "/api-token-auth/",
      type: "POST",
      data: uR.serialize(form),
      success: function(data) {
        if (opts.form) {
          form.removeAttribute("loading");
          forEach(that.fields,function(item,i) { item.error = ''; });
          that.non_field_errors = '';
        }
        opts.success(data);
      },
      error: function(jqxhr) {
        if (opts.form) {
          form.removeAttribute("loading");
          var errors = JSON.parse(jqxhr.responseText);
          forEach(that.fields,function(el,i) { el.error = errors[el.name]; });
          that.non_field_errors = errors.non_field_errors;
        }
        opts.error(jqxhr);
        that.update()
      },
    });
  }

  function debounce(func, wait, immediate) {
    var timeout, wait = wait | 200;
    return function() {
      var context = this, args = arguments;
      var later = function() {
        timeout = null;
        if (!immediate) func.apply(context, args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
      if (immediate && !timeout) func.apply(context, args);
    };
  };

  function forEach(array,func) {
    for (var i=0;i<array.length;i++) { func(array[i],i,array); }
  }
  return {
    serialize: serialize,
    ajax: ajax,
    debounce: debounce,
    forEach: forEach,
  }
})()
  
