/**
 * Created by fan on 4/11/17.
 */

module smartorg.stnl.monitor {
    export interface IPlumScope {
        getDataFrom: Function;
        test: Function;

        serverReports: Array<any>;
    }
}

'use strict';

angular.module(
    'sentinellaMonitor', []
).controller('MonitorCtrl', [
    '$scope', ($scope: smartorg.stnl.monitor.IPlumScope) => {

        $scope.getDataFrom = () => {

        };

        $scope.test = () => {
            $scope.serverReports = [{
                "project": "AstroService",
                "status": "stable",
                "updated": "2016-04-28T23:12:04Z",
                "build": 130
            }, {
                "project": "Sequoia",
                "status": "stable",
                "updated": "2016-07-25T17:36:05Z",
                "build": 140
            }, {
                "project": "Sequoia-Dev",
                "status": "stable",
                "updated": "2016-08-03T23:55:04Z",
                "build": 537
            }, {
                "project": "Sequoia-Dev-Testem",
                "status": "stable",
                "updated": "2016-08-03T23:48:28Z",
                "build": 492
            }];
        };

        $scope.getDataFrom();
    }
]);