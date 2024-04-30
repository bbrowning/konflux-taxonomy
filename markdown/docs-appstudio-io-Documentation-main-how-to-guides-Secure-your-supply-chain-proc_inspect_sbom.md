Inspecting SBOMs
================

Software bill of materials
--------------------------

A software bill of materials (SBOM) provides greater transparency for your software supply chain. In Konflux, an SBOM lists all the software libraries that a component uses. Those libraries can enable specific functionality or facilitate development.

You can use an SBOM to better understand the composition of your software, identify vulnerabilities, and assess the potential impact of any security issues that may arise. Also, to comply with cybersecurity regulations, you might need to provide your customers with the SBOM for your application’s components.

Viewing an SBOM in the web UI
-----------------------------

Prerequisites* You must have an application that Konflux has successfully built and deployed.
ProcedureIn the console, complete the following steps to download the SBOM for a component:

1. Navigate to the **Activity** > **Pipeline runs** tab.
2. For the component whose SBOM you want to view, select its most recent pipeline run.
3. On the **Pipeline run details** page, select **View SBOM**.


	1. You can use your web browser to immediately search the SBOM for terms that indicate vulnerabilities in your software supply chain. For example, try searching for "log4j".
	2. You can select **Download** to download the SBOM, or **Expand** to view it full-screen.


|  | This SBOM is unsigned. You can still use it for standard business processes, like providing an SBOM to your customers. However, do not use this unsigned SBOM as a legal document. |
| --- | --- |

Downloading an SBOM in the CLI
------------------------------

Prerequisites* Install the [Cosign](https://docs.sigstore.dev/cosign/installation/) CLI tool.
* Install the [jq](https://stedolan.github.io/jq/download/) CLI tool.
* [Login](../../../getting-started/getting_started_in_cli/) to Konflux.
ProcedureIn the CLI, complete the following steps to download the SBOM for a component:

1. List your components.


```
$ oc get components
```
Example output
```
NAME                               AGE   STATUS   REASON   TYPEdevfile-sample-go-basic-8wqt       8m54s True     OK       Updateddevfile-sample-python-basic-ikch   20d   True     OK       Updated
```
2. Choose which component’s SBOM you want to download. Then use `oc get` and the jq CLI tool to get the component image path.


```
$ oc get component <component name> -ojson | jq '.status.containerImage'
```
Example
```
$ oc get component devfile-sample-python-basic-ikch -ojson | jq '.status.containerImage'    "quay.io/redhat-appstudio/user-workload@sha256:<output omitted>"
```
3. Use Cosign to download the SBOM. From the output of the last command, pass the image path as an argument into Cosign’s `download sbom` command. Be sure to delete any quotation marks around the image path.

Example
```
$ cosign download sbom quay.io/redhat-appstudio/user-workload@sha256:<output omitted>
```


|  | Because the SBOM is unsigned, Cosign displays a warning about its authenticity. You can still use this SBOM for standard business processes, like providing an SBOM to your customers. However, do not use this unsigned SBOM as a legal document. |
| --- | --- |


```
WARNING: Downloading SBOMs this way does not ensure its authenticity.If you want to ensure a tamper-proof SBOM, download it using 'cosign download attestation <image uri>'or verify its signature using 'cosign verify --key <key path> --attachment sbom <image uri>'.
```

	1. (Optional) To view the full SBOM in a searchable format, you can redirect the output:
```
$ cosign download sbom quay.io/redhat-appstudio/user-workload@sha256:<output omitted> > sbom.txt
```
Reading the SBOM
----------------

In the SBOM, as the following sample excerpt shows, you can see four characteristics of each library that a component uses:

1. Its author or publisher
2. Its name
3. Its version
4. Its licenses
This information helps you verify that individual libraries are safely-sourced, updated, and compliant.


```
{    "bomFormat": "CycloneDX",    "specVersion": "1.4",    "serialNumber": "urn:uuid:89146fc4-342f-496b-9cc9-07a6a1554220",    "version": 1,    "metadata": {        ...    },    "components": [        {            "bom-ref": "pkg:pypi/flask@2.1.0?package-id=d6ad7ed5aac04a8",            "type": "library",            "author": "Armin Ronacher <armin.ronacher@active-4.com>", **(1)**            "name": "Flask", **(2)**            "version": "2.1.0", **(3)**            "licenses": [ **(4)**                {                    "license": {                        "id": "BSD-3-Clause"                    }                }            ],            "cpe": "cpe:2.3:a:armin-ronacher:python-Flask:2.1.0:*:*:*:*:*:*:*",            "purl": "pkg:pypi/Flask@2.1.0",            "properties": [                {                    "name": "syft:package:foundBy",                    "value": "python-package-cataloger"                    ...
```
Additional resources
--------------------

* You can implement an automated check that verifies the integrity and security of your SBOM, using the CycloneDX tool, by upgrading your build pipeline.
[Creating a team workspace](../../managing-workspaces/proc-creating_a_team_workspace/)[Downloading your SLSA provenance](../proc_inspect-slsa-provenance/)