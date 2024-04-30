Preventing redundant rebuilds
=============================

After you upgrade the build pipeline for a component, Konflux rebuilds the component when new pull requests (PRs) include changes to that component. This behavior helps you identify any issues the PR might cause before merging it.

By default, Konflux configures upgraded pipelines to rebuild a component *only* if a PR includes changes to that component. This configuration prevents redundant rebuilds in repositories that contain multiple components.

However, depending on the structure of your repository and the dependencies of your component, you may want to adjust the default configuration for rebuilds to better suit your needs. In particular, the default configuration might still rebuild a component too often. You can change this behavior by editing the `on-cel-expression` annotation.

ProcedureTo prevent redundant rebuilds of a component, complete the following steps.

1. Using your preferred IDE, in the repository of your component, open the `/.tekton/<name of component>-on-pull-request.yaml` file and find the`on-cel-expression` annotation.

Example:


```
pipelinesascode.tekton.dev/on-cel-expression: event == "pull_request" && target_branch      == "main" && ( "my-component/***".pathChanged() || ".tekton/my-component-sample-pull-request.yaml".pathChanged()      || "root-docker/Dockerfile".pathChanged() )
```
2. Set the value as the path or paths that you want to trigger rebuilds. PRs with changes to files in those paths will cause Konflux to rebuild the component.

Example:


```
pipelinesascode.tekton.dev/on-cel-expression: event == "pull_request" && target_branch      == "main" && ( "my-component/context/***".pathChanged() || ".tekton/my-component-pull-request.yaml".pathChanged()      || "root-docker/Dockerfile".pathChanged() )
```


|  | Misconfiguring this value can prevent builds from starting or cause them to start at the wrong time. |
| --- | --- |
3. Commit the changes.
4. Wait for Konflux to rebuild your component.
VerificationTo verify that you have prevented redundant rebuilds:

1. Open a PR that modifies the component that you want Konflux to rebuild.
2. Wait for Konflux to rebuild your component.
3. Check the PipelineRuns page in Konflux. There should be only one new PipelineRun with the type as “Build.” Check its logs for the `build-container` task. They should only refer to the component you specified with `on-cel-expression`.
TroubleshootingIf Konflux continues to rebuild your whole application for each new PR:

* Make sure you entered the right path as the value for `on-cel-expression`.
* Make sure the logical operators between conditions in `on-cel-expression` are correct. For example, did you accidentally replace || with &&?
* Make sure you merged the commit that changes `on-cel-expression`.
If builds are failing to start:

* Try the previously listed troubleshooting items.
* If those ideas do not work, use `git revert` to restore your pipeline definition to its original state.
If builds are starting at the wrong time:

* For any component whose builds are starting at the wrong time, ensure that its `on-cel-expression` excludes all paths in the repo that are not associated with that component.
[Defining component relationships](../proc_defining_component_relationships/)[Overview of Konflux tests](../../testing_applications/con_test-overview/)