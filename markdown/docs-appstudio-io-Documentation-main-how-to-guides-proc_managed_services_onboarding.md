Managed services team onboarding
================================

The Managed Environment team creates the following objects on the Managed workspace:

* **ReleasePlanAdmission** - The Managed Environment team creates or updates the `ReleasePlanAdmission` object in response to the `ReleasePlan` object created by the development team. It indicates that the Managed Environment team has approved the application specified in the [ReleasePlan](https://redhat-appstudio.github.io/docs.appstudio.io/Documentation/main/how-to-guides/proc_release_plan/) object.
* **`copy-application.sh`** - The Managed Environment team runs the `copy-application.sh` script by defining the application name before releasing an application to production. The script copies the application and all of its components from the Development to the Managed workspace. As a result, when releasing an application to production, the Managed Environment team uses the application on its workspace rather than the one on the Developer workspace.Additionally, if the Development team adds a new component to the application on their workspace, they must notify the Managed Environment team. So they can run the `copy-application.sh` script again to ensure that the managed workspace has the most recent version of the application.
Creating a `ReleasePlanAdmission` object
----------------------------------------

**Prerequisites*** An existing Development and Managed workspace.
* An existing `ReleasePlan` object in the Development workspace.
**Procedures**1. Create a `ReleasePlanAdmission.yaml` object locally.

**Example `ReleasePlanAdmission.yaml` object**


```
apiVersion: appstudio.redhat.com/v1alpha1kind: ReleasePlanAdmissionmetadata: name: sre-production **(1)** namespace: managed-workspace **(2)**spec: applications:  - demo-app **(3)** data: <key> **(4)** environment: <sre-production> **(5)** origin: <dev-workspace> **(6)** pipelineRef: <pipeline_ref> **(7)** policy: <policy> **(8)** serviceAccount: <service-account> **(9)**
```


| **1** | The name of the release plan admission. |
| --- | --- |
| **2** | The Managed environment team’s workspace. |
| **3** | A list of applications that you want to enable to be deployed in the managed workspace. |
| **4** | Optional: An unstructured key used for providing data for the managed Pipeline. |
| **5** | Optional: The environment from which the application updates are allowed to be received in the Managed workspace. This environment is created by the Development team. |
| **6** | The development team workspace where the application is defined. |
| **7** | Reference to the Pipeline to be executed by the release service. |
| **8** | The enterprise contract policy against which the system validates an application before releasing it to production. |
| **9** | Optional: The name of the service account to use in the Pipeline to gain elevated privileges. It’s used only if you have defined the `pipelineRef` value. |



|  | The ReleasePlanAdmission.yaml represents the reciprocal link to the ReleasePlan.yaml objects created by the development team. |
| --- | --- |
2. In the Managed workspace, apply the `ReleasePlanAdmission.yaml` file and add the resource to your cluster by running the following command:


```
oc apply -f ReleasePlanAdmission.yaml -n managed
```
**Verification**1. On the Trusted Application Pipeline console, select the **Release services** > **Release plan admission** tab.
2. Review the Release plan admission object that you just added. Using the Release plan admission tab, you can update or delete the selected Release plan object.
The `copy-application.sh` script
--------------------------------

**Prerequisites*** An existing Development and Managed workspace.
* Download [./copy-application.sh](https://github.com/redhat-appstudio/release-service-utils/blob/main/copy-application.sh) script.
**Procedures*** Run the following command to copy the application from the development workspace to the managed workspace:


```
./copy-application.sh <managed workspace name> -a <development workspace name>/<application name>
```
To show the command usage information, run the `./copy-application.sh --help` command.
[Creating a `releasePlan` object](../proc_release_plan/)[Deleting an application](../proc_delete_application/)