Java build service components
=============================

When configuring standard Java builds with enabled dependencies, the JVM-build-service consists of the following components:

* Dependency Analyzer
* Build Database
* Cache
Dependency analyzer
-------------------

Dependency Analyzer is responsible for determining all the dependencies in a Java application. The Dependency Analyzer task analyzes the completed application to find the dependencies in the final application. It then creates the **ArtifactBuild** objects that tell the system to try to rebuild any dependencies from 3rd party repositories.

Build database
--------------

The Build Database consists of one or more `.git` repositories containing information about how to build projects, for example, SCM locations and build parameters. The system stores all this information in the `./build-info` and `./scm-info` directories.

In addition, you can configure your own build database by adding the following data:


```
apiVersion: v1kind: ConfigMapmetadata: name: jvm-build-config namespace: test-jvm-namespacedata: registry.owner: OrgID **(1)**
```


| **1** | The organization ID. |
| --- | --- |

Cache
-----

You can use the caching service to improve the performance. The cache is a Quarkus application and is configured via standard Quarkus configuration keys. That means any config key listed here can be overridden by both system properties, or by environment variables.

Troubleshooting
---------------

1. **Issue: Missing artifact build**

Resolution Identify the source from where the system is building the application. When identified, if missing, add the source URL and tags to the `scm.yaml` file:

**Example `scm.yaml` file**


```
type: "git"uri: "https://gitlab.ow2.org/asm/asm.git"tagMapping: - pattern: (\d+)\.(\d+)   tag: ASM_$1_$2 - pattern: (\d+)\.(\d+)\.(\d+)   tag: ASM_$1_$2_$3
```
2. **Issue: Dependencies failed to rebuild**

Resolution: You can resolve this error by adding additional build arguments or by following the trial and error route.

**Example additional build arguments**


```
additionalArgs: - "-DskipDocs=true" - "-Dno-test-modules"
```
References
----------

### `/build-info` and `/scm-info` directories

The `./build-info` and `./scm-info` directories consist of all the build information. The layout of this directory is based on the group id of the ArtifactBuild. For example, in the case of an ArtifactBuild with the group id of com.acme, you must store its information in the **/build-info/com/acme** folder.

Within this group id directory, you can store more specific information that is only applied to a specific artifact, version, or combination of artifact + version. You can store these types of information by using the **\_artifact** and **\_version** folders.

When you use both **\_artifact** and **\_version** folders, the **\_artifact** folder takes precedence over the **\_version** folder.

**Example**If you have an artifact com.acme.gizmo:gizmo-core:1.0.0.Final you can place the files relevant to this artifact at different locations.

* **/build-info/com/acme/gizo** - Applied to every artifact with the group id com.acme.gizmo. This is the most common layout and most of the artifacts with a given group id come from the same directory
* **/build-info/com/acme/gizo/\_artifact/gizmo-core** - Provides information about a specific artifact. This is helpful when lots of different repositories build artifacts with the same group id
* **/build-info/com/acme/gizo/\_artifact/gizmo-core/\_version/1.0.0.Final** - Contains information about a specific version of a specific artifact
* **/build-info/com/acme/gizo/\_version/1.0.0.Final** - Contains information about a specific version of a specific group id
Additional resources
--------------------

For more information, see [Java build service](../java-build-service/).

[Java build service](../java-build-service/)[Glossary](../../../glossary/)