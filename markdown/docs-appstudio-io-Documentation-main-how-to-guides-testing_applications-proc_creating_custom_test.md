Creating a custom integration test
==================================

In Konflux, you can create your own integration tests to run on all components of a given application before they are deployed.

ProcedureTo create any custom test, complete the following steps:

1. In your preferred IDE, create a Tekton pipeline in a `.yaml` file.
2. Within that pipeline, create tasks, which define the actual steps of the test that Konflux executes against images before deploying them.
3. Commit the `.yaml` file to a GitHub repo and add it as an integration test in Konflux.
Procedure with exampleTo create a custom test that checks that your app serves the text “Hello world!”, complete the following steps:

1. In your preferred IDE, create a new `.yaml` file, with a name of your choosing.
2. Define a new Tekton pipeline. The following example is the beginning of a pipeline that uses `curl` to check that the app serves the text “Hello world!”.

Example pipeline file:


```
kind: PipelineapiVersion: tekton.dev/v1beta1metadata:  name: example-pipelinespec:  params:    - description: 'Snapshot of the application'      name: SNAPSHOT      default: '{"components": [{"name":"test-app", "containerImage": "quay.io/example/repo:latest"}]}'      type: string  tasks:
```
3. In the `.pipeline.spec` path, declare a new task.

Example task declaration:


```
tasks:  - name: task-1    description: Placeholder task that prints the Snapshot and outputs standard TEST_OUTPUT    params:      - name: SNAPSHOT        value: $(params.SNAPSHOT)    taskSpec:      params:      - name: SNAPSHOT      results:      - name: TEST_OUTPUT        description: Test output      steps:      - image: registry.redhat.io/openshift4/ose-cli:latest        env:        - name: SNAPSHOT          value: $(params.SNAPSHOT)        script: |          dnf -y install jq          echo -e "Example test task for the Snapshot:\n ${SNAPSHOT}"          // Run custom tests for the given Snapshot here          // After the tests finish, record the overall result in the RESULT variable          RESULT="SUCCESS"          // Output the standardized TEST_OUTPUT result in JSON form          TEST_OUTPUT=$(jq -rc --arg date $(date +%s) --arg RESULT "${RESULT}" --null-input \            '{result: $RESULT, timestamp: $date, failures: 0, successes: 1, warnings: 0}')          echo -n "${TEST_OUTPUT}" | tee $(results.TEST_OUTPUT.path)
```
4. Save the `.yaml` file.


	1. If you haven’t already, commit this file to a GitHub repository that Konflux can access.
	
	Complete example file:
```
kind: PipelineapiVersion: tekton.dev/v1beta1metadata:  name: example-pipelinespec:  params:    - description: 'Snapshot of the application'      name: SNAPSHOT      default: '{"components": [{"name":"test-app", "containerImage": "quay.io/example/repo:latest"}]}'      type: string    - description: 'Namespace where the application is running'      name: NAMESPACE      default: "default"      type: string    - description: 'Expected output'      name: EXPECTED_OUTPUT      default: "Hello World!"      type: string  workspaces:  - name: cluster-credentials    optional: true  tasks:    - name: task-1      description: Placeholder task that prints the Snapshot and outputs standard TEST_OUTPUT      params:        - name: SNAPSHOT          value: $(params.SNAPSHOT)      taskSpec:        params:        - name: SNAPSHOT        results:        - name: TEST_OUTPUT          description: Test output        steps:        - image: registry.redhat.io/openshift4/ose-cli:latest          env:          - name: SNAPSHOT            value: $(params.SNAPSHOT)          script: |            dnf -y install jq            echo -e "Example test task for the Snapshot:\n ${SNAPSHOT}"            // Run custom tests for the given Snapshot here            // After the tests finish, record the overall result in the RESULT variable            RESULT="SUCCESS"            // Output the standardized TEST_OUTPUT result in JSON form            TEST_OUTPUT=$(jq -rc --arg date $(date +%s) --arg RESULT "${RESULT}" --null-input \              '{result: $RESULT, timestamp: $date, failures: 0, successes: 1, warnings: 0}')            echo -n "${TEST_OUTPUT}" | tee $(results.TEST_OUTPUT.path)
```
5. Add your new custom test as an integration test in Konflux.


	1. For additional instructions on adding an integration test, see this document: [Adding an integration test](../proc_adding_an_integration_test/).
Data injected into the PipelineRun of the integration testWhen you create a custom integration test, Konflux automatically adds certain parameters, workspaces, and labels to the PipelineRun of the integration test. This section explains what those parameters, workspaces, and labels are, and how they can help you.

Parameters:

* **`SNAPSHOT`**: contains the [snapshot](../../../glossary/#_snapshot) of the whole application as a JSON string. This JSON string provides useful information about the test, such as which components Konflux is testing, and what git repository and commit Konflux is using to build those components. For information about snapshot JSON string, see [an example snapshot JSON string](https://github.com/redhat-appstudio/integration-examples/blob/main/examples/snapshot_json_string_example).
Labels:

* **`appstudio.openshift.io/application`**: contains the name of the application.
* **`appstudio.openshift.io/component`**: contains the name of the component.
* **`appstudio.openshift.io/snapshot`**: contains the name of the snapshot.
* **`test.appstudio.openshift.io/optional`**: contains the optional flag, which specifies whether or not components must pass the integration test before deployment.
* **`test.appstudio.openshift.io/scenario`**: contains the name of the integration test (this label ends with "scenario," because each test is technically a custom resource called an `IntegrationTestScenario`).
VerificationAfter adding the integration test to an application, you need to trigger a new build of its components to make Konflux run the integration test. Make a commit to the GitHub repositories of your components to trigger a new build.

When the new build is finished, complete the following steps in the Konflux console:

1. Go to the **Integration tests** tab and select the highlighted name of your test.
2. Go to the **Pipeline runs** tab of that test and select the most recent run.
3. On the **Details** page, see if the test succeeded for that component. Select the other tabs to view more details.


	1. If you used our example script, switch to the **Logs** tab and verify that the test printed “Hello world!”.
[Adding an integration test](../proc_adding_an_integration_test/)[Retriggering integration tests](../proc_retriggering_integration_tests/)