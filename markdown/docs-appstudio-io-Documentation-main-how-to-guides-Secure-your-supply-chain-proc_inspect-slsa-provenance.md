Downloading your SLSA provenance
================================

Since we claim to meet SLSA Build Level 3, we have provided the following procedure for you to download the SLSA provenace that Konflux generates for each of your [components](../../../glossary/#component), including both the attestation and its signature.

Prerequisites* [Login](../../../getting-started/getting_started_in_cli/) to Konflux in your CLI
* [Install](https://stedolan.github.io/jq/download/) the `jq` command line utility
* [Install](https://docs.sigstore.dev/cosign/installation/) the `cosign` command line utility
ProcedureFirst you need to get the image path for the component whose attestation you want to download. Then, you can use `cosign` to download the provenance.

1. List your components:


```
oc get components
```
Example output:


```
NAME                         AGE   STATUS   REASON   TYPEpartner-catalog-build-ucmg   24d   True     OK       Updatedpartner-catalog-ec-pz7b      18d   True     OK       Updated
```
2. Choose a component and get its image path:


```
oc get component <component name> -ojson | jq '.status.containerImage'
```
Example:


```
oc get component partner-catalog-build-ucmg -ojson | jq '.status.containerImage'
```
3. For convenience, save the image path to a local variable.

Example:


```
IMAGE=quay.io/redhat-user-workloads/rhn-support-csears-tenant/demo-build/partner-catalog-build-ucmg@sha256:<output omitted>
```
4. Use `cosign` to download the attestation, and use `jq` to put it in a human-readable format:


```
cosign download attestation $IMAGE | jq '.payload|@base64d|fromjson'
```
Example output:


```
{  "_type": "https://in-toto.io/Statement/v0.1",  "predicateType": "https://slsa.dev/provenance/v0.2",  "subject": [    {      "name": "quay.io/redhat-user-workloads/rhn-support-csears-tenant/demo-build/partner-catalog-build-ucmg",      "digest": {        "sha256": "<output omitted>"      }    }  ],  "predicate": {    "builder": {      "id": "https://tekton.dev/chains/v2"    },    "buildType": "tekton.dev/v1beta1/TaskRun",    "invocation": {<remaining output omitted>
```
5. Use the same tools to download the attestation signature:


```
cosign download attestation $IMAGE | jq '.|keys'
```
Example output:


```
[  "payload",  "payloadType",  "signatures"][  "payload",  "payloadType",  "signatures"]
```
6. (Optional) You can also print a high-level overview of the provenance-related artifacts that Konflux has created for a component:


```
cosign tree $IMAGE
```
Example output:


```
📦 Supply Chain Security Related artifacts for an image: quay.io/redhat-user-workloads/rhn-support-csears-tenant/demo-build/partner-catalog-build-ucmg@sha256::<output omitted>└── 💾 Attestations for an image tag: quay.io/redhat-user-workloads/rhn-support-csears-tenant/demo-build/partner-catalog-build-ucmg:sha256-:<output omitted>.att   ├── 🍒 sha256::<output omitted>   └── 🍒 sha256::<output omitted>└── 🔐 Signatures for an image tag: quay.io/redhat-user-workloads/rhn-support-csears-tenant/demo-build/partner-catalog-build-ucmg:sha256-:<output omitted>.sig └── 🍒 sha256::<output omitted>└── 📦 SBOMs for an image tag: quay.io/redhat-user-workloads/rhn-support-csears-tenant/demo-build/partner-catalog-build-ucmg:sha256-:<output omitted>.sbom  └── 🍒 sha256:<output omitted>
```
Additional resources
--------------------

* Learn about the SLSA framework and [how Konflux meets the requirements of SLSA Build Level 3](../../../concepts/slsa/con_slsa-conformity/).
* Red Hat’s Enterprise Contract (EC) is a powerful tool that you can also use to verify your SLSA provenance; visit [this page](https://enterprisecontract.dev/posts/introducing-the-enterprise-contract/) to learn how to use the EC CLI tool to verify your provenance. You will need the public key used by Tekton Chains, which is available as the **public-key** secret in the **openshift-pipelines** namespace and readable to all authenticated users.
[Inspecting SBOMs](../proc_inspect_sbom/)[Configuring dependencies rebuild for Java apps in the CLI](../proc_java_dependencies/)