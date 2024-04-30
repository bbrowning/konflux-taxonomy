Creating a `ReleasePlan` object
===============================

The development team creates a `ReleasePlan` object in the developer workspace. The `ReleasePlan` object includes a reference to the application that the development team wants to release, along with workspace where the application is supposed to be released.

**Prerequisites*** You have an existing Development workspace.
* Ensure you have installed `oc`.
* You have completed the steps listed in the [Getting started in the CLI](https://redhat-appstudio.github.io/docs.appstudio.io/Documentation/main/getting-started/getting_started_in_cli/) page.
**Procedures**1. Create a `ReleasePlan.yaml` object locally.

**Example `ReleasePlan.yaml` object**


```
apiVersion: appstudio.redhat.com/v1alpha1kind: ReleasePlanmetadata: labels:   release.appstudio.openshift.io/auto-release: 'true' name: sre-production **(1)** namespace: dev-workspace **(2)**spec: application: demo-app **(3)** data: <key> **(4)** pipelineRef: <pipeline_ref> **(5)** serviceAccount:  <service-account> **(6)** target: managed-workspace **(7)**
```


| **1** | The name of the release plan. |
| --- | --- |
| **2** | The development team’s workspace. |
| **3** | The name of the application that you want to deploy to the managed workspace. |
| **4** | Optional: An unstructured key used for providing data for the managed Pipeline. |
| **5** | Optional: Reference to the Pipeline to be executed by the release service. |
| **6** | Optional: The name of the service account to use in the Pipeline to gain elevated privileges. It’s used only if you have defined the `pipelineRef` value. |
| **7** | The workspace to which the system deploys the application. This workspace is created by the Managed environment team (for example, your organization’s SRE team) |
2. In the development workspace, apply the `ReleasePlan.yaml` file and add the resource to your cluster by running the following command:


```
$ oc apply -f ReleasePlan.yaml -n dev
```
**Verification**1. On the Trusted Application Pipeline console, select the **Release services** > **Release plan** tab.
2. Review the Release plan object that you just added. Using the Release plan tab, you can update or delete the selected Release plan object.
Next steps[Managed services team onboarding](https://redhat-appstudio.github.io/docs.appstudio.io/Documentation/main/how-to-guides/proc_managed_services_onboarding.adoc/)

[Releasing an application](../con_release_application/)[Managed services team onboarding](../proc_managed_services_onboarding/)