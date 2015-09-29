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
  
  submit(e) {
    uR.ajax({
      url: "/api-token-auth/",
      type: "POST",
      data: uR.serialize(form),
      success: function(data) { JWT.updateToken(data); that.parent.success() },
    });
  }
  
  this.fields = [
    { name: "username", type: "text", labelclass: "control-label", label: "Username: ", required: true },
    { name: "password", type: "password", labelclass: "control-label", label: "Password: ", required: true }
  ]
  //this.fields[0].focus = true;
</login>

<password-change>
  <form onsubmit={ submit }>
    <div if={ !password_changed }>
      <input-field each={ fields } if></input-field>
      <div class="submit-row">
        <input type="submit" value="Change Password" class="btn btn-info" />
        <div class="alert alert-danger error" if={ non_field_errors }>{ non_field_errors }</div>
        <div style="margin-top: 5px;"><a href="/auth/password_reset/">Forgotten username/password?</a></div>
      </div>
    </div>
    <div if={ password_changed } class="alert alert-success">
      Your password has been changed successfully.
      <button class="btn btn-danger btn-block">Close</div>
    </div>
  </form>

  submit(e) {
    uR.ajax({
      url: "/api-token-auth/",
      type: "POST",
      data: uR.serialize(form),
      success: function(data) {
        that.parent.success();
        that.password_changed = true;
      },
    });
  }
  

  this.fields = [
    {name: "old_password", type: "text", labelclass: "control-label", label: "Old Password: ", require: true},
    {name: "password", type: "text", labelclass: "control-label", label: "New Password: ", require: true},
    {name: "password2", type: "text", labelclass: "control-label", label: "Confirm Password: ", require: true},
  ]

</password-change>
