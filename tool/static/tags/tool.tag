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
    <h2><i class="fa fa-check fa-2x" if={ has }></i> { name }</h2>
    <div each={ courses } class="course">
      <i class="fa fa-check fa-2x" if={ has }></i>
      { name }
    </div>
  </div>
  this.course_ids = window.TXRX.user.completed_course_ids
  this.on("update",function() {
    if (this.opts.criteria_json) {
      this.opts.criteria_json.forEach(function(criteria) {
        criteria.has = window.TXRX.user.criterion_ids.indexOf(criteria.id) != -1;
        criteria.courses.forEach(function(course) {
          course.has = window.TXRX.user.completed_course_ids.indexOf(course.id) != -1;
          console.log(course)
        });
      });
    }
  });
</permission>

<toolmaster>
  <search-users search_term={ opts.search_term }>
    <h2>Manage Tool Permission</h2>
    <p>Search for students and grant/remove their privileges for { opts.name }.</p>
  </search-users>
  <div if={ active_user } class="row">
    <div class="col-sm-6">
      <h3><u>Course Enrollments</u></h3>
      <checkbox each={ student.enrollment_jsons } onclick={ parent.toggleEnrollment }>
        { session_name }
      </checkbox>
    </div>
    <div class="col-sm-6">
      <h3><u>Tool Criteria</u></h3>
      <checkbox each={ criteria } has={ id in parent.student.criterion_ids } cid={ id } pid={ parent.student.criterion_ids } onclick={ parent.toggleCriterion }>
        { name }
      </checkbox>
    </div>
  </div>

  var that = this;
  toggleCriterion(e) {
    $.get(
      '/tools/toggle_criterion/',
      { user_id: this.active_user.id, criterion_id: e.item.id },
      function(data) {
        that.student.criterion_ids = data;
        that.update();
      },
      "json"
    );
  }

  toggleEnrollment(e) {
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

  this.on("update", function() {
    that.criteria  = window.TXRX.criteria;
    if (that.active_user) {
      that.criteria.forEach(function(c) {
        c.has = that.student.criterion_ids.indexOf(c.id) != -1;
      });
    }
  });

  select(e) {
    var target = this.root;
    target.setAttribute("ur-loading","loading");
    this.active_user = e.item;
    $.get(
      "/api/user/student/"+e.item.id+"/",
      function(data) {
        target.removeAttribute("ur-loading");
        that.student = data;
        that.update()
      }
    )
  }
</toolmaster>

<search-users>
  <yeild/>
  <input type="text" name="q" onkeyup={ search } placeholder="Search by name or email" autocomplete="off"
         value={ opts.search_term } />
  <div class="results">
    <div each={ students }>
      <button class="btn btn-primary btn-success btn-block" onclick={ parent.parent.select }>
        <div class="row">
          <div class="col-sm-4">{ username }<br />{ get_full_name }&nbsp;</div>
          <div class="col-sm-8">{ email }<br/>{ paypal_email }
          </div>
        </div>
      </button>
    </div>
  </div>

  var that = this;
  that.students = [];
  var old_value = '',value;
  search(e) {
    value = that.root.querySelector("[name=q]").value;
    if (old_value == value) { return }
    uR.bounce(s,[e]);
    old_value = value;
  }
  function s(e) {
    var target = that.root.querySelector(".results");
    target.setAttribute("ur-loading","loading")
    if (!value) { that.students = []; target.removeAttribute("ur-loading"); return; }
    $.get(
      "/api/user/search/",
      {q: value},
      function(data) {
        target.removeAttribute("ur-loading");
        that.students = data;
        that.update()
      },
      "json"
    )
  }
  this.on("mount",function() {
    that.root.querySelector("[name=q]").focus();
    that.search();
  });
</search-users>

<checkbox>
  <a class="alert alert-block alert-{ alert_class }">
    <i class="fa fa-{ 'check-': has }square-o fa-3x"></i>
    <yield/>
  </a>

  this.on("update",function() {
    this.alert_class = this.has?"success":"danger";
  });

</checkbox>
