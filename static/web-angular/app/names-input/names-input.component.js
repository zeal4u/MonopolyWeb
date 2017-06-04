/**
 * Created by jsz on 2016/10/20.
 */
'use strict';
angular.
    module('namesInput').
    component('namesInput',{
        templateUrl: 'names-input/names-input.template.html',
        controller:  ['$scope','$http','$location',
            function IndexController($scope,$http,$location) {
                var player_names = [];
                $scope.startPlay = function(players) {
                    var players = angular.copy(players);

                    if(players.names != ''){
                        $location.path('/game/:'+players.names);
                    }
                };
            }
        ]
    });