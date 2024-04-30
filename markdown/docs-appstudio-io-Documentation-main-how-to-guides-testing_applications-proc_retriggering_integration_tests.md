Retriggering Integration Tests
==============================

Integration test scenarios for a given snapshot can be re-triggered by adding a label to the snapshot.

Prerequisites
-------------

* You have a snapshot that has completed all its initial tests. All initial tests must be finished before you trigger subsequent tests.
* The snapshot for which tests will be retriggered has completed its initial tests
* You have CLI access to the specific OpenShift cluster. For information on obtaining CLI access, refer to [Getting started in CLI](../../../getting-started/getting_started_in_cli/)
* You have an up-to-date kubectl binary. Alternatively, the `oc` binary is also compatible.
Procedure
---------

1. Identify the IntegrationTestScenario that needs to be rerun. For a given snapshot, you can only rerun one IntegrationTestScenario.
2. Label the snapshot with `test.appstudio.openshift.io/run`, assigning the scenario name you wish to rerun as its value.


```
$ kubectl label snapshot [snapshot name] test.appstudio.openshift.io/run=[scenario name]
```
3. The tests are re-triggered automatically. Once they are re-triggered, the system removes the label, allowing you to apply a new label for a different scenario if you wish to test multiple scenarios.


```
$ tkn pipelinerun list[Example Output]NAME                            STARTED         DURATION   STATUSintegration-pipelinerun-jfrdb   4 seconds ago   ---        Running
```
4. To verify the tests, run `tkn pipelinerun describe [pipelinerun]` and ensure that the labels `appstudio.openshift.io/snapshot` and `test.appstudio.openshift.io/scenario` reference the correct snapshot and scenario.


```
$ tkn pipelinerun describe integration-pipelinerun-jfrdb[Expected labels in the output]Name:              integration-pipelinerun-jfrdbNamespace:         defaultService Account:   appstudio-pipelineLabels:... appstudio.openshift.io/snapshot=snapshot-sample... test.appstudio.openshift.io/test=component...
```
[Creating a custom integration test](../proc_creating_custom_test/)[Overview of Konflux environments](../../managing-environments/con_overview_of_environments/)