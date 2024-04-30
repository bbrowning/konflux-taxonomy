Overview of Konflux environments
================================

Environments represent infrastructure. You can use them to test, develop, and release your application to production. You can create two types of environments in Konflux:

* Static environments, to which you can deploy your application for development or production.
* Temporary (ephemeral) environments, to which you can temporarily deploy your application during testing.
The following sections further explain these different environments and how you can use them.

Static environments
-------------------

By default, Konflux deploys your application to AWS through Red Hat OpenShift Service on AWS (ROSA). This default static environment runs your application for as long as you want. But you can host your application in a different static environment, using a bring your own cluster (BYOC) option.

Currently, with the BYOC option, you can use a static environment hosted by any of the major cloud providers — AWS, Azure, GCP, etc.

Temporary environments
----------------------

You might want to deploy your application as part of a custom integration test. For example, you might want to test if endpoints react in an expected manner, or to see if components react correctly to API queries.

Normally, Konflux runs integration tests in the static development environment. But to deploy your application during a test, you need a new environment. The static development environment might already host the latest version of your application.

This is the use case for temporary environments. You can configure Konflux to deploy your application to a temporary clone of the development environment. You can perform this configuration when adding an integration test. Konflux then clones the environment each time it performs the test. The temporary environment disappears after testing.

Additional resources
--------------------

* [Creating your own environment](../proc_creating_your_own_environment/) with the BYOC option
* [Adding an integration test](../../testing_applications/proc_adding_an_integration_test/) (step 7 discusses temporary environments)
[Retriggering integration tests](../../testing_applications/proc_retriggering_integration_tests/)[Creating your own environment](../proc_creating_your_own_environment/)