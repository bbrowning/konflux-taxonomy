Why Konflux?
============

Developing an app is a long, costly process. Multiple teams, computing power, and a whole lot of time make the endeavor of launching an app *expensive*.

Enter Konflux – your one stop shop for building, testing, and deploying source code with secure CI/CD. Simply input the URL of your repository into our service, and we get to work building a pipeline, generating a snapshot, testing your code, and ultimately deploying your application to the hybrid cloud. Quickly get your app out to the world and then immediately see the value that it creates.

**Give us a few clicks, and we’ll get you started in a few minutes.**

*We’re secure*: We provide support for [SLSA Level 3](https://slsa.dev/spec/v1.0/levels) compliance to help you spot critical vulnerabilities. You can rest assured that our strong protections against tampering and threats can help keep you and your applications safe.

*We’re fast*: We help you import, containerize, and deploy your applications in minutes.

Let’s get to work and give you back the time, effort, and money that your developers traditionally spent on manual processes.

Key features
------------

Want to learn more? You can benefit from all of the following features with Konflux:

* Build your Java, Python, Node, or Go-based application into a container image.
* Apply the appropriate attestations and cryptographic signatures and provenance by using Tekton chains.
* Automatically deploy your container image to a provided development environment.
* Verify that your container image meets SLSA guidelines by using our enterprise contract with 41+ rules.
* Catch critical vulnerabilities quickly with each pull request.
* Continuously build, test, and roll out your applications with a simple `git push` or acceptance of a pull request.
* Take advantage of GitOps-based continuous deployment with an embedded ArgoCD to your Kubernetes.
* And much more!
Use cases
---------

You can create applications with any of the following languages and frameworks:

* Java
* Spring Boot
* Quarkus
* Node.js
* Python
* Go
We use our Dockerfiles and Devfiles to containerize your application.

How does it work?
-----------------

Under the hood, Konflux is largely based on OpenShift, Tekton, and ArgoCD. To get started, you don’t need to know anything about those technologies, but we know you might be curious!

### Customized Tekton build pipeline

Konflux enables you to have a Tekton pipeline stored in your own repo. We provide features to help you keep that pipeline up to date and in compliance with your release standards.

### View your triggered builds

We automatically start a build by using the pipeline definition in your pull request (PR). You can set up your PRs to auto-merge after successful PR tests.

We post PR test feedback on GitHub by using the `checks` API. In this way, your application code and your build pipeline code can be properly tested and automatically merged. Builds that are triggered by a PR are not deployed to your development environment, so you must merge them first.

### Merge and retest your pull requests

After you merge the PR, the commit activity shows that the merged commit is being built. If successful, we trigger any integration tests that you defined and then move to deployment.

With Konflux, it’s easy to automate the application creation process from commit to production deployment.

What’s next
-----------

To learn how to create an app with a sample, go to [Getting started](getting-started/get-started/).

[Getting started with Konflux](getting-started/get-started/)