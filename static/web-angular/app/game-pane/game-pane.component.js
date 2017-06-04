/**
 * Created by jsz on 2016/10/20.
 */
'use strict';
angular.module('gamePane').component('gamePane', {
    templateUrl: 'game-pane/game-pane.template.html',
    controller: ['$scope', '$routeParams', '$http','$location',function GamePaneController($scope, $routeParams,$http,$location) {

        var players_names = $routeParams.names.replace(':','').split(',');
        var successFun = function (data, status, headers, config) {
            $scope.current_player = data['current_player'];
            $scope.messages = data['messages'];
        };

        var errorFun = function (data, status, headers, config) {
            $scope.messages = ['Hello Boys! Something Wrong!']
        };
        // init the page
        $http({
            method: 'GET',
            url: '/nextTurn',
            params: players_names
        }).success(successFun).error(errorFun);

        $scope.nextTurn= function () {
            $http({
                method: 'POST',
                url: '/nextTurn'
            }).success(function (data,staus,headers,config) {
                $scope.current_player = data['current_player'];
                $scope.messages = data['messages'];
                if(data.is_over){
                    $location.path('/gameOver/:'+ data['messages']);
                }
            }).error(errorFun);
        };
    }]
});