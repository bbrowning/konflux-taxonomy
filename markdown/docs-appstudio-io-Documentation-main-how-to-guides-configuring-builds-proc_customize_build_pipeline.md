Customizing the build pipeline
==============================

To meet your specific needs, customize the way that Konflux builds components. You can customize in two ways:

* Change the parameters of the build pipeline of a component.
* Extend the pipeline with your own tasks (or deleting existing tasks).
For example, you can change for how long Konflux saves the container images of component, by changing the value of the `image-expires-after` parameter. Or you can ensure that the container images it builds for a component are compliant with regulations for your industry, by adding a compliance check as a task to its build pipeline.

PrerequisitesTo customize a build pipeline, you must first [upgrade it](../proc_upgrade_build_pipeline/).

ProcedureTo customize the build pipeline in any way, start by completing the following steps:

1. In your preferred IDE, navigate to the `.tekton` directory in the repository of your component.
2. Open both `.yaml` files in the repository.
Changing parameters
-------------------

Procedure1. In each `.yaml` file in the `.tekton` directory, customize the parameters of the build pipeline by changing the pipeline `params`:


	1. Pipeline params have the paths `.spec.params` and `.pipelineSpec.params`
	2. Change the default `value` of existing parameters. For example, you can set the value of `image-expires-after` to `2w`, instead of `5d`
	3. Add parameters. New parameters must include a `name` and `value`.
2. Commit your changes to the repository of the component.
Extending the build pipeline with your own tasks
------------------------------------------------

Procedure1. In each `.yaml` file in the `.tekton` directory, add a new task under `tasks`.

Example task:


```
  name: example-task  params:  - name: example-param    value: “Example”  runAfter:  - build-container #You can be more specific by choosing another task  taskRef:    params:    - name: name      value: example-task # metadata.name field of the Task    - name: bundle      value: quay.io/tekton-bundle-catalog/example-task-bundle:1.0      # For more details on tekton bundles, refer https://tekton.dev/docs/pipelines/pipelines/#tekton-bundles    - name: kind      value: task    resolver: bundles  when:  - input: $(params.skip-checks)    #This references the pipeline parameters    operator: in    values:    - "false"
```
An example of a custom task added to the pipeline that sends a slack notification when the `Pipelinerun` fails:


```
  name: slack-webhook-notification  params:    - name: message      value: PipelineRun $(context.pipelineRun.name) failed    - name: secret-name      value: my-secret # name of secret in the your namespace which contains slack web-hook URL under key specified in 'key-name' parameter below    - name: key-name      value: dev-team  taskRef:    params:    - name: bundle      value: quay.io/redhat-appstudio-tekton-catalog/task-slack-webhook-notification:0.1    - name: name      value: slack-webhook-notification    - name: kind      value: Task    resolver: bundles  when:    - input: $(tasks.status)      operator: in      values: ["Failed"]
```
2. Commit your changes to the repository of the component.


|  | * To use `slack-webhook-notification` task, you need to create a secret in your namespace with at least one key where the value is the webhook URL. For example, to create a secret for Slack, run `oc create secret generic my-secret --from-literal dev-team=https://hooks.slack.com/services/XXX/XXXXXX` * If you want to define a task directly in this file, rather than using `taskRef`, you can use `taskSpec`. Visit the documentation linked in the [Additional resources](#additional-resources) section. |
| --- | --- |

Exchanging the build pipeline build task with higher memory limits
------------------------------------------------------------------

The `buildah` task, which builds components from a Dockerfile, has a memory limit of 4 GB. To build components with memory requirements greater than 4 GB, use the following tasks:

* [quay.io/redhat-appstudio-tekton-catalog/task-buildah-6gb](https://quay.io/repository/redhat-appstudio-tekton-catalog/task-buildah-6gb?tab=tags)
* [quay.io/redhat-appstudio-tekton-catalog/task-buildah-8gb](https://quay.io/repository/redhat-appstudio-tekton-catalog/task-buildah-8gb?tab=tags)
* [quay.io/redhat-appstudio-tekton-catalog/task-buildah-10gb](https://quay.io/repository/redhat-appstudio-tekton-catalog/task-buildah-10gb?tab=tags)
ProcedureTo exchange the build task with a memory limit of 6 GB, complete the following steps. For a memory limit of 8 or 10 GB, replace the references to 6 GB with the appropriate values.

1. Go to the GitHub repo of your component.
2. In each .yaml file in the .tekton directory, under tasks, locate the task named build-container:


	1. Under `.taskRef.params`, set `name` to `buildah-6gb`.
	2. Under `.taskRef.params`, set `bundle` to `quay.io/redhat-appstudio-tekton-catalog/task-buildah-6gb:0.1`.
Verification
------------

When you commit changes to these `.yaml` files in your repository, Konflux automatically triggers a new build. Wait for Konflux to complete the new build, then verify your changes have been made by following these steps:

1. Navigate to **Activity > Pipeline runs**.
2. Select the most recent build pipeline run.
3. In the **Details** tab, confirm that there are new tasks that you added in the pipeline visualization.
4. In the **Logs** tab, confirm the following:


	1. Any new tasks are in the navigation bar.
	2. If you changed a parameter’s value, and that value gets printed, the new value is in the log.
Troubleshooting
---------------

If you experience any issues with your customized pipeline, try the following solutions:

* If you believe that your desired parameter values are not being passed into the pipeline, make sure that your assignment of that value doesn’t get overwritten later in the `.yaml` file.
* If your new task is not appearing in the pipeline run, ensure the following:


	+ You added it to the correct place in the `.yaml` files, so that it has the path `.spec.params` or `.pipelineSpec.params`.
	+ You specified a valid `runAfter` field, and that the task in that field completed successfully.
* For problems with both parameters and tasks, make sure you committed your changes to the `.tekton` directory in the repository that Konflux references for the component.
* If your build pipeline can no longer successfully run, your best option is to simply rebuild the `.tekton` directory:


	+ Delete the `.tekton` directory in the repository of the component.
	+ In the Konflux console, on the **Overview** tab for the relevant application, scroll down and select **Manage build pipelines**.
	+ Select the three dots next to the relevant component and select **Roll back to default pipeline**.
	+ Complete the steps for [upgrading the build pipeline](../proc_upgrade_build_pipeline/) of that component again.
Additional resources
--------------------

* Visit the Tekton documentation that explainins [how to use `taskSpec`](https://tekton.dev/docs/pipelines/taskruns/#specifying-the-target-task) in a task declaration.
[Upgrading to a custom build pipeline](../proc_upgrade_build_pipeline/)[Creating secrets for your builds](../proc_creating-secrets-for-your-builds/)