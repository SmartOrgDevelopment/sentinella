/**
 * Created by fan on 4/11/17.
 */
'use strict';
angular.module('sentinella', [
    "ngRoute",
    "sentinellaMonitor"
]).config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/monitor', {
            controller: 'MonitorCtrl',
            templateUrl: 'template/monitor.html'
        }).otherwise({ redirectTo: '/monitor' });
    }]);
