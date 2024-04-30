Enabling hermetic builds
========================

A hermetic build is a secure, self-contained build process that doesn’t depend on anything outside of the build environment. This means that it does not have network access, is not vulnerable to external influences, and cannot fetch dependencies at run time. Instead, you must declare all required resources and dependencies in your build definition.

In Konflux, you can block network access to the build process and run a hermetic build by setting the `**hermetic**` parameter in your pipeline definition file to `true`. This means that you must fetch all dependencies *before* the build can start. The following is an example code snippet:


```
kind: PipelineRunspec:  params:    ...  - name: hermetic    value: "true"    ...
```


|  | * Hermetic builds disable network access, so a build with dependencies outside of its Git repository—​including supported languages—​might fail. To prevent this, or to pull in dependencies from a package manager for one of the [supported languages](../proc_prefetching-dependencies-to-support-hermetic-build/#supported-languages), follow the instructions in [Prefetching the package manager dependencies for the hermetic build](https://redhat-appstudio.github.io/docs.appstudio.io/Documentation/main/how-to-guides/proc_prefetching-dependencies-to-support-hermetic-build/).Similarly, with a [Buildah](https://github.com/redhat-appstudio/build-definitions/blob/main/task/buildah/0.1/buildah.yaml) task for a non-Java application, when you set the `**hermetic**` parameter to `true`, you’re isolating the build from the network, which restricts it to building only from dependencies listed in your Git repository. * Do not add these parameters to the [`**pipelineSpec.params**`](https://github.com/burrsutter/partner-catalog-stage/blob/e2ebb05ba8b4e842010710898d555ed3ba687329/.tekton/partner-catalog-stage-wgxd-pull-request.yaml#L87) section, as it should always display the default values for hermetic builds. |
| --- | --- |

Prerequisites* You have an [upgraded build pipeline](https://redhat-appstudio.github.io/docs.appstudio.io/Documentation/main/how-to-guides/configuring-builds/proc_upgrade_build_pipeline/).
ProcedureTo create a hermetic build for a component, complete the following steps:

1. Go to the `.tekton` directory in your component’s repository and find the `.yaml` files related to your `**pull request**` and `**push**` processes.
2. To configure the hermetic pipeline in both the `.yaml` files, add the following hermetic pipeline parameters to the `spec.params` section:


```
spec:    params:        -   ...        -   name: hermetic            value: "true"
```
3. Commit your changes to the component repository and create a pull request.
4. Verify that your build was successful, then merge your pull request.
Verification* From the Konflux **Applications** view, go to **Activity > Pipeline runs**.


	+ Look at the pipeline run with **Build** in the **Type** column and confirm that the `build-container` stage displays a green checkmark. This indicates that the build process successfully fetched all dependencies.
* From the Konflux **Applications** view, go to **Activity > Latest commits**.
TroubleshootingIf your build fails, be sure to look at your logs:

In Konflux, from the **Applications** view, select the application build you want to troubleshoot, then from the resulting **Overview** page, select the **Activity** tab. From there, under **Activity By**, select **Pipeline runs**. From the **Name** column, select the build whose logs you want to check, then from the resulting **Pipeline run details** view, do one of the following:

* Select the **Logs** tab.
* Alternatively, you can click **build-container**. When the right panel opens, select the **Logs** tab to see a partial view of the log for that build.
Additional resources
--------------------

For more information about the importance of provenance, see [Supply chain security through SLSA conformity](https://redhat-appstudio.github.io/docs.appstudio.io/Documentation/main/concepts/slsa/con_slsa-conformity/).

[Configuration as Code](../configuration-as-code/proc_configuration_as_code/)[Prefetching package manager dependencies for hermetic build](../proc_prefetching-dependencies-to-support-hermetic-build/)