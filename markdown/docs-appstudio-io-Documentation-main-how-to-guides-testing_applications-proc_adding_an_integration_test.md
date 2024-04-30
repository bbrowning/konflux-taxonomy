Adding an integration test
==========================

In Konflux, you can add integration tests to verify that the individual components of your application integrate correctly, forming a complete and functional application. Konflux runs these integration tests on the container images of components before their deployment.

Prerequisites* You have created an application in Konflux.
ProcedureComplete the following steps in the Konflux console:

1. Open an existing application and go to the **Integration tests** tab.
2. Select **Add integration test**.
3. In the **Integration test name** field, enter a name of your choosing.
4. In the **GitHub URL** field, enter the URL of the GitHub repository that contains the test you want to use.
5. Optional: If you want to use a branch, commit, or version other than the default, specify the branch name, commit SHA, or tag in the **Revisions** field
6. In the **Path in repository** field, enter the path to the `.yaml` file that defines the test you want to use.
7. Optional: To allow the integration tests to fail without impacting the deployment and release process of your application, you can choose to select **Mark as optional for release**.



|  | By default, all integration test scenarios are mandatory and must pass. A failing integration test marks the application snapshot as failed, preventing its deployment and release. However, if you have selected **Mark as optional for release**, a failure in this test won’t hinder the deployment and release of the application snapshot. |
| --- | --- |
8. Select **Add integration test**.
9. Start a new build for any component you want to test.


	1. For components using the default build pipeline, go to the **Components** tab, select the three dots next to the name of the component, and select **Start new build**.
	2. For components with an upgraded build pipeline, make a commit to their GitHub repository.
VerificationWhen the new build is finished:

1. Go to the **Integration tests** tab and select the highlighted name of your test.
2. Go to the **Pipeline runs** tab of that test and select the most recent run.
3. On the **Details** page, you can see if the test succeeded for that component. Navigate to the other tabs for more details.
[Enabling a Snyk task](../enable_snyk_check_for_a_product/)[Creating a custom integration test](../proc_creating_custom_test/)