<course-filters>
  <input type="checkbox" id="toggle_filters" name="toggle"/>
  <label for="toggle_filters" class="btn btn-success">Filter by Subject</label>
  <form onsubmit={ apply } class="filters course_filters" autocomplete="off">
    <input name="q" id="classes_q" class="form-control" placeholder="Search Classes" onkeyup={ search } 
           onblur={ apply } id="courseSearch" />
    <div class="list_filter btn-group-vertical">
      <label class="btn btn-default { opts.active_subject?' ':'selected' }" onclick={ click }>All Subjects</label>
    </div>
    <div each={ CLASS_SUBJECTS } class="list_filter btn-group-vertical">
      <label if={ active_courses + inactive_courses } onclick={ parent.click }
             class="btn btn-default { (parent.opts.active_subject == value)?'selected':' ' }" >{ name }</label>
      <!--
          <div each={ children } class="child">
            <input type="radio" value={ value } id="filter_subject_{ value }" name="subject" />
            <label for="filter_subject_{ value }" class="btn btn-default" onclick={ filter }>-- { name }</label>
          </div>
          -->
    </div>
  </form>

  click(e) {
    opts.filterSubjects(e.item?e.item.value:"");
    opts.active_subject = (e.item || {}).value;
    this.toggle_filters.checked = false;
    riot.update();
  }
  apply(e) {
    opts.filterSearch(this.classes_q.value);
    this.toggle_filters.checked = false;
    riot.update();
  }
  search(e) {
    opts.filterSearch(this.classes_q.value);
    riot.update();
  }
  this.search = uR.debounce(this.search);
</course-filters>

<course-list>
  <div each={ opts.courses } if={ visible }>
    <a href={ url } class="course well { well_class }" id="course_{ id }">
      <div class="picture">
        <img src={ im.url } width={ im.width } height={ im.height } />
        <div class="enrolled-status" status={ enrolled_status }></div>
      </div>
      <div class="details">
        <div class="subjects" if={ TXRX.DEBUG }><span each={ subject in subject_names }>{ subject }</span></div>
        <div class="title">{ name }</div>
        <div class="description">{ short_description }</div>
        <div class="enrolled-status" data-status={ enrolled_status }></div>
        <div class="sessions" if={ active_sessions.length }>
          <span class="next_session { active_sessions[0].closed_status }">{ active_sessions[0].short_dates }</span>
          <div class="pull-right">
            <span class="full_sessions" if={ full_sessions.length }>
              [{ full_sessions.length } Full<span class=" hidden-xs">
                Session{ (full_sessions.length > 1)?"s":"" }</span>]
            </span>
            <span class="open_sessions" if={ open_sessions.length }>
              [{ open_sessions.length } Open<span class=" hidden-xs">
                Session{ (open_sessions.length > 1)?"s":"" }</span>]
            </span>
          </div>
        </div>
      </div>
      <div class="price">{ (fee > 0 && next_time != 0)?("$"+fee):"FREE" }</div>
    </a>
  </div>
</course-list>

<session-list>
  <h1 class="fee page_title" if={ opts.active_sessions }>
    <span if={ opts.fee }>${ opts.fee }</span>
    <span if={ !opts.fee }>Free</span>
  </h1>
  <h3 if={ opts.active_sessions }>Upcoming Sessions:</h3>
  <div class="session well" id="s{ id }" each={ opts.active_sessions }>
    <a if={ parent.user.is_superuser || instructor_pk == parent.user.id }
       href="/classes/instructor_session/{ id }/" class="instructor-link fa fa-edit"></a>
    <a if={ parent.user.is_superuser } href="/admin/course/session/{ id }/"
       class="admin-link fa fa-pencil-square"></a>
    <div class="date" each={ classtimes }>
      { moment.format("ddd MMM D") } { start_time } - { end_time } 
    </div>
    <div class="instructor">with { instructor_name }</div>
    <b class="full" if={ closed_status == 'full' }>This session is full</b>
    <b class="full" if={ closed_status == 'past' }>This session has passed</b>
    <b class="full" if={ closed_status == 'private' }>This session is private</b>
    <b class="full" if={ closed_status == 'cancelled' }>This session has been canceled. If you were enrolled and have not received an email, please contact <a href="mailto:{ uR.config.support_email }">{ uR.config.support_email }</a></b>
    <div if={ !closed_status && fee }>
      <add-to-cart product_id={ product_id } add_text="Add this session to  cart"></add-to-cart>
    </div>
    <div if={ !closed_status && !fee }>
      <button class="btn btn-success rsvp" onclick={ parent.rsvp } if={ !rsvpd && parent.user.id }>
        RSVP for this event</button>
      <button class="btn btn-danger unrsvp" onclick={ parent.unrsvp } if={ rsvpd && parent.user.id }>
        Cancel RSVP</button>
      <a if={ !parent.user.id } href="/accounts/login/?next={ window.location.href }">
        Login to RSVP</a>
      <div class="alert alert-warning" if={ message }>{ message }</div>
    </div>
  </div>
  <a if={ user.is_superuser && opts.past_session_count } class="btn btn-success btn-block"
     onclick={ loadPastSessions }>
    Show { opts.past_session_count } Archived Sessions</a>

  this.user = uR.auth.user;
  var self = this;
  add(e) {
    uR.drop.saveCartItem(e.item.product_id,1,this);
  }
  viewCart(e) {
    $("#cartModal").modal({show:true});
  }
  loadPastSessions(e) {
    var target = e.target;
    target.setAttribute("ur-loading","loading");
    $.get(
      '/classes/past_sessions.json?id='+self.opts.id,
      {},
      function(data) {
        target.removeAttribute("ur-loading","loading");
        self.opts.active_sessions = self.opts.active_sessions.concat(data);
        self.opts.past_session_count = 0;
        self.update();
      },
      'json'
    );
  }
  function _rsvp(e,url) {
    var target = document.getElementById("s"+e.item.id);
    target.setAttribute("ur-loading","loading");
    $.get(
      url,
      function(data) {
        target.removeAttribute("ur-loading","loading");
        uR.auth.user.enrollments[e.item.id] = data.quantity;
        e.item.message = data.message;
        self.update();
      },
      "json"
    );
  }
  rsvp(e) {
    var url = "/classes/rsvp/"+e.item.id+"/";
    _rsvp(e,url);
  }
  unrsvp(e) {
    var url = "/classes/unrsvp/"+e.item.id+"/";
    _rsvp(e,url);
  }
  function showSmartTime(moment) {
    if (moment.minutes() == 0) {
      if (moment.hours() == 0) { return "midnight" }
      if (moment.hours() == 12) { return "noon" }
      return moment.format("ha")
    }
    return moment.format("h:mma")
  }
  this.on("update",function() {
    uR.forEach(this.opts.active_sessions,function(session) {
      var user = uR.auth.user;
      if (window.location.search.indexOf("overbook="+session.id) != -1) { session.closed_status = ""; }
      session.fee = self.opts.fee;
      if (user && user.enrollments) { session.rsvpd = user.enrollments[session.id]; }
      session.incart = false;
      uR.forEach(session.classtimes,function(classtime) {
        classtime.moment = moment(classtime.start);
        classtime.start_time = showSmartTime(classtime.moment);
        classtime.end_moment = moment(classtime.end);
        classtime.end_time = showSmartTime(classtime.end_moment);
      });
      if (session.product_id) { uR.drop.product_on_page = uR.drop.products[session.product_id]; }
    });
  });
</session-list>
