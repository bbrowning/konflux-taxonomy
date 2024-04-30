Surface-level tests
===================

Scope
-----

This document covers the surface-level tests (formerly known as "sanity tests") that Konflux runs as part of its component build pipeline. These surface-level tests automatically check all application images to ensure that they’re up-to-date, correctly formatted, and protected from security vulnerabilities.

Surface-level tests
-------------------

The Konflux component build pipeline supports several types of tests, including surface-level tests. The surface-level tests used in Konflux are run in the form of [Tekton tasks](https://tekton.dev/docs/pipelines/tasks/#overview). The utility used for validating container information is [Conftest](https://www.conftest.dev/). The following tables show the currently implemented surface-level tests:



Table 1. Deprecated image checks
| Test name | Description | Failure message |
| --- | --- | --- |
| image\_repository\_deprecated | Deprecated images are no longer maintained, leading to unresolved security vulnerabilities. | The container image must not be built from a repository marked as 'Deprecated' in COMET |



Table 2. Unsigned RPM check
| Test name | Description | Failure message |
| --- | --- | --- |
| image\_unsigned\_rpms | Packages signed with Red Hat’s secure signing server adheres to stringent policies and procedures. | All RPMs in the image must be signed. Found following unsigned rpms(nvra): |

[Overview of Konflux tests](../con_test-overview/)[Enabling a Snyk task](../enable_snyk_check_for_a_product/)