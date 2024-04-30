Java build service
==================

JVM build service
-----------------

The JVM build service enhances your Java builds by providing the following features:

* A local cache of Maven artifacts to speed up build times
* A software bill of materials (SBOM) based on artifact tracking to find dependencies in your final image
* The ability to rebuild Java dependencies from the source so that you can be sure of your dependencies' provenance
You can configure standard Java builds in either of the following situations:

* When you have [enabled dependencies rebuild](../../../how-to-guides/Secure-your-supply-chain/proc_java_dependencies/#_configuring_java_builds_with_enabled_dependencies_rebuild)
* When you have [disabled dependencies rebuild](../../../how-to-guides/Secure-your-supply-chain/proc_java_dependencies/#_configuring_java_builds_with_disabled_dependencies_rebuild)
Additional resources
--------------------

For information about the components that you use when configuring standard Java builds with enabled dependencies, see [Java build service components](../java-build-service-components/).

[Supply chain security through SLSA conformity](../../slsa/con_slsa-conformity/)[Java build service components](../java-build-service-components/)