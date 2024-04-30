Managing a security fix for your application
============================================

Sometimes, you need to address an **embargoed security issue** in your application. So as not to disclose aspects of the security vulnerability prematurely, you will want to prepare a fix in private or with a limited set of collaborators. This document guides you on how to make a private copy of your git repository and clone your application to a private workspace where you can prepare a fix and invite other collaborators only on a need-to-know basis, so that you can control who is aware of the issue while you develop the fix.

Key steps include:

* **Clone affected application:** Cloning affected applications into a private workspace, enabling developers to tackle security issues without exposing sensitive information.
* **Prepare the fix:** Preparing the fix with source code in your private git mirror and builds in your private workspace.
* **Release the fix:** Releasing the build from your private workspace and "upstreaming" your patch from your private git mirror back to your team’s normal development repo.
Cloning applications to a private workspace
-------------------------------------------

Cloning an application involves replicating the application’s code and configuration into a dedicated private workspace, ensuring that sensitive information remains isolated and protected.

**Prerequisite*** You have the [maintainer role](#getting-started/roles_permissions/) or greater in the original workspace where the embargoed issue was identified.
* You have downloaded the [RHTAP CLI](https://github.com/redhat-appstudio/rhtap-cli/releases).
**Procedure**1. Create a [Private Mirror](https://docs.github.com/en/repositories/creating-and-managing-repositories/duplicating-a-repository) of the corresponding repository for any components that will receive fixes related to embargoed information. This step is crucial to safeguard sensitive data and prevent unauthorized access.



|  | Creating a private fork of the public [GitHub repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/duplicating-a-repository) is not possible. |
| --- | --- |
2. [Submit a request for a new workspace](../../managing-workspaces/proc-creating_a_team_workspace/) dedicated to work on the embargoed issue. This workspace will serve as the private environment for cloning the affected application. Don’t expose information about the vulnerability in your choice of a name for the workspace. If you had previously created a private workspace and is no longer in use for another embargoed process, you can re-use it as long as you re-restrict the [User Access](https://console.redhat.com/preview/application-pipeline/access) appropriately. Your personal workspace can also be used; make sure to review User Access.
3. Log in to the original workspace where the application was previously being developed using the `oc` CLI tool. (See [Getting started with CLI](#getting-start/getting_started_in_cli/).) Append `/workspaces/<original-tenant-workspace>` to the AppStudio API url used in the `oc login` command to target a particular workspace other than your default user workspace.
4. To export records the application from the original workspace with details changed to refer to your new private workspace, run the following command:


```
./rhtap export application <name_of_your_application>  --from <original-tenant-workspace> --to <private-workspace> --as-prebuilt-images --skip <impacted component git url>
```


|  | Ensure that you have excluded the impacted component from which you have created a private mirror in step 1. |
| --- | --- |
5. Confirm that the YAML file has been generated under the `./data` directory. This file contains the necessary information for importing the application into the new workspace.
6. Log in to the newly created private workspace using the `oc` CLI tool. Append `/workspaces/<private-workspace>` to the AppStudio API url used in the `oc login` command to target the new private workspace.
7. Apply the generated YAML file to the new private workspace by using the following command:


```
oc apply -f ./data/<path-to-yaml>
```
8. Within the RHTAP UI, in the private workspace, import the private mirror as a new component in the application that you just created in step 7.
At this point, you should have a clone of your application in the new private workspace, with all of its components mirrored from the original workspace, except the impacted component, which is now linked to the new private Git mirror repository.

Preparing the security fix
--------------------------

**Prerequisite*** You have cloned your application to a private workspace and have replaced the impacted component with a private mirror.
**Procedure**1. Verify that pull requests to your private mirror create PipelineRuns in the private workspace and that integration tests run correctly.
2. Prepare the fix to your security issue as a pull request against your private mirror.
3. Invite reviewers from your security department or select members from your team to review the patch and confirm that it fixes the embargoed security issue, by [granting them collaborator rights in your workspace](https://redhat-appstudio.github.io/docs.appstudio.io/Documentation/main/getting-started/get-started/#adding-collaborators-to-your-workspace).
4. When you are satisfied that the fix is ready, wait until the embargo disclosure time before releasing your fix.
Releasing the security fix
--------------------------

**Prerequisite*** You have prepared a fix in a private git mirror and private workspace.
* You have reviewed the fix with representatives from your security department and select members of your team on a need-to-know basis.
* The date for lifting the embargo has arrived.
**Procedure**1. In the private workspace, use the UI to identify the pullspec of the image bearing the fix, pinned to digest.
2. In your team’s normal workspace (not the private workspace), use the CLI to identify a `Snapshot` that you want to use as a basis for your new release. A common choice is "the most recently released Snapshot", which you can find by picking through your history of Releases sorted by creation date to find the relevant Snapshot identifier.
3. Use `oc` to extract the Snapshot that you want to use as a basis for your new release to a local yaml file with `oc get snapshots <that snapshot id> -o yaml > snapshot.yaml`
4. Edit the extracted file to construct a new `Snapshot` that replaces the impacted components pullspec with the pullspec of the image bearing the fix, pinned to digest. You can discard all annotations and labels and you should give the Snapshot a new `name`.
5. Create that new Snapshot in the system with `oc apply -f snapshot.yaml`.
6. Review your integration test pipelines to confirm that the `Snapshot` is valid and can be released.
7. Create a `Release` resource referencing the specified `Snapshot`. Follow a similar procedure as outlined above. Export the existing `Release` as a starting point. Modify it to reference the new `Snapshot` and make any necessary adjustments.
8. In your team’s normal workspace (not the private workspace), use the UI to watch the progress of the `Release`. When completed, your fix is live and available to your customers.
9. Extract the commit(s) from your private mirror and apply them back to the main Git repository used by your team for normal development.


|  | Ensure to apply the patch(es) from your private mirror to the Git repository that your team normally uses for managing development. Failure to do so results in security regressions in subsequent releases from your team. |
| --- | --- |



|  | It is possible that during the time that the issue is under embargo, other changes have been merged in the other components of your application. Those changes are built and integrated in your team’s original workspace, but the components in the new private workspace are pinned to old versions of your components. They do not rebuild as new changes are merged. This is due to the `--as-prebuilt-images` flag you passed to the `rhtap export …​` command. In order to ensure that your in-progress change will work with the latest state of your application during development, you may want to periodically re-export the components from your original workspace and re-apply them to your private workspace in order to test that your in-progress change continues to work against the latest revision of the other components. |
| --- | --- |

[Creating your own environment](../../managing-environments/proc_creating_your_own_environment/)[Creating a team workspace](../../managing-workspaces/proc-creating_a_team_workspace/)