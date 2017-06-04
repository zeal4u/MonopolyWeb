/**
 * Created by jsz on 2016/10/21.
 */
angular.module('gameOver').
    component('gameOver',{
        templateUrl: 'game-over/game-over.template.html',
        controller : ['$scope','$routeParams',function ($scope,$routeParams) {
          $scope.messages = $routeParams.messages.replace(':','');
        }]
    });