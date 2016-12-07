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
  _ROOT + "js/router.js",
  _ROOT + "js/zepto.min.js",
  _ROOT + "js/wow_account.js",
  _ROOT + "js/sell_accounts.js",
  _ROOT + "js/items.js",
  _ROOT + "js/init.js",
  _ROOT + ".dist/sell_account.js",
];

gulp.task('build-js',['build-tag'], function () {
  return gulp.src(source_files)
    .pipe(sourcemaps.init())
    .pipe(concat('out.js'))
    //.pipe(uglify({mangle: false, compress: false}))
    .pipe(sourcemaps.write("."))
    .pipe(gulp.dest(_ROOT + ".dist/"));
});

gulp.task('build-tag', function() {
  return gulp.src([_ROOT + 'tags/*.tag'])
    .pipe(riot())
    .pipe(gulp.dest(_DEST));
});

var css_files = [
  _ROOT + "less/bootstrap.css",
  _ROOT + "wmd/wmd.css",
  _ROOT + "less/blog.css",
  _ROOT + "less/base.less",
]

gulp.task('build-css', function () {
  return gulp.src(css_files)//"static/bfish/**/*.less"])
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
