Supply chain security through SLSA conformity
=============================================

Supply-chain Levels for Software Artifacts (SLSA)
-------------------------------------------------

Supply-chain Levels for Software Artifacts (SLSA) is a security framework produced through industry collaboration. We use this framework as a guide for reinforcing the build process we use for your applications, to better secure your software supply chain.

SLSA assigns two primary responsibilities to build platforms like Konflux:

* **Provenance** to describe how the platform built each software artifact
* **Build isolation** to prevent tampering with the build process
SLSA also includes three Build Levels, which provide you with increasing guarantees about how build platforms fulfill these responsibilities. Any build platform that generates provenance conforms to the SLSA framework’s Build Level 1 (L1) specifications. Build platforms produce artifacts with higher Build Levels by hardening provenance against forgery and by isolating the build process. As of the v1.0 specification, Build Level 3 (L3) is the highest Build Level. Konflux produces Build L3 artifacts.

The rest of this document further explains our key responsibilities, provenance and build isolation, and how we fulfill those responsibilities. It concludes with a table summarizing how Konflux meets the requirements for SLSA Build L3.

SLSA Provenance
---------------

In the context of its framework, SLSA defines provenance as “the verifiable information about software artifacts describing where, when and how something was produced.” SLSA provenance is expressed through attestation, and for higher Build Levels, build platforms must sign that attestation.

### Attestation

Attestation is the fundamental component of provenance, and you can think of it like a recipe. A recipe tells you how someone made a certain dish, and attestation tells you how a build platform created a software artifact. Our SLSA attestation specifically includes a subject that tells you which artifact the attestation belongs to, and a predicate that explains how Konflux built each artifact, including relevant links.

### Signing the attestation

At higher Build Levels, SLSA directs build platforms to harden their provenance by signing each attestation. With the signature, you can verify that no one tampered with the attestation for your artifacts. Currently, Konflux signs attestations using a private key.

### Evaluating provenance

In its Build Levels, SLSA evaluates provenance based on three questions:

* Completeness: Does the provenance fully explain how the artifact was built?
* Authenticity: How certain are you that the provenance came from the builder?
* Accuracy: How difficult is it to tamper with provenance during the build process?
Completeness of provenance comes from its attestation, and authenticity derives from the signature.

Accuracy is where provenance and build isolation intersect. To generate unforgeable provenance, build platforms must store those secret materials in a secure management system that platform users cannot access. In Konflux, only Tekton Chains, which generates and signs provenance, has access to the private key.

Build isolation
---------------

According to the SLSA framework, our other primary responsibility is to guarantee that we build your software correctly, without external influence, by isolating the builds. For Build L2, SLSA directs build platforms to run builds in a hosted environment, and for Build L3, they direct us to make builds internally isolated within that hosted environment.

### Hosted

If builds run on an individual’s workstation, they become inconsistent. This inconsistency can cause mundane technical issues, but it also introduces security risks. What if undetected malware is lurking on that person’s machine?

To shrink the attack plane, SLSA dicates that builds should execute “using a hosted build platform on shared or dedicated infrastructure, not on an individual’s workstation.” By using an environment that comes from a known, auditable state, build platforms can largely ensure that they generate artifacts in the same way every time.

Konflux is a hosted build platform. We execute builds on Amazon Web Services (AWS) through Red Hat OpenShift Service on AWS (ROSA).

### Internally isolated

Running builds in a hosted environment can protect your builds from malware installed on an individual’s workstation. But an attacker could gain access to your instance of a hosted build platform. What if they inject a malicious payload into one of your artifacts during the build process, and falsify the provenance to cover their tracks? Or what if they use one build to poison an environment that another build uses?

To mitigate these threats, and others, SLSA instructs build platforms to execute builds in an environment that, within the larger hosted environment, is internally isolated from other builds, users, and the control plane. The only external influence that is permissible is influence that the build itself requests, such as dependencies.

Konflux internally isolates builds within ROSA using several different tactics. For example, Tekton Chains generates and signs provenance in its own namespace, separate from the one that runs user-defined build steps, so attackers cannot forge provenance. And builds themselves run in their own ephemeral pods, so they cannot persist or influence the build environment of subsequent builds.

How we meet the requirements for SLSA Build L3
----------------------------------------------

The following table summarizes how Konflux conforms to the specification for producing SLSA Build L3 software artifacts.



| Build level | Requirements | How we meet them |
| --- | --- | --- |
| *For provenance* | | |
| L1: Provenance exists | Provenance is:* Automatically generated * Formatted per SLSA guidelines, or contains equivalent information * Complete as possible | Provenance in Konflux is:* Generated for each software artifact * Formatted according to SLSA guidelines * Complete |
| L2: Hosted build platform | Provenance is complete and authentic:* Users can validate provenance. * The control plane, not tenants, generates provenance. * Provenance is complete. | Konflux:* Signs attestations with a private key * Generates provenance itself using Tekton Chains * Generates complete attestations |
| L3: Hardened builds | Provenance is complete, authentic, and accurate:* Secret material used to authenticate provenance is stored in a secure management system. * Secret material is not accessible to the environment running user-defined build steps. * Provenance is complete, including fully enumerated external parameters. | Konflux:* Stores secret materials in Tekton Chains, which is a secure management system * Uses Tekton Chains in a separate namespace * Enumerates external parameters in its provenance |
| *For build isolation* | | |
| L1 | No build isolation requirements for L1 conformity | N/A |
| L2: Hosted build platform | All build steps run using a hosted build platform on shared or dedicated infrastructure, not on an individual’s workstation. | Konflux is hosted through ROSA. |
| L3: Hardened builds | Builds run in an isolated environment:* Builds cannot access secrets of the platform. * Two builds cannot influence one another. * Builds cannot persist or influence environment of other builds. * Builds cannot inject false entries into a cache used by another build. * Services allowing remote influence must be listed as external parameters in provenance. | In Konflux:* Only Tekton Chains can access secret materials. * Builds run in ephemeral pods. * ServiceAccounts (API objects that are shared within projects) have reduced permissions. * Tekton Chains generates and signs provenance outside users’ workspaces. * External parameters are fully enumerated in provenance. |

Additional resources
--------------------

* Learn [how to inspect the SLSA](../../../how-to-guides/Secure-your-supply-chain/proc_inspect-slsa-provenance/) provenance for your components.
* Visit the [SLSA overview page](https://slsa.dev/spec/v1.0/), the [Build Levels](https://slsa.dev/spec/v1.0/levels) page, or the [verifying build platforms](https://slsa.dev/spec/v1.0/verifying-systems) page.
[Managing multiple software versions](../../../how-to-guides/proc_multiversion/)[Java build service](../../java-build-service/java-build-service/)