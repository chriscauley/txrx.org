var riot = require('gulp-riot');
var gulp = require('gulp');
var concat = require("gulp-concat");
var less = require('gulp-less');
var rollup = require('gulp-rollup');
var sourcemaps = require("gulp-sourcemaps");
var through = require('through2');
var uglify = require('gulp-uglify');
var util = require('gulp-util');

var _ROOT = "main/static/";
var _DEST = ".static/"

var source_files = [
  _ROOT + "less/bootstrap/js/collapse.js",
  _ROOT + "less/bootstrap/js/modal.js",
  _ROOT + "less/bootstrap/js/transition.js",
  _ROOT + "less/bootstrap/js/alert.js",
  _ROOT + "less/bootstrap/js/dropdown.js",
  _ROOT + "less/bootstrap/js/tooltip.js",
  _ROOT + "less/bootstrap/js/popover.js",
  _ROOT + "less/bootstrap/js/tab.js",
  _ROOT + "js/moment.js",
  _ROOT + "js/simpleCart.js",
  _ROOT + "js/cart.js",
  _ROOT + "js/init.js",
  _ROOT + "js/blog.js",
  _ROOT + "js/favico.js",
  _ROOT + "js/course.js",
  ".static/_tags.js",
];

gulp.task('build-js',['build-tag'], function () {
  return gulp.src(source_files)
    .pipe(sourcemaps.init())
    .pipe(concat('txrx-built.js'))
    //.pipe(uglify({mangle: false, compress: false}))
    .pipe(sourcemaps.write("."))
    .pipe(gulp.dest(_DEST));
});

var tag_files = [
  _ROOT + "tags/course.tag",
  _ROOT + "tags/store.tag"
];

gulp.task('build-tag', function() {
  return gulp.src(tag_files)
    .pipe(riot())
    .pipe(concat('_tags.js'))
    .pipe(gulp.dest(_DEST));
});

var css_files = [
  _ROOT + "less/bootstrap.css",
  _ROOT + "wmd/wmd.css",
  _ROOT + "less/blog.css",
  _ROOT + "less/base.less",
]

gulp.task('build-css', function () {
  return gulp.src(css_files)
    .pipe(less({}))
    .pipe(concat('txrx-built.css'))
    .pipe(gulp.dest(_DEST));
});

var build_tasks = ['build-js', 'build-css'];

gulp.task('watch', build_tasks, function () {
  gulp.watch(["main/static/js/*.js","main/static/tags/*.tag"], ['build-js']);
  gulp.watch("main/static/less/**/*.less", ['build-css']);
});

gulp.task('default', build_tasks);
