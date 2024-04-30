Important notices about the privacy of your data
================================================

Publication notification for GitHub and Quay
--------------------------------------------

As a user, you have the right to understand where and how you enter personal and sensitive data, and when your data gets published to GitHub or Quay.

Data in GitHub repositories might be public
-------------------------------------------

When you create an application, Konflux generates a *public* Git repository that stores a Kubernetes YAML file with configuration instructions for your application’s components. These instructions contain a reference to the container image built from the source code for those components.

**Note:** Konflux cannot store application configuration instructions in a private GitOps repository. The artifacts created by Konflux are public and visible to anyone who is viewing the GitOps repository.

Data in Quay repositories might be public
-----------------------------------------

* If you use a public GitHub repository as a component’s source, Konflux publishes the container image it builds to a public Quay repository.
* If you use a private GitHub repository as a component’s source, Konflux publishes the container image it builds to a private Quay repository.
Secrets for sensitive data are available
----------------------------------------

With Konflux, you can use build and deployment secrets to secure your environments and store sensitive data such as your credentials, API and encryption keys, access tokens, and more. We store secrets using AWS Secrets Manager.

**Note:** Use secrets to store sensitive data. Do not enter any sensitive data in environment variables because Konflux stores such variables in a public GitOps repository. To create secrets, see [Creating secrets for your builds](https://redhat-appstudio.github.io/docs.appstudio.io/Documentation/main/how-to-guides/configuring-builds/proc_creating-secrets-for-your-builds).

[Support](../support/)