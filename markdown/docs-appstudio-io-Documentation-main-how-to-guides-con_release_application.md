Releasing an application
========================

Two teams work together to release an application:

* **Development team** - The team that develops and supports the application in a pre-production environment.
* **Managed environment team** - The team that supports the production instance of that application.
![Managed Environment](../../_images/managed_environment.png)[1] When an application is ready for release, the Development team contacts the Managed Environment team; for example, their organization’s SRE team, requesting access to the Managed environment for the first production release.

[2] The Managed environment team creates the managed environment and responds to the development team with the managed environment’s configuration details. The Managed environment inherits some details of the development team’s workspace. However, the development team has limited access to the production environment, which is a part of the managed environment.

[3] The development team creates a matching configuration in their environment that is same as that of the Managed environment and attempts to release the application to production.

[4] The Managed environment team validates the initial release and configures a traffic gateway, which allows external traffic to the application.

Next steps[Creating a `releasePlan` object](https://redhat-appstudio.github.io/docs.appstudio.io/Documentation/main/how-to-guides/proc_release_plan/)

[Managing compliance with the Enterprise Contract](../proc_managing-compliance-with-the-enterprise-contract/)[Creating a `releasePlan` object](../proc_release_plan/)