// Angular.js app for course
var myApp = angular.module("myApp", ["infinite-scroll"]);

myApp.controller("DemoController", function($scope) {
  $scope.courses = ALL_CLASSES;
  $scope.subjects = CLASS_SUBJECTS;
  $scope.active_subject = "";
  if (window.location.search.indexOf("young_adults") != -1) {
    $scope.active_subject = 22;
  }

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

  for (var ci=0; ci<ALL_CLASSES.length; ci++) {
    var course = ALL_CLASSES[ci];
    course.search_string = [course.name,course.short_description,course.subject_names.join(' ')];
    course.search_string = course.search_string.join(' ').toLowerCase();
    for (var csi=0; csi<course.subject_ids.length; csi++) {
      for (var si=0; si< $scope.subjects.length; si++) {
        var subject = $scope.subjects[si];
        if (subject.id != course.subject_ids[csi]) { continue; }
        if (course.next_time == 0) {
          subject.active_courses += 1;
        } else {
          subject.inactive_courses += 1;
        }
      }
    }
  }
  $scope.filterSubjects = function(value) {
    console.log(value)
    if (value != $scope.active_subject) {
      $scope.scheduled_courses = []; // visible "active" courses
      $scope._vsi = 0; // number of visible scheduled courses
      $scope.unscheduled_courses = []; // visible "inactive"
      $scope._vui = 0; // number of visible unscheduled courses
    }
    $scope.active_subject = value;

    $scope.active_courses = [];
    $scope.inactive_courses = [];
    for (var i=0;i<$scope.courses.length;i++) {
      var c = $scope.courses[i];
      if (!!value && c.subject_ids.indexOf(value) == -1) { continue; }
      if (!!current_search && c.search_string.indexOf(current_search) == -1 ) { continue; }
      if (c.next_time == 0) {
        $scope.inactive_courses.push(c);
      } else {
        $scope.active_courses.push(c);
      }
    }
    $scope.loadMore();
  }

  var current_search = '';
  $scope.filterSearch = function() {
    current_search = document.getElementById('courseSearch').value.toLowerCase();
    $scope.filterSubjects($scope.active_subject);
  }

  $scope.loadMore = function() {
    if (!$("#all_classes_tab").hasClass("active")) { return; }
    //if ($scope.inactive_courses.length && $scope._vui >= $scope.inactive_courses.length) {return }
    //$scope._vsi = Math.max($scope.scheduled_courses.length+6,$scope.active_courses.length);
    //$scope.scheduled_courses = $scope.active_courses.slice(0,$scope._vsi);
    //if ($scope._vsi < $scope.active_courses.length) { return }
    //$scope._vui = Math.max($scope.unscheduled_courses.length+6,$scope.inactive_courses.length);
    //$scope.unscheduled_courses = $scope.inactive_courses.slice(0,$scope._vui);
    $scope.scheduled_courses = $scope.active_courses;
    $scope.unscheduled_courses = $scope.inactive_courses;
  };

  $scope.filterSubjects( $scope.active_subject);
  
});
