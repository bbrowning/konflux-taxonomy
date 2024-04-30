Managing multiple software versions
===================================

Software projects are often required to maintain multiple versions of thesoftware in parallel in order to support different users of the software withdifferent needs. As far as source code goes, the typical way to maintainmultiple versions is by using different Git branches. Using branches inconjunction with Konflux can be somewhat tedious as a separate Component needsto be defined for each branch and a separate Application needs to be definedfor each collection of components that need to be tested and released together.

The Konflux Project Controller seeks to streamline the process of managingmultiple versions by introducing the following objects and concepts:

* A **Project** is used to describe a major piece of software that can be workedon by multiple teams over an extended period of time. A project may containone or more development streams.
* A **ProjectDevelopmentStream** indicates an independent stream of development.A **ProjectDevelopmentStream** can contain one or more **Applications** eachcontaining one or more **Components**.
* As described above, starting a new development stream involves creating alarge amount of **Application** and **Component** resources. The ProjectController helps to streamline that by allowing to create a**ProjectDevelopmentStreamTemplate** resource that specifies the resources to becreated and allows for using variables to customize them. Using a template,many similar development streams can be created quickly.
Using the Project Controller
----------------------------

In the sections below we will describe how to use the custom resourcessupported by the Project Controller to manage multiple software versions andgenerate Application and Component resources.

### Before you begin

It’s possible to have the Project Controller create all the Application andComponent resources you would need. It is recommended, however, for the firsttime a particular repository is on-boarded, to do so manually via the KonfluxUI. That would help ensuring the right access credentials are in place as wellas that the Tekton Pipeline-as-Code files are committed to the repo.

When creating components the Project Controller assumes that:

* The default pipeline is not being used and that each branch in a component’srepo contains the necessary Tekton Pipeline-as-Code files to build it.
* Any credentials required to access the component repo had already beenconfigured as secrets in the Konflux workspace.
### Creating a Project

Create a project resource by applying YAML like the following:

project.yaml
```
apiVersion: projctl.konflux.dev/v1beta1kind: Projectmetadata:  name: konflux-multibranch-samplespec:  displayName: "Multi-version demonstration sample project"  description: |    A sample project to demonstrate how to use the projects API.
```
### Creating a ProjectDevelopmentStreamTemplate

To enable quickly creating multiple development streams, we must create atemplate for them.

template.yaml
```
apiVersion: projctl.konflux.dev/v1beta1kind: ProjectDevelopmentStreamTemplatemetadata:  name: konflux-multibranch-sample-templatespec:  project: konflux-multibranch-sample  variables:  - name: version    description: A version number for a new development stream  - name: versionName    description: A K8s-compliant name for the version    defaultValue: "{{hyphenize .version}}"  resources:  - apiVersion: appstudio.redhat.com/v1alpha1    kind: Application    metadata:      annotations:        application.thumbnail: "5"        finalizeCount: "0"      finalizers:      - spi.appstudio.redhat.com/remote-secrets      - application.appstudio.redhat.com/finalizer      name: "konflux-multibranch-sample-{{.versionName}}"    spec:      displayName: "konflux-multibranch-sample-{{.versionName}}"  - apiVersion: appstudio.redhat.com/v1alpha1    kind: Component    metadata:      annotations:        applicationFailCounter: "0"      finalizers:      - test.appstudio.openshift.io/component      - component.appstudio.redhat.com/finalizer      - image-controller.appstudio.openshift.io/image-repository      - image-registry-secret-sa-link.component.appstudio.openshift.io/finalizer      - pac.component.appstudio.openshift.io/finalizer      name: konflux-multibranch-sample-{{.versionName}}    spec:      application: "konflux-multibranch-sample-{{.versionName}}"      componentName: "konflux-multibranch-sample-{{.versionName}}"      source:        git:          context: ./          dockerfileUrl: Dockerfile          revision: "{{.version}}"          url: https://github.com/ifireball/konflux-multibranch-sample.git
```
The **resources** section for the template may be created by looking at the YAMLfor existing resources and copying it while removing generated and unnecessarydata and adding variable references where needed.

Here are specific examples for how to clean up and use the YAML for certainresource kinds:

* For any kind of resource, the `namespace`, `creationTimestamp`, `generation`,`resourceVersion`, `uid` and `ownerReferences`, metadata fields should beremoved as well as the `status` section.
* For **Application** resources the `metadata.name` and `spec.displayName` fieldsshould contain variable references.
* For **Component** resources:


	+ The following annotations should be removed:
	
	
		- `build.appstudio.openshift.io/status`
		- `image.redhat.com/image`
	+ The `spec.containerImage` field should be removed.
	+ The following fields should probably contain variable references:
	
	
		- `spec.application`
		- `spec.componentName`
		- `source.git.revision`
Some notes about using template variables:

* You can use the [Go text/template](https://pkg.go.dev/text/template) syntax toplace template variable values into various resource attributes as well asvariable default values.
* You can use the custom `hyphenize` template function to create a valuesuitable for use in resource names.
* It’s advisable to quote strings that contain variable references and othertemplate syntax elements to prevent the curly braces from being parsed as JSONembedded into YAML.
### Creating a ProjectDevelopmentStream

Once the **Project** and **ProjectDevelopmentStreamTemplate** resources are inplace, we can create **ProjectDevelopmentStream** resources.

devstream.yaml
```
apiVersion: projctl.konflux.dev/v1beta1kind: ProjectDevelopmentStreammetadata:  name: konflux-multibranch-sample-v1-0-0spec:  project: konflux-multibranch-sample  template:    name: konflux-multibranch-sample-template    values:    - name: version      value: "v1.0.0"
```
Creating this **ProjectDevelopmentStream** resource will cause the resourcesspecified by the referenced **ProjectDevelopmentStreamTemplate** resource to getcreated. Since we’ve used the `version` template variable in the`spec.git.revision` field of the component resources, each component versionwill use a different branch of the component repository.

### Branching your component repositories

Beyond creating new Git branches for your components in order to maintaindifferent versions, you must also adjust the `.tekton/*.yaml` files within thosebranches in order to make the pipelines run and target the right components.

In particular the following changes must be made each time a new branch iscreated in each of the pipeline YAML files:

* The `pipelinesascode.tekton.dev/on-cel-expression` annotation should beadjusted to specify and filter by the right branch name. For example, for apull request pipeline that resides in the `v1.0.0` branch the annotation valuewould be:


```
event == "pull_request" && target_branch == "v1.0.0"
```
For a push pipeline in the same branch the value would be:


```
event == "push" && target_branch == "v1.0.0"
```
* The `appstudio.openshift.io/application` and`appstudio.openshift.io/component` labels must be adjusted to specify theright Application and Component respectively. Failing to do this will causebuilds of the pipeline to be associated with the wrong application orcomponent.
Known limitations
-----------------

The following limitations exist in the current controller implementation and arelikely to be resolved in the future.

* Resource creation order is important. You must first create **Project**resources followed by **ProjectDevelopmentStreamTemplate** resources and onlythen **ProjectDevelopmentStream** resources.
* If a **ProjectDevelopmentStreamTemplate** is modified, resources that werealready created using that template do not get updated unless either:


	+ The controller gets restarted
	+ The **ProjectDevelopmentStream** resource referring to the template is modified
* If a resource created by a template is modified, the configuration is notaligned back with the template unless either:


	+ The controller gets restarted
	+ The **ProjectDevelopmentStream** resource referring to the template ismodified
* A **ProjectDevelopmentStream** that isn’t referring a template may be modifiedto refer to a template. Similarly, the template **ProjectDevelopmentStream** isreferring to may be changed. In both those cases, resources owned by the**ProjectDevelopmentStream** but not defined by the new template do not getdeleted.
[Deleting an application](../proc_delete_application/)[Supply chain security through SLSA conformity](../../concepts/slsa/con_slsa-conformity/)