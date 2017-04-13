/**
 * Created by fan on 4/11/17.
 */

module smartorg.stnl.monitor {
    export interface IPlumScope {
        stnl: {
            monitoring: boolean;
            lastUpdate: Date;
            status: string;
            failingBranches: Array<any>;
            buzzState: boolean;
        };

        funcs: any;

        test: Function;

        serverReports: Array<any>;
    }
}

"use strict";

angular.module(
    "smartorg.stnl.monitor", []
).controller("MonitorCtrl", [
    "$scope", "$http", "$timeout", ($scope: smartorg.stnl.monitor.IPlumScope,
                                    $http, $timeout) => {

        const SERVICE_HOST = "http://127.0.0.1:5000";
        const PASSED = "passed";
        const FAILED = "failed";
        const WAIT_TIME = 30000;  // 30 sec

        const BUZZ_ON = "buzz on";

        $scope.stnl = {
            monitoring: false,
            lastUpdate: undefined,
            status: "passed",
            failingBranches: [],
            buzzState: true
        };

        $scope.funcs = {
            loading: false,

            startMonitor: () => {
                $scope.stnl.monitoring = true;
                $scope.funcs.monitor();
            },

            stopMonitor: () => {
                $scope.stnl.monitoring = false;
            },

            getStatus: () => {
                $http({
                    method: "GET",
                    url: SERVICE_HOST + "/status"
                }).then((response) => {
                    let rs = response.data;

                    $scope.stnl.status = rs;

                    if (rs == PASSED) {
                        // Do nothing
                    } else if (rs == FAILED) {
                        $scope.funcs.getReport();
                    } else {
                        // Do nothing
                    }
                }, (err) => {
                    console.error(err);
                })
            },

            getReport: () => {
                $http({
                    method: "GET",
                    url: SERVICE_HOST + "/report"
                }).then((response) => {
                    let rs = response.data;

                    $scope.stnl.failingBranches =
                        $scope.funcs.getFailingBranch(rs);

                    $scope.stnl.lastUpdate = new Date();
                }, (err) => {
                    console.error(err);
                })
            },

            getFailingBranch: (jsonReport: any) => {
                let failingBranches = [];

                let repos = Object.keys(jsonReport);
                for (let r of repos) {
                    jsonReport[r].forEach(branchReport => {
                        if (branchReport.branch.state == FAILED) {
                            failingBranches.push({
                                "repo": r,
                                "branch": branchReport.branch,
                                "commit": branchReport.commit
                            });
                        }
                    });
                }

                return failingBranches;
            },

            monitor: () => {
                $scope.funcs.getStatus();

                $timeout(() => {
                    if ($scope.stnl.monitoring) {
                        $scope.funcs.monitor();
                    }
                }, WAIT_TIME);
            },

            loadBuzzState: () => {
                $http({
                    method: "GET",
                    url: SERVICE_HOST + "/buzz"
                }).then((response) => {
                    let rs = response.data;

                    $scope.stnl.buzzState = rs === BUZZ_ON;
                }, (err) => {
                    console.error(err);
                })
            },

            buzzSwitch: () => {
                let state = !$scope.stnl.buzzState ? "on" : "off";

                $http({
                    method: "PUT",
                    url: SERVICE_HOST + "/buzz/" + state
                }).then((response) => {
                    let rs = response.data;

                    $scope.stnl.buzzState = rs === BUZZ_ON;
                }, (err) => {
                    console.error(err);
                })
            }
        };

        $timeout(() => {
            $scope.funcs.loadBuzzState();
        });
    }
]);