var app = angular.module("booksgalore");

// Since Jinja2 and Angular use the syntax to identify their expressions
// it is advisable to interpolate Angular to recognise {[ instead of {{

app.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[');
  $interpolateProvider.endSymbol(']}');
}]);

app.config(function($logProvider){
    $logProvider.debugEnabled(true);
});