<login>
  <form name="form" onsubmit={ submit }>
    <input-field each={ fields }></input-field>

    <div class="submit-row">
      <input type="submit" value="Log in" class="btn btn-info" />
      <a href="/auth/password_reset/" class="pull-right">Forgotten username/password?</a>
      <div class="alert alert-danger error" if={ non_field_errors }>{ non_field_errors }</div>
    </div>
  </form>

  var that = this;

  function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
  }

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

  submit(e) {
    form.setAttribute("loading","loading");
    $.ajax({
      url: "/api-token-auth/",
      type: "POST",
      data: serialize(form),
      success: function(data) {
        that.fields.forEach(function(item,i) { item.error = ''; });
        that.non_field_errors = '';
        var next = getParameterByName("next");
        JWT.updateToken(data);
        this.parent.opts.success;
      },
      error: function(jqxhr) {
        var errors = JSON.parse(jqxhr.responseText);
        console.log(errors)
        that.fields.forEach(function(el,i) { el.error = errors[el.name]; });
        that.non_field_errors = errors.non_field_errors;
        that.update()
      },
    });
  }
  
  this.fields = [
    { name: "username", type: "text", labelclass: "control-label", label: "Username: ", required: true },
    { name: "password", type: "password", labelclass: "control-label", label: "Password: ", required: true }
  ]
  //this.fields[0].focus = true;
</login>

