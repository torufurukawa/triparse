var gulp = require('gulp');
var typescript = require('gulp-typescript');
var exec = require('child_process').exec;

gulp.task('build', function() {
  var options = {out: 'main.js'};
  gulp.src([
    './*.ts',
    '!./node_modules/**'
  ])
  .pipe(typescript(options))
  .pipe(gulp.dest('./'));
});

gulp.task('main', function (callback) {
  exec('node main.js', function (err, stdout, stderr) {
    console.log(stdout);
    console.log(stderr);
    callback(err);
  });
})

gulp.task('watch', function(){
  gulp.watch('./*.ts', ['build', 'main']);
});
