/**
 * Created by fan on 4/11/17.
 */
"use strict";
angular.module("smartorg.stnl.monitor", []).controller("MonitorCtrl", [
    "$scope", "$http", "$timeout", function ($scope, $http, $timeout) {
        var SERVICE_HOST = "http://127.0.0.1:5000";
        var PASSED = "passed";
        var FAILED = "failed";
        var WAIT_TIME = 30000; // 30 sec
        var BUZZ_ON = "buzz on";
        $scope.stnl = {
            monitoring: false,
            lastUpdate: undefined,
            status: "passed",
            failingBranches: [],
            buzzState: true
        };
        $scope.funcs = {
            loading: false,
            startMonitor: function () {
                $scope.stnl.monitoring = true;
                $scope.funcs.monitor();
            },
            stopMonitor: function () {
                $scope.stnl.monitoring = false;
            },
            getStatus: function () {
                $http({
                    method: "GET",
                    url: SERVICE_HOST + "/status"
                }).then(function (response) {
                    var rs = response.data;
                    $scope.stnl.status = rs;
                    if (rs == PASSED) {
                        // Do nothing
                    }
                    else if (rs == FAILED) {
                        $scope.funcs.getReport();
                    }
                    else {
                        // Do nothing
                    }
                }, function (err) {
                    console.error(err);
                });
            },
            getReport: function () {
                $http({
                    method: "GET",
                    url: SERVICE_HOST + "/report"
                }).then(function (response) {
                    var rs = response.data;
                    $scope.stnl.failingBranches =
                        $scope.funcs.getFailingBranch(rs);
                    $scope.stnl.lastUpdate = new Date();
                }, function (err) {
                    console.error(err);
                });
            },
            getFailingBranch: function (jsonReport) {
                var failingBranches = [];
                var repos = Object.keys(jsonReport);
                var _loop_1 = function (r) {
                    jsonReport[r].forEach(function (branchReport) {
                        if (branchReport.branch.state == FAILED) {
                            failingBranches.push({
                                "repo": r,
                                "branch": branchReport.branch,
                                "commit": branchReport.commit
                            });
                        }
                    });
                };
                for (var _i = 0, repos_1 = repos; _i < repos_1.length; _i++) {
                    var r = repos_1[_i];
                    _loop_1(r);
                }
                return failingBranches;
            },
            monitor: function () {
                $scope.funcs.getStatus();
                $timeout(function () {
                    if ($scope.stnl.monitoring) {
                        $scope.funcs.monitor();
                    }
                }, WAIT_TIME);
            },
            loadBuzzState: function () {
                $http({
                    method: "GET",
                    url: SERVICE_HOST + "/buzz"
                }).then(function (response) {
                    var rs = response.data;
                    $scope.stnl.buzzState = rs === BUZZ_ON;
                }, function (err) {
                    console.error(err);
                });
            },
            buzzSwitch: function () {
                var state = !$scope.stnl.buzzState ? "on" : "off";
                $http({
                    method: "PUT",
                    url: SERVICE_HOST + "/buzz/" + state
                }).then(function (response) {
                    var rs = response.data;
                    $scope.stnl.buzzState = rs === BUZZ_ON;
                }, function (err) {
                    console.error(err);
                });
            }
        };
        $timeout(function () {
            $scope.funcs.loadBuzzState();
        });
    }
]);
