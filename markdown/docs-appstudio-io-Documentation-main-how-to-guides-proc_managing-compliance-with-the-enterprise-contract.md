Managing compliance with the Enterprise Contract
================================================

The Enterprise Contract (EC) is an artifact verifier and customizable policy checker. By default, Konflux adds the Enterprise Contract as an integration test to each new application. The Enterprise Contract then keeps your software supply chain secure and ensures container images comply with your organization’s policies. It does this by verifying the security and provenance of builds created through Konflux.

Konflux’s build process uses Tekton Chains to produce a signed in-toto attestation of the build pipeline. The Enterprise Contract then uses this attestation to verify the build’s integrity and compliance with a set of policies. These policies include best practices and any organization-specific requirements.

If you ever need to restore the default EC integration test to an application, or if you want to use a different configuration of the EC as an integration test, use the following procedure.

Prerequisites* You have created an application.
* You have an upgraded build pipeline.
Procedure1. In the Konflux UI, open an existing application and go to the **Integration tests** tab.
2. Select **Add integration test**.
3. In the **Integration test name** field, enter a name of your choosing.
4. In the **GitHub URL** field, enter **<https://github.com/redhat-appstudio/build-definitions>**
5. In the **Path in repository** field, to use the default EC configuration, enter **/pipelines/enterprise-contract.yaml**


	1. You can also enter any of the paths in the [list of Enterprise Contract Configuration Files](https://github.com/enterprise-contract/config#readme), to use a configuration that matches your specific needs more closely.
	2. For example, to verify your artifacts with the policy rules that Red Hat uses, enter **/pipelines/enterprise-contract-redhat.yaml**
6. Optional: If passing the this test is optional, and you do not want to prevent the application from being deployed or released, then select **Mark as optional for release**.
7. Select **Add Integration test**.
8. Trigger a new build by commiting a change in the GitHub repository of the application you are working with.
Verification1. On your application, go to the **Activity > Pipeline** runs tab.
2. Select a pipeline run with **Type** as **Test**, and review the status of your test pipeline.
3. You can also review pipeline run details, logs, task runs, and security details by selecting a pipeline run with **Type** as **Test**.
Additional resources* To produce a signed [in-toto](https://in-toto.io/in-toto/) attestation of the build pipeline, go to [Tekton Chains](https://tekton.dev/docs/chains/).
* For information on the source code for the Tekton pipelines defined in the bundle, see the [build-definitions](https://github.com/redhat-appstudio/build-definitions/blob/main/pipelines/enterprise-contract.yaml) and[ec-cli](https://github.com/enterprise-contract/ec-cli/blob/main/tasks/verify-enterprise-contract/0.1/verify-enterprise-contract.yaml) repositories.
* To use a specific version of the pipeline bundle instead of the devel tag, you can select one of the [pinned tags](https://quay.io/repository/redhat-appstudio-tekton-catalog/pipeline-enterprise-contract?tab=tags).
* For information on components in Enterprise Contract, see the [Components](https://enterprisecontract.dev/docs/ec/main/index.html#_components).
* For information on the Enterprise Contract policies designed for Konflux, see the [Enterprise Contract Policies](https://enterprisecontract.dev/docs/ec-policies/index.html).
[Configuring dependencies rebuild for Java apps in the CLI](../Secure-your-supply-chain/proc_java_dependencies/)[Releasing an application](../con_release_application/)