window.NO_DISCOUNT = [];
uR.auth.ready(function() {
  var active_subject;
  window.COURSE_MAP = {};
  uR.forEach(ALL_CLASSES,function(c) { COURSE_MAP[c.id] = c; });
  // set enrollment status for ALL_CLASSES, this can be moved to course.tag 
  if (uR.auth.user) {
    uR.forEach(uR.auth.user.enrolled_course_ids,function(c_id) {
      var c = COURSE_MAP[c_id];
      if (!c) { return } // Course is inactive
      c.enrolled_status = "completed";
      if (uR.auth.user.completed_course_ids.indexOf(c_id) == -1) {
        c.enrolled_status = "enrolled";
        c.well_class = "enrolled";
      }
    })
  }

  // assign ALL_CLASSES to subjects and generate search string
  // this should be part of the mount or update section of course list
  for (var ci=0; ci<ALL_CLASSES.length; ci++) {
    var course = ALL_CLASSES[ci];
    course.search_string = [course.name,course.short_description,course.subject_names.join(' ')];
    course.search_string = course.search_string.join(' ').toLowerCase();
    if (course.no_discount) {
      uR.forEach(course.active_sessions, function(s) { window.NO_DISCOUNT.push(s.id); });
    }

    //Tally number of active classes in each subject.
    for (var csi=0; csi<course.subject_ids.length; csi++) {
      for (var si=0; si< CLASS_SUBJECTS.length; si++) {
        var subject = CLASS_SUBJECTS[si];
        if (subject.id != course.subject_ids[csi]) { continue; }
        if (course.next_time == 0) { subject.active_courses += 1; }
        else { subject.inactive_courses += 1; }
      }
    }
    course.full_sessions = [];
    course.open_sessions = [];
    for (var si=0;si<course.active_sessions.length;si++) {
      var session = course.active_sessions[si];
      if (FULL_SESSIONS.indexOf(session.id) == -1) { course.open_sessions.push(session); }
      else { course.full_sessions.push(session); }
    }
  }
  // course lists and search
  var current_search = '', scheduled_courses = [], unscheduled_courses = [];
  function filterSubjects(value) {
    active_subject = value || active_subject;
    current_search = current_search.toLowerCase();
    uR.forEach(ALL_CLASSES, function(c) {
      c.visible = true;
      if (!!value && c.subject_ids.indexOf(value) == -1) { c.visible = false; }
      if (!!current_search && c.search_string.indexOf(current_search) == -1 ) { c.visible = false; }
    });
    riot.update('course-list');
  }

  uR.forEach(ALL_CLASSES,function(c) {
    if (c.next_time == 0) {
      // don't show gardening in unscheduled courses because there are a lot of them
      if (c.subject_ids.indexOf(27) == -1) { unscheduled_courses.push(c); }
    }
    else { scheduled_courses.push(c); }
  });
  function filterSearch(value) {
    current_search = value;
    filterSubjects(active_subject);
  }

  riot.mount("#course-tabs");
  document.getElementById("scheduled-courses").appendChild(document.createElement("course-list"))
  riot.mount("#scheduled-courses course-list",{courses: scheduled_courses});
  document.getElementById("unscheduled-courses").appendChild(document.createElement("course-list"))
  riot.mount("#unscheduled-courses course-list",{courses: unscheduled_courses});

  if (window.location.search.indexOf('young_adults') != -1) {
    filterSubjects(22);
    active_subject = 22;
  } else {
    filterSubjects();
  }
  riot.mount("course-filters",{
    active_subject: active_subject,
    current_search: current_search,
    filterSubjects: filterSubjects,
    filterSearch: filterSearch
  });
  if (unscheduled_courses) { $(".course_divider").show(); }
});
// #! TODO
// Currently only used in the course tabs section. Should be replaced with ur-tabs
$(function() {
  $('[data-toggle="tab"]').click(function(e) {
    var $this = $(this), loadurl = $this.data('href'), targ = $($this.attr('href'));
    if (!loadurl) { return true; }

    $this.removeData('href');

    if (targ.hasClass("needs_ajax")) {
      $.get(loadurl, function(data) {
        targ.html(data).removeClass("needs_ajax");
      });
    }
  });
});
