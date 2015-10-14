<tool-checkout>
  <div each={ window.TXRX.criteria }>
    <a href="#criterion/{ id }" class="btn btn-block btn-success">{ name }</a>
  </div>

</tool-checkout>

<badge>
  <div class="row">
    <div class="col-sm-4">
      <div class="badge-box">
        <div class="row">
          <div each={ columns } class="col-sm-6">
            <div each={ rows } style="background-color: {this.color}" class="{ group: true, any: any }">
              <a onclick={ parent.parent.loadPermission } each={ permissions }
                 class="{ permission: true, has: has, has_not: !has }">
                { abbreviation }
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="col-sm-8">
      <permission></permission>
    </div>
  </div>

  var that = this;
  this.on("mount",function() {
    that.columns = [{'rows':[]},{'rows':[]}]
    window.TXRX.permissions.forEach(function(p) {
      p.has = (window.TXRX.user.permission_ids.indexOf(p.id) > -1);
    });
    window.TXRX.groups.forEach(function(g) {
      that.columns[g.column].rows.push(g);
      g.permissions = window.TXRX.permissions.filter(function(p) {
        if (p.group_id == g.id) {
          if (p.has) { g.any = true }
          return true
        }
      });
    });
    this.update();
  });
  loadPermission(e) {
    riot.mount("permission",e.item);
  }

</badge>

<permission>
  <h1>{ opts.name }</h1>
  <div each={ opts.criteria_json }>
    <h2>{ name }</h2>
    <div each={ courses }>{ name }</div>
  </div>
  
</permission>

<search-criterion>
  <h2>Manage Tool Permission</h2>
  <p>Search for students and grant/remove their privileges for { opts.name }.</p>
  <input type="text" name="q" onkeyup={ search } placeholder="Search by name or email" autocomplete="off" />
  <div if={ students.length; }>
    <div each={ students }>
      <button class="btn btn-primary btn-success btn-block" onclick={ parent.expand }>
        <div class="row">
          <div class="col-sm-4">{ username }<br />{ get_full_name }&nbsp;</div>
          <div class="col-sm-8">{ email }<br/>{ paypal_email }
          </div>
        </div>
      </button>
      <checkbox each={ criteria } onclick={ parent.parent.toggleCriterion }>
        { name }
      </checkbox>
    </div>
  </div>

  var that = this;
  that.students = [];
  var old_value = '',value;
  search(e) {
    value = document.querySelector("search-criterion [name=q]").value;
    if (old_value == value) { return }
    uR.bounce(s,[e]);
    old_value = value;
  }
  function s(e) {
    that.loading = true;
    if (!value) { that.students = []; that.loading = false; return; }
    $.get(
      "/api/user/search/",
      {q: value},
      function(data) {
        that.loading = false;
        that.students = data;
        that.update()
      },
      "json"
    )
  }
  this.on("mount",function() { $("search-criterion [name=q]").focus(); });
  this.on("update", function() {
    if (this.active_user) {
      this.active_user.criteria.forEach(function(c) {
        c.has = that.active_user.criterion_ids.indexOf(c.id) != -1;
      });
    }
  });

  expand(e) {
    if (e.item.criteria) { e.item.criteria = this.active_user = null; return }
    if (this.active_user) { this.active_user.criteria = null }
    this.active_user = e.item;
    e.item.criteria = window.TXRX.criteria;
  }

  toggleCriterion(e) {
    $.get(
      '/tools/toggle_criterion/',
      { user_id: this.active_user.id, criterion_id: e.item.id },
      function(data) {
        that.active_user.criterion_ids = data;
        that.update();
      },
      "json"
    );
  }
</search-criterion>

<checkbox>
  <a class="alert alert-block alert-{ alert_class }">
    <i class="fa fa-{ 'check-': has }square-o fa-3x"></i>
    <yield/>
  </a>

  this.on("update",function() {
    this.alert_class = this.has?"success":"danger";
  });

</checkbox>
