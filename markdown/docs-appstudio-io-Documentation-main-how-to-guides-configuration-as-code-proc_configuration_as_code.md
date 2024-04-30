Configuring Applications and Components as Code with Kustomize
==============================================================

If you want to define a large application with many components, easily duplicate or update components, or ensure consistent component and application states - you may want to configure your Konflux Application(s) and Component(s) as Code through Kustomize. This document will overview a basic application and component configuration that can be replicated and duplicated through the use of Kustomize bases and overlays. You can learn more about Kustomize [here](https://kustomize.io/). This document is roughly based on the configuration defined in [this repository](https://github.com/konflux-ci/casc-gpt) and you can see the configuration first-hand there!

Key steps include:

1. **Create a basic file structure for your bases and overlays:** Preparing a space and structure for your Application and Component Bases and Overlays.
2. **Create a Base for your Components:** Preparing a base which contains all of the default or common values for every component you’ll create.
3. **Create a Base for your Application:** Preparing a base which contains all of the default or common values for every Application you’ll create.
4. **Create an Overlay for every Component:**  Preparing an overlay that patches in component-specific data for every component in your Application.
5. **Create an Overlay for your Application:** Preparing an overlay that patches in specific data for each application you want to create.
6. **Create patches for Application-specific Component Configurations:** Preparing Application-specific patches for all components in a given Application and accomodating variations in specific patches.
7. **Bonus - Duplicating or expanding your Application:** A discussion of the general philosophy of Configuration-as-Code and how to extend, duplicate, or customize your Application, Components, and Workspace as Code.


|  | Throughout this document, substitute your application and component names for placeholder values like `application-a`, `application-a`, `component-a`, etc. |
| --- | --- |

Create a File Structure
-----------------------

As with many Kustomize projects, we’ll need a space to define a `base` and some `overlay`(s). Within our `overlay`(s), we’ll also define a folder for a base *set* of components and a folder for each application-specific overrides for that base set of components.

Create a file structure as follows:


```
├── base│   ├── component.yaml│   └── kustomization.yaml├── overlay│   └── application-a│       ├── base│       │   ├── application.yaml│       │   ├── component-a│       │   │   ├── component-a-override.yaml│       │   │   └── kustomization.yaml│       │   ├── component-b│       │   │   ├── component-b-override.yaml│       │   │   └── kustomization.yaml│       │   └── kustomization.yaml│       └── v1-overlay│           ├── application-patch.yaml│           ├── component-patch.yaml│           ├── exception-component-patch-1.yaml│           └── kustomization.yaml└── README.md
```


|  | You can omit `component-b` if you only wish to define a single component. This was included for illustration. |
| --- | --- |

In this file structure, you will find:. `base`: which is a directory housing your base component yaml and a kustomize to point to the base.. `overlay`: which contains one or more application variants, useful when defining multiple different applications.. `overlay/application-a/base`: a base which defines one or more component overrides, one per component in the application and a base for your application.. `overlay/application-a/v1-overlay`: An override for your application and an application specific patches for your component(s).

Create a Base for your Components
---------------------------------

If you are creating more than one component, its likely that your components will share some, if not most, of their configuration. These default or global values can be defined in the Base component and overridden on a case-by-case basis in your Component overlays.

### Creating your Base Component

You’ll define this base in `base/component.yaml`. It typically follows a pattern similar to the following:


```
apiVersion: appstudio.redhat.com/v1alpha1kind: Componentmetadata:  annotations:    image.redhat.com/generate: "true"    appstudio.openshift.io/pac-provision: request    build.appstudio.openshift.io/request: configure-pac  name: example-componentspec:  componentName: example-component  application: appName  targetPort: 8080  source:      git:        url: gitUrl        context: ./        dockerfileUrl: ContainerFileLocation        revision: defaultBranch
```


|  | This will create a component with a custom build pipeline. If you wish to use the default build, omit the `build.appstudio.openshift.io/request: configure-pac` annotation. |
| --- | --- |

### Creating your Base Kustomization

With our base component defined, we need to tell Kustomize it exists, for later consumption in overlays, so we’ll set up a basic `base/kustomization.yaml` as follows:


```
apiVersion: kustomize.config.k8s.io/v1beta1kind: Kustomizationresources:  - component.yaml
```
Create a Base for your Application
----------------------------------

Each Application will have its own base and one or more overrides.

You can think of each application "variant" as the base that defines the structure of your application and all components in that application and the concrete application as an "implementation" of that variant that defines any differentiating specs such as application name, version, and component branches.

Create your base application at `overlay/application-a/application-a-base/application.yaml` like the following:


```
apiVersion: appstudio.redhat.com/v1alpha1kind: Applicationmetadata:  name: basespec:  description: base  displayName: base
```
and its Kustomization file at `overlay/application-a/application-a-base/kustomization.yaml`:


```
apiVersion: kustomize.config.k8s.io/v1beta1kind: Kustomizationresources:  - application.yaml
```
Create an Overlay for every Component
-------------------------------------

For each application, we need define every component in said application as an overlay. These overlays should contain all component-specific information that is *consistent across all versions of the application* in the case that you’ll have more than one version of that application.

For example, you’ll typically have more than one version defined if you’re developing a versioned operator and have consistent component names across every version of an application, but different branches (this is the OpenShift / OpenShift CI Model with release-versioned branches).

We’ll define these components as folders in `overlay/application-a/base`. Each folder should be named after its component name, ex. `component-a`, and contain and `override.yaml` and `kustomization.yaml` that look like:

`overlay/application-a/base/component-a/component-a-override.yaml` (replacing name, URL, and Dockerfile):


```
- op: replace  path: /metadata/name  value: component-a-name- op: replace  path: /spec/componentName  value: component-a-name- op: replace  path: /spec/source/git/url  value: https://myvcs.com/myorg/component-a- op: replace  path: /spec/source/git/dockerfileUrl  value: "Dockerfile"
```
`overlay/application-a/base/component-a/kustomization.yaml`:


```
apiVersion: kustomize.config.k8s.io/v1beta1kind: Kustomizationresources:  - ../../../../base # Path to base componentpatches:  - path: component-a-override.yaml # Path to Override File    target:      kind: Component
```


|  | You can repeat this pattern for every component in your application. |
| --- | --- |

Create an Overlay for your Application and Application-specific Component Configuration
---------------------------------------------------------------------------------------

For each version or variant of your application as configured in the prior steps, you’ll define an application overlay and any additional application-specific component patches.

We’ll version this concrete application and set of patches in its own overlay folder in the application folder, in our case `overlay/application-a/v1-overlay` which will hold:

1. `application-patch.yaml`: our application overlay
2. `component-patch.yaml`: a version-specific patch for all components, typically a branch name
3. `exception-component-patch.yaml`: an example version-specific patch for a specific component or set of components
4. `kustomization.yaml`: a kustomization file that defines how the patches are applied to components
Let’s start with our `application-patch.yaml` at `overlay/application-a/v1-overlay/application-patch.yaml` (replacing values with your own):


```
- op: replace  path: /metadata/name  value: application-a-v1- op: replace  path: /spec/description  value: "Pipeline for application-a v1"- op: replace  path: /spec/displayName  value: "application-a v1"
```
Followed by our override for components at `overlay/application-a/v1-overlay/component-patch.yaml`:


```
- op: replace  path: /spec/application  value: application-a-v1 # Must match /metadata/name in application-patch.yaml- op: replace  path: /spec/source/git/revision  value: release-v1 # Replace with your target branch for all components
```
If you have any patches specific to this application revision that only impact a certain component or set of components, you can define another patch as defined in `overlay/application-a/v1-overlay/exception-component-patch-1.yaml`:


```
- op: replace  path: /spec/source/git/revision  value: main # In this example, one of our components will build off of main, so we have to set it in a separate patch.
```
and finally we can set up our `overlay/application-a/v1-overlay/kustomization.yaml` to apply these patches correctly:


```
apiVersion: kustomize.config.k8s.io/v1beta1kind: KustomizationnameSuffix: v1 # Add a suffix to all resource names in the application for uniquenessresources:  - ../basepatches:  - target:      kind: Application    path: application-patch.yaml  - target:      kind: Component    path: component-patch.yaml  - target:      kind: Component      name: component-b    path: exception-component-patch-1.yaml
```


|  | This kustomizaton applies a suffix to all resources, we recommend doing this to ensure uniqueness and make it easier to identify components and applications. |
| --- | --- |



|  | You can define more than one exceptional patch and match component names through regex. |
| --- | --- |

Defining Multiple Versions or Variants of an Application
--------------------------------------------------------

If multiple versions of an application exist (as in versioned operators) or variants of applications that share some or all components, you can define multiple application overlays following the same pattern as above.

This will result in a configuration that looks something like the following, with a folder for each version.


```
├── base│   ├── component.yaml│   └── kustomization.yaml├── overlay│   └── application-a│       ├── base│       │   ├── application.yaml│       │   ├── component-a│       │   │   ├── component-a-override.yaml│       │   │   └── kustomization.yaml│       │   ├── component-b│       │   │   ├── component-b-override.yaml│       │   │   └── kustomization.yaml│       │   └── kustomization.yaml│       ├── v1-overlay│       │   ├── application-patch.yaml│       │   ├── component-patch.yaml│       │   ├── exception-component-patch-1.yaml│       │   └── kustomization.yaml│       └── v2-overlay│           ├── application-patch.yaml│           ├── component-patch.yaml│           ├── exception-component-patch-1.yaml│           └── kustomization.yaml└── README.md
```
Defining Multiple Applications
------------------------------

If you wish to define multiple applications with different sets of components and versions for each application, you can replicate the configuration overviewed above for `application-a` for a second application and include it as an additional application base and overlays in the `overlay` directory.

This is the preferred way to define multiple applications within an application category (ex. Operators) or family/product organization (ex. Red Hat Advanced Cluster Management) as code because it allows you to make bulk configurations to your base component yaml (such as enabling muti-arch or labelling/ownership) in a single place, the component base, rather than multiple places.

If you follow this method to create an `application-b` composed of `component-c` and `component-d` then you’re directory structure will look something like:


```
├── base│   ├── component.yaml│   └── kustomization.yaml├── overlay│   ├── application-a│   │   ├── base│   │   │   ├── application.yaml│   │   │   ├── component-a│   │   │   │   ├── component-a-override.yaml│   │   │   │   └── kustomization.yaml│   │   │   ├── component-b│   │   │   │   ├── component-b-override.yaml│   │   │   │   └── kustomization.yaml│   │   │   └── kustomization.yaml│   │   ├── v1-overlay│   │   │   ├── application-patch.yaml│   │   │   ├── component-patch.yaml│   │   │   ├── exception-component-patch-1.yaml│   │   │   └── kustomization.yaml│   │   └── v2-overlay│   │       ├── application-patch.yaml│   │       ├── component-patch.yaml│   │       ├── exception-component-patch-1.yaml│   │       └── kustomization.yaml│   └── application-b│       ├── base│       │   ├── application.yaml│       │   ├── component-c│       │   │   ├── component-c-override.yaml│       │   │   └── kustomization.yaml│       │   ├── component-d│       │   │   ├── component-d-override.yaml│       │   │   └── kustomization.yaml│       │   └── kustomization.yaml│       └── v1-overlay│           ├── application-patch.yaml│           ├── component-patch.yaml│           ├── exception-component-patch-1.yaml│           └── kustomization.yaml└── README.md
```


|  | You can also modify the project structure to fit your own needs by moving application bases and component definitions to different levels, but we’ve found this configuration offers the most layered encapsulation across applications and application versions. |
| --- | --- |

[Creating secrets for your builds](../../configuring-builds/proc_creating-secrets-for-your-builds/)[Enabling hermetic builds](../../proc_hermetic-builds/)