Configuring dependencies rebuild for Java applications
======================================================

For Java applications in Konflux, you can configure the Java Virtual Machine (JVM) build service either with the dependencies rebuild feature enabled or with that feature disabled.

JVM Build Service overview
--------------------------

The Java Virtual Machine Build Service (JBS or JVM Build Service) is a controller that rebuilds Java and other JVM Language based dependencies from source.

The Java ecosystem uses a binary distribution model, where binary jar files are downloaded from central repositories, such as Maven Central. This distribution model means that the only way to ensure an application is completely built from source is to rebuild all its component libraries from source in a trusted environment. Due to the Java ecosystem, you would need to manually rebuild the component libraries.

The Java binary distribution model relies on dependencies with unknown provenance maintained by external communities. This means that you can’t be sure who uploaded these artifacts or the build environment, so you can’t be sure of their flaws or vulnerabilities. The only way to know that you’re building from clean, logical code in a secure environment is to build from source code.

JBS automates this process as much as possible, making it much less time-consuming to create builds that are build from source in a controlled environment.

### Workflow Description

When using the JVM Build Service, the user workflow is as follows:

* The system builds your application by using community dependencies.
* The JVM Build Service analyzes your application and determines which dependencies the system needs to rebuild.
* The JVM Build Service generates `ArtifactBuild` objects to represent each artifact in your application before determining to which repository the artifacts belong. The JVM Build Service tags from which systems the artifacts derive.
* The system analyzes the repository and uses the results to find a build strategy. For example, if the system cannot find the JDK version to use, the system uses all versions to determine the most effective version to use.
* The system attempts to build all the dependencies and stores them in container images in an image registry, and `quay.io` is the default.
* When the system has completed all its builds, you can rebuild your application.
* If all the builds are successful, your application’s SBOM displays that none of the dependencies came from third-party repositories. However, you may need to troubleshoot when some dependencies fail to build.
Setup
-----

### Logging into the Server

All interactions with the JVM Build Service require you to be logged into the OpenShift namespace used for your builds.

Procedure* Copy the login command from: <https://registration-service-toolchain-host-operator.apps.stone-prd-host1.wdlc.p1.openshiftapps.com/>
### Setting up the CLI

Many of the commands can be setup using the JVM Build Service CLI. The CLI is currently distributed as a docker image.

Prerequisite* Log into your OpenShift namespace.
Procedure1. To use the Docker image, create the following alias:


```
alias jbs='docker run --mount type=bind,source=$HOME/.kube/config,target=/kube --mount type=bind,source=$HOME/.github,target=/root/.github --env KUBECONFIG=/kube  -it --rm   quay.io/redhat-appstudio/hacbs-jvm-cli:latest'
```
2. To update the latest version, create an updated alias.
3. To pull the latest version of the Docker image, run the updated alias:


```
alias update-jbs='docker  pull quay.io/redhat-appstudio/hacbs-jvm-cli:latest'
```
4. To show the usage, run commands with `--help` option.
5. To modify build recipes, like commands that fix failing builds, create a file like, `$HOME/.github`, that is specified at <https://github-api.kohsuke.org/>.
Configuring The JVM Rebuild Service
-----------------------------------

You can set up the JVM Build Service in the following ways:

* Setting up with the CLI
* Setting up without Quay.io configuration
* Setting up with Quay.io configuration
### Setting up with the CLI

If you do not require explicit quay.io configuration, you can simply set up the JVM Build Service. The JVM Build service automatically creates rebuilds for you and creates a query repository to store your rebuilt artifacts.

Prerequisite* You have setup the CLI.
Procedure* In the CLI, run the `setup rebuilds` commmand:

```
jbs> setup rebuildsWorking...found .dockerconfigjson secret with appropriate token keys in namespace sdouglas1-tenant, rebuilds are possibleRebuilds setup successfully
```
The `setup rebuilds` command automatically performs the steps detailed below and creates rebuilds for you. The JVM Build Service automatically creates a query repository to store your rebuilt artifacts.

### Setting up without Quay.io configuration\*

If you do not want to use the CLI, use the `kubectl` command to create the Kubernetes objects to set up the JVM Build Service directory.

Procedure1. Create a file, for example, `config.yaml`.
2. In the `config.yaml` file, create a `JBSConfig` resource with the following data:


```
apiVersion: jvmbuildservice.io/v1alpha1kind: JBSConfigmetadata:  name: jvm-build-configspec:  enableRebuilds: "true"
```
3. Run `kubectl apply -f config.yaml`
### Setting up with explicit Quay.io configuration

If you want to specify where the rebuilt artifacts are stored, you must use the Quay.io configuration to configure your JVM Build Service. You must also provision a secret to allow the JVM Build Service to push to the repository.

Procedure1. In the RHTAP UI create an image pull secret for the quay.io repository using the page under the 'Secrets' tab. This can be called anything you like.
2. Create a file, for example, `config.yaml`.
3. In the `config.yaml` file, create a **JBSConfig** resource with the following data:


```
apiVersion: jvmbuildservice.io/v1alpha1kind: JBSConfigmetadata:  name: jvm-build-configspec:  enableRebuilds: "true" **(1)**  registry:   host: quay.io **(2)**   owner: OrgID **(3)**   repository: artifact-deployments **(4)**   secretName: my-secret **(5)**  mavenBaseLocations:    maven-repository-300-jboss: "https://repository.jboss.org/nexus/content/groups/public/" **(6)**    maven-repository-301-gradleplugins: "https://plugins.gradle.org/m2"    maven-repository-302-confluent: "https://packages.confluent.io/maven"
```


| **1** | To enable and configure the rebuild dependencies function, add enable-rebuilds: "true" to the `JBSConfig` object. |
| --- | --- |
| **2** | The URL of the registry that holds the images of your rebuild dependencies. |
| **3** | The organization ID. |
| **4** | The repository to store the images in. |
| **5** | The name of the secret we created in the UI. |
| **6** | List any additional Maven repositories here. |
4. While logged into the build namespace, run `kubectl apply -f config.yaml`.
Examining the system state
--------------------------

After you have run your first java build with rebuilds enabled you can use `kubectl` to view the state of the rebuilds.

To do this run the following command:


```
kubectl get artifactbuilds.jvmbuildservice.io
```
This will give you output similar to the following:


```
NAME                        GAV                                    STATEwsdl4j.1.6.3-138a1801       wsdl4j:wsdl4j:1.6.3                    ArtifactBuildCompletexmlsec.3.0.0-ceb06cd9       org.apache.santuario:xmlsec:3.0.0      ArtifactBuildCompletexsdlib.2013.6.1-0aed4ed6    net.java.dev.msv:xsdlib:2013.6.1       ArtifactBuildFailed
```
This lets you view the state of the builds of all maven artifacts that were identified. As a single build, it can produce multiple artifacts, and you can look at the individual builds:


```
kubectl get artifactbuilds.jvmbuildservice.ioNAME                             URL                                              TAG                STATE                              MESSAGE03dc791547cab448e388fc3c4a1edaa7 https://github.com/LatencyUtils/LatencyUtils.git LatencyUtils-2.0.3 DependencyBuildStateComplete080dbba8b3ffba35739ebe5bce69a2be https://github.com/apache/commons-logging.git    LOGGING_1_2        DependencyBuildStateComplete
```
The names of the `PipelineRun` objects begin with the build name. This enables you to view logs for each `PipelineRun`.

### Rerunning builds

To rebuild an artifact, you need to annotate the `ArtifactBuild` object with `jvmbuildservice.io/rebuild=true`. For example, to rebuild the `zookeeper.3.6.3-8fc126b0` `ArtifactBuild`, you would run:


```
kubectl annotate artifactbuild zookeeper.3.6.3-8fc126b0 jvmbuildservice.io/rebuild=true
```
You can also use the `jvmbuildservice.io/rebuild=failed` annotation to rebuild only failed artifacts, for example, the following command retries all failed artifacts:


```
kubectl annotate artifactbuild --all jvmbuildservice.io/rebuild=failed
```
Generally, when you are trying to fix a failure, you must manually run the builds yourself.

Dealing wth failed builds
-------------------------

In order to see why the build failed, look at the results from the JVM Build Service.

Look at the state of the corresponding `ArtifactBuild`. In the previous example, to figure out why `jackson-databind`failed, execute the following command to view the ArtifactBuild state:


```
kubectl get artifactbuilds.jvmbuildservice.io jackson.databind.2.13.4.2-50dca403 -o yaml
```
You might get the following output:


```
apiVersion: jvmbuildservice.io/v1alpha1kind: ArtifactBuildmetadata:  creationTimestamp: "2022-12-21T02:50:31Z"  generation: 1  name: jackson.databind.2.13.4.2-50dca403  namespace: test-jvm-namespace  resourceVersion: "51371901"  uid: f11a4b7f-b19b-4e79-ab8f-392bff80e25fspec:  gav: com.fasterxml.jackson.core:jackson-databind:2.13.4.2status:  scm:    scmType: git    scmURL: https://github.com/FasterXML/jackson-databind.git **(1)**    tag: jackson-databind-2.13.4.2  state: ArtifactBuildFailed **(2)**
```


| **1** | This is the SCM information that was successfully discovered |
| --- | --- |
| **2** | This tells us the current state. In this case the build has failed. |

You need to deal with the failure states: `ArtifactBuildMissing` and `ArtifactBuildFailed`.

### Dealing with missing artifacts (`ArtifactBuildMissing`)

If your build has ended up in the state,`ArtifactBuildMissing`, you must add some SCM information into your build data repository.

There are three possible causes of this state:

* We could not figure out which repository the artifact comes from.
* We could not map the version to a tag in this repository.
* The pipeline failed for other reasons, for instance, network failure.
The pipeline will be named <artifact-build-name>-scm-discovery-<random-string>. To view the pipeline logs:


```
tkn pr list | grep jackson.databind.2.13.4.2-50dca403 **(1)**tkn pr logs jackson.databind.2.13.4.2-50dca403-<discoveredid> **(2)**
```


| **1** | Find the pipeline name. |
| --- | --- |
| **2** | Use the name from the first line to view the logs. |

This pipeline log helps you identify why the build failed.

To fix missing SCM information, add additional information to the [build information repository](https://github.com/redhat-appstudio/jvm-build-data/tree/main/scm-info). After this information has been updated, see the instructions on how to re-run it: [Rerunning builds](#rebuilding_artifacts).

The SCM information for the `com.fasterxml.jackson.core:jackson-databind:2.13.4.2` above will be searched for in the followinglocation, from most specific to least specific:


```
scm-info/com/fasterxml/jackson/core/_artifact/jackson-databind/_version/2.13.4.2/scm.yaml **(1)**scm-info/com/fasterxml/jackson/core/_artifact/jackson-databind/scm.yaml **(2)**scm-info/com/fasterxml/jackson/core/scm.yaml **(3)**
```


| **1** | This approach specifies the group-id, the artifact-id, and the version. Note, that the version matches based on 'less than', so older versions, like 2.1, would still match, while newer versions would not. |
| --- | --- |
| **2** | These match based on the group-id and artifact-id. This approach is good for when a specific group-id is used in lots of different repositories. |
| **3** | These match based on the group-id. This is used when the majority of the artifacts within the group id come from a single repo. |

After we identify where we can add a SCM info file, the file has the following format. Note that everything is optional except for the URL.


```
type: "git" **(1)**uri: "https://github.com/eclipse-ee4j/jaxb-stax-ex.git" **(2)**tagMapping: **(3)**  - pattern: (.*)-jre **(4)**    tag: v$1 **(5)**  - pattern: (\d+)\.(\d+)    tag: release-$1-$2  - pattern: 3.0    tag: jaxb-stax3-3.0legacyRepos: **(6)**  - type: "git"    uri: "https://github.com/javaee/metro-stax-ex.git"    path: "stax-ex" **(7)**
```


| **1** | The type is optional, at the moment only git is supported. |
| --- | --- |
| **2** | The primary URI to search |
| **3** | Mappings between a version and a tag. We attempt to do this automatically but it is not always successful. |
| **4** | If the version matches the regex then we look for a corresponding tag. |
| **5** | The tag to search for in the repo. `$n` can be used to substitute the regex capture groups, with $0 being the full match. |
| **6** | Additional repositories to search. This can be useful if a project has moved home over time. |
| **7** | Some projects are not in the root of the repo. The path tells us the directory they are in. |

After adding this information, re-running the build should resolve this information, moving it to the state `ArtifactBuildBuilding`, and eventually to `ArtifactBuildComplete`.

### Identifying why a build failed

To fix failed builds, first look at the build logs and figure out why it failed.

**Procedure**

1. Identify the correct `DependencyBuild` object.
2. Run `kubectl get dependencybuilds` to list the objects.
3. Pick the object you are interested in. Generally each `DependencyBuild` will have multiple pipelineruns, named using the pattern `<dependency-build-name>-build-<n>`.
4. View the logs by using the command `tkn pr logs <name>`:

```
tkn pr logs e8f6f6126f222a021fedfaee3bd3f980-build-0
```
The builds are performed from lowest JDK to highest JDK. Although some JDKs may be skipped if the analyser can determine theyare not relevant. If a build has failed because of a JDK version issue, you might need to look at a later build.

### Unknown build systems

If there are no builds at all, then the analyser could not find a build file to use.

**Procedure**

1. Create a fork of the repository.
2. Change the build system to Maven.
3. Build from the fork.
To see an example, go to [this Java package project](https://github.com/jvm-build-service-code/cs-au-dk-dk.brics.automaton) on GitHub.

Because the 1.11-8 release had no build file, we forked the project and added a file. We then added this file to [the SCM information](https://github.com/redhat-appstudio/jvm-build-data/blob/30a00905314ca5bf20d653af1a59c39c93b9aadb/scm-info/dk/brics/_artifact/automaton/scm.yaml#L6).

### Tweaking build parameters

Tweak build parameters to get them to pass. Tweak build paramaters by adding a `build.yaml` file to the builddata repository. For our databind example, the file would go in one of the following locations:


```
build-info/github.com/FasterXML/jackson-databind/_version/2.13.4.2/build.yaml **(1)**build-info/github.com/FasterXML/jackson-databind/build.yaml **(2)**
```


| **1** | This file applies to version up to and including version 2.13.4.2 |
| --- | --- |
| **2** | This file applies to all other versions |

An example of a complete (although nonsensical) file is shown below:


```
enforceVersion: true **(1)**additionalArgs: **(2)**  - "-DskipDocs"alternativeArgs: **(3)**  - "'set Global / baseVersionSuffix:=\"\"'"  - "enableOptimizer"preBuildScript: | **(4)**    ./autogen.sh    /bin/sh -c "$(rpm --eval %configure); $(rpm --eval %__make) $(rpm --eval %_smp_mflags)"additionalDownloads: **(5)**  - uri: https://github.com/mikefarah/yq/releases/download/v4.30.4/yq_linux_amd64 **(6)**    sha256: 30459aa144a26125a1b22c62760f9b3872123233a5658934f7bd9fe714d7864d **(7)**    type: executable **(8)**    fileName: yq **(9)**    binaryPath: only_for_tar/bin **(10)**
```


| **1** | If the tag contains build files that do not match the version include this to override the version. |
| --- | --- |
| **2** | Additional parameters to add to the build command line. |
| **3** | A complete replacement for the build command line, this should not be used with 'additionalArgs' as it will replace them. This is mostly used in SBT builds. |
| **4** | A script to run before the build. This can do things like build native components that are required. |
| **5** | Additional downloads required for the build. |
| **6** | The URI to download from |
| **7** | The expected SHA. |
| **8** | The type, can be either `executable`, or `tar`. |
| **9** | The final file name, this will be added to `$PATH`. This is only for `executable` files. |
| **10** | The path to the directory inside the tar file that contains executables, this will be added to `$PATH`. |

Configuring Java builds with disabled dependencies rebuild
----------------------------------------------------------

You must configure your repository by creating a Kubernetes JBSConfig custom resource to ensure that your namespace uses the JVM build service. When this ConfigMap is present, the build service operator configures the necessary support infrastructure in a workspace. To speed up the build process and reduce the load on Maven Central, this currently creates an artifact cache that caches Maven objects.

When building an application, the system redirects all requests by using this artifact cache. By default this proxies to maven central, however, you can configure other repositories. The repositories configured in your project will not be used,which allows the namespace administrator to control where dependencies come from.

**Procedure**1. Browse to an appropriate directory and create a file, for example, `config.yaml`.
2. In the `config.yaml` file, create a **ConfigMap** resource with the following data:


```
apiVersion: jvmbuildservice.io/v1alpha1kind: JBSConfigmetadata:  name: jvm-build-configspec:  mavenBaseLocations: **(1)**    maven-repository-300-jboss: "https://repository.jboss.org/nexus/content/groups/public/"    maven-repository-301-gradleplugins: "https://plugins.gradle.org/m2"    maven-repository-302-confluent: "https://packages.confluent.io/maven"
```


| **1** | To add a maven repository the key in the map must follow a set pattern, which is, maven-repository-$priority-$name: $repo-url. Additionally, Maven central has a priority of 200; therefore the system tries anything with a lower priority before maven central. The rebuilt artifacts if they are in use have a priority of 100. |
| --- | --- |
### Clearing the cache

If for some reason you need to clear the cache you can do it by applying an annotation to the `JBSConfig` object:

`kubectl annotate jbsconfig jvmbuildservice.io/clear-cache=true --all`

This will delete all cached artifacts from the local storage, and they will be re-downloaded from the upstream repositories.

Additional resources
--------------------

For more information, see:

* [Java build service](../../../concepts/java-build-service/java-build-service/).
* [Java build service components](../../../concepts/java-build-service/java-build-service-components/)
[Downloading your SLSA provenance](../proc_inspect-slsa-provenance/)[Managing compliance with the Enterprise Contract](../../proc_managing-compliance-with-the-enterprise-contract/)