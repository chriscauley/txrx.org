$(function() {
  var active_subject;
  // set enrollment status for ALL_CLASSES
  for (var si=0; si<USER_SESSIONS.length;si++) {
    session = USER_SESSIONS[si];
    for (var ci=0; ci<ALL_CLASSES.length;ci++) {
      c = ALL_CLASSES[ci];
      if (c.id == session.course_id) {
        c.enrolled_status = session.enrolled_status;
        c.well_class = session.closed_status || "enrolled";
      }
    }
  }

  // assign ALL_CLASSES to subjects and generate search string
  for (var ci=0; ci<ALL_CLASSES.length; ci++) {
    var course = ALL_CLASSES[ci];
    course.search_string = [course.name,course.short_description,course.subject_names.join(' ')];
    course.search_string = course.search_string.join(' ').toLowerCase();
    for (var csi=0; csi<course.subject_ids.length; csi++) {
      for (var si=0; si< CLASS_SUBJECTS.length; si++) {
        var subject = CLASS_SUBJECTS[si];
        if (subject.id != course.subject_ids[csi]) { continue; }
        if (course.next_time == 0) { subject.active_courses += 1; }
        else { subject.inactive_courses += 1; }
      }
    }
  }

  // course lists and search
  var current_search, active_subject, scheduled_courses, unscheduled_courses;

  function filterSubjects(value) {
    scheduled_courses = [];
    unscheduled_courses = [];
    for (var i=0;i<ALL_CLASSES.length;i++) {
      var c = ALL_CLASSES[i];
      if (!!value && c.subject_ids.indexOf(value) == -1) { continue; }
      if (!!current_search && c.search_string.indexOf(current_search) == -1 ) { continue; }
      if (c.next_time == 0) { unscheduled_courses.push(c); }
      else { scheduled_courses.push(c); }
    }
    $("#scheduled-courses").replaceWith('<course-list id="scheduled-courses"></course-list>');
    $("#unscheduled-courses").replaceWith('<course-list id="unscheduled-courses"></course-list>');
    riot.mount("#scheduled-courses",{courses: scheduled_courses});
    riot.mount("#unscheduled-courses",{courses: unscheduled_courses});
  }

  function filterSearch(value) {
    current_search = value;
    filterSubjects(active_subject);
  }

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
