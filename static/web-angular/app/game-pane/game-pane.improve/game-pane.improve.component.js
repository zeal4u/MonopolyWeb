/**
 * Created by jsz on 2016/10/22.
 */
angular.module('gamePaneImprove').component('gamePaneImprove', {
    templateUrl: 'game-pane/game-pane.improve/game-pane.improve.template.html',
    controller: ['$scope', '$routeParams', '$http', '$location','$timeout', function GamePaneController($scope, $routeParams, $http, $location,$timeout) {

        var players_names = $routeParams.names.replace(':', '').split(',');
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


        $scope.nextTurn = function () {
            $http({
                method: 'POST',
                url: '/nextTurnImprove'
            }).success(function (data, staus, headers, config) {
                // here neead to write something for controlling the animation

                $scope.current_player = data['current_player'];

                positions = data['positions']
                messages = data['messages'];

                if (data.isOver) {
                    $location.path('/gameOver/:' + data['messages']);
                }else{
                    for(i = 0; i < positions.length();i++){
                        $timeout(function () {
                            $scope.position = positions[i];
                            $scope.message = messages[i];
                        },500,true);
                    }
                }

            }).error(errorFun);
        };
    }]
});