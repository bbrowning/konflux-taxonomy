Getting started with CLI
========================

In addition to the user interface (UI), you can also use the command line interface (CLI) to access and configure Konflux to meet your specific needs.

PrerequisitesTo access Konflux with the CLI, you must configure `oc` commands. Follow the instructions in [Getting started with the OpenShift CLI](https://docs.openshift.com/container-platform/4.12/cli_reference/openshift_cli/getting-started-cli.html).

ProcedureTo log in to Konflux by using the CLI, complete the following steps:

1. Navigate to the [OpenShift Developer Sandbox](https://registration-service-toolchain-host-operator.apps.stone-prd-host1.wdlc.p1.openshiftapps.com/).
2. Select the checkbox next to **I agree to the Terms and Conditions**.
3. Select **Get started with OpenShift Developer Sandbox**.
4. In the webpage banner, select **Proxy login command**.
5. Click the **copy icon** to copy the command and your unique token.
6. Open your terminal and paste the command that you copied in the previous step. This command runs `oc login --token=[your token] [appstudio api url]`.
VerificationTo verify that `oc login` worked correctly, complete the following steps:

1. Run `cd ~/.kube`.
2. Run `ls` and verify that there is a file named `config`.
Switching workspaces
--------------------

To use the CLI tool with a workspace other than your default personal workspace, append `/workspaces/<workspace-name>` to the AppStudio API url used in your `oc login` command in step 6.

oc commands for Konflux
-----------------------

The following list contains common `oc` commands and examples of their outputs, where relevant:

### oc get application

Example output:


```
NAME     AGE   STATUS   REASONmy-app   15s    True      OK
```
### oc get components

Example output:


```
NAME                                        AGE   STATUS   REASON   TYPEdevfile-sample-java-springboot-basic-mhqg   50s   True     OK       GitOpsResourcesGenerated
```
### oc get routes

Example output:


```
NAME    HOST/PORT                     PATH  SERVICES                   PORT    TERMINATION     WILDCARDmy-app  myapp-my-namespace.yourserver  /    single-container-app-7g2w  8080    edge/Redirect   None
```
### oc get environments

Example output:


```
NAME          AGEdevelopment   2d19h
```
### oc get snapshot

Example output:


```
NAME           AGEmy-app-ggkxt   153m
```
### oc get pipelinerun

Example output:


```
NAME                                              SUCCEEDED   REASON      STARTTIME   COMPLETIONTIMEdevfile-sample-java-springboot-basic-mhqg-mnwx6   True        Completed   9m30s       6m46s
```
### oc get taskrun

Example output:


```
NAME                                                              SUCCEEDED   REASON      STARTTIME   COMPLETIONTIMEdevfile-sample-java-springboot-basic-mhqg-mnwx6-build-container   True        Succeeded   11m         9m45sdevfile-sample-java-springboot-basic-mhqg-mnwx6-init              True        Succeeded   12m         12mdevfile-sample-java-springboot-basic-mhqg-mnwx6-show-summary      True        Succeeded   9m42s       9m34sdevfile-sample78ef7b0924ed3b025289a33d98b0e1f4-clone-repository   True        Succeeded   12m         11m`
```
### oc get gitopsdeployment

Example output:


```
NAME                                                                                            SYNC STATUS   HEALTH STATUSmy-app-development-binding-g7m54-my-app-development-devfile-sample-java-springboot-basic-mhqg   Synced        Healthy
```
### oc get deployment

Example output:


```
NAME                                                                                            SYNC STATUS   HEALTH STATUSmy-app-development-binding-g7m54-my-app-development-devfile-sample-java-springboot-basic-mhqg   Synced        Healthy
```
### oc create

### oc create secret

### oc get service [name]

Example output:


```
NAME                                        TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGEdevfile-sample-java-springboot-basic-mhqg   ClusterIP   172.30.23.168   <none>        8081/TCP   10d
```
### oc logs [-f] [-p] (POD | TYPE/NAME) [-c CONTAINER]

### oc get pods

Example output:


```
NAME                                                              READY   STATUS      RESTARTS   AGEdevfile-sample-java-springb8214c8b0443987b4d7705b3830fa823e-pod   0/6     Completed   0          13mdevfile-sample-java-springbf2e030e1f22f1d5a7be9e9c899eaaf25-pod   0/1     Completed   0          11mdevfile-sample-java-springboot-basic-mhqg-798c5845bd-sxfxt        1/1     Running     0          5m19sdevfile-sample-java-springboot-basic-mhqg-mnwx6-init-pod          0/1     Completed   0          13mdevfile-sample78ef7b0924ed3611ba7cdef4a1f702c76765753714be6-pod   0/1     Completed   0          13m
```
### oc get pods -l '!tekton.dev/memberof'

Example output:


```
NAME                                                              READY   STATUS      RESTARTS   AGEdevfile-sample-java-springb8214c8b0443987b4d7705b3830fa823e-pod   0/6     Completed   0          13mdevfile-sample-java-springbf2e030e1f22f1d5a7be9e9c899eaaf25-pod   0/1     Completed   0          11mdevfile-sample-java-springboot-basic-mhqg-798c5845bd-sxfxt        1/1     Running     0          5m4sdevfile-sample-java-springboot-basic-mhqg-mnwx6-init-pod          0/1     Completed   0          13mdevfile-sample78ef7b0924ed3611ba7cdef4a1f702c76765753714be6-pod   0/1     Completed   0          13m
```
[Getting started with Konflux](../get-started/)[Importing and configuring code](../../how-to-guides/Import-code/proc_importing_code/)