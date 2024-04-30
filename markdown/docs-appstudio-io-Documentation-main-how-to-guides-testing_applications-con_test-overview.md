Overview of Konflux tests
=========================

You can ensure that your applications are stable, secure, compliant, and mutually compatible by implementing tests for Konflux to run on their components. There are currently 4 types of tests in Konflux:

* Surface-level tests
* Product security tests
* Custom tests
* Integration tests
The following sections explain each of these test types in greater detail.

Surface-level tests
-------------------

Surface-level tests in Konflux ensure the stability of the application, the build pipeline, its components, and the environment in which it is being tested. The surface-level tests used in Konflux are executed in the form of Tekton [tasks](../../../glossary/#task). The utility used for validating container information is [conftest](https://www.conftest.dev/). A full listing of Konflux surface-level tests is available in this document: [Surface-level tests](../surface-level_tests/).

For Konflux to perform our predefined surface-level tests on a given component, you must [upgrade its build pipeline](../../configuring-builds/proc_upgrade_build_pipeline/).

Product security tests
----------------------

Product security tests in Konflux ensure a product is secure and keep your image, application, and build pipeline up to date. Product Security tests include:

* Vulnerability scanning via Clair
* Anti-virus scanning via ClamAV
* Code scanning via SAST tools


	+ [Enabling a Snyk task for a product](../enable_snyk_check_for_a_product/)
For Konflux to perform our predefined product security tests on a given component, you also must [upgrade its build pipeline](../../configuring-builds/proc_upgrade_build_pipeline/).

Custom tests
------------

Custom tests in Konflux are tests that users and administrators create. To add a custom test to an individual component, [customize its build pipeline](../../configuring-builds/proc_customize_build_pipeline/) to include the test as another Tekton task. Or, to add a test that runs on all components of an application, [create a custom integration test](../proc_creating_custom_test/).

Integration tests
-----------------

Integration tests ensure that all build components are able to work together at the same time. You can [add an integration test](../proc_adding_an_integration_test/), simply by giving Konflux the address to a GitHub repo, and the path within that repo to the `.yaml` file that defines the test.

Konflux runs integration tests after it successfully builds the components of an application. As part of the build process, Konflux creates an image for each component and stores them in a Quay.io repository. Images of all the components are then compiled into a snapshot of the application. Konflux tests the snapshot against user-defined IntegrationTestScenarios, which, again, refer to a GitHub repository.

[Preventing redundant rebuilds](../../configuring-builds/proc_preventing_redundant_rebuilds/)[Surface-level tests](../surface-level_tests/)