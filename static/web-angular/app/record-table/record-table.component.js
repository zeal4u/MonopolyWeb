/**
 * Created by jsz on 2016/10/20.
 */
'use strict';
angular.module('recordTable').
    component('recordTable',{
    templateUrl: 'record-table/record-table.template.html',
    controller: ['$scope','$http','$location',function RecordController($scope,$http, $location) {
        $scope.records = {}
        var getRecord = function () {
            $http({
                method: 'POST',
                url: '/getRecord',
            }).success(function (data,status,headers,config) {
                $scope.records = data
            })
        };
        getRecord();
    }
    ]
});