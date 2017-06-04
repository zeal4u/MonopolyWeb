/**
 * Created by jsz on 2016/10/20.
 * this this route of website
 */
'use strict';
angular.
  module('monopolyApp').
  config(['$routeProvider',
    function ($routeProvider) {
      $routeProvider.
          when('/game',{
           template: '<game-pane></game-pane>'
      }).
          when('/game/:names',{
            template: '<game-pane></game-pane>',
      }).
          when('/names-input',{
            template: '<names-input></names-input>'
      }).
          when('/record',{
            template: '<record-table></record-table>'
      }).
          when('/gameOver/:messages',{
            template: '<game-over></game-over>'
      }).
          otherwise({redirectTo:'/names-input'});
    }]
  );
