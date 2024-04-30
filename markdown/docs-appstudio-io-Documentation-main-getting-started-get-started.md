Getting started with Konflux
============================

Signing up
----------

1. Go to [Konflux](https://console.redhat.com/preview/hac/application-pipeline).
2. Click **Join waitlist**.
Creating your first application
-------------------------------

We include ready-to-use bundled code samples that you can import into our service. In this guide, we’ll walk you through how to fork a sample repository and create your first application. To begin, click **Create an application**.

### Choosing a bundled sample

Scroll to **Select a sample** and choose one of the following options:

* Node.js
* Quarkus
* Spring Boot
* Python
* Go
Decided on a favorite sample? Great! Now let’s fork the code to your repo. By the way, we call this code a *component*.

### Forking a sample repository

#### Why should you fork a sample?

These are the many perks to forking one of our samples:

* Pipeline customization
* Automated builds for new commits with GitHub webhook integration
* Pull request testing
* Rebuilding dependencies from source
* Scanning your build for vulnerabilities, viruses, and other checks
#### How to fork a sample

To fork the sample, complete the following steps:

1. Click **Open Git repository** for the sample that you chose. This link takes you to GitHub.
2. Now that you’re in GitHub, click **Fork**.
3. Copy the URL of this new forked repository.
### Importing the code from your forked repository

1. Return to the app and scroll up to **Bring in your own code**.
2. In **Git repository URL**, paste the URL that you copied previously.
3. Click **Import code**.
### Reviewing and configuring

We now scan your Git repository for source code and detect your runtime and other configuration settings for you to review. You have the option to use our default build pipeline or to customize the pipeline. Let’s stick with the default option for now.

Complete the following steps to finish:

1. In **Application details**, enter a name for your app.
2. In **Component name**, enter a name for your component.
3. Leave the toggle set to **Default build pipeline**.
4. Scroll to the end of the page and click **Create application**.
Advanced options
----------------

### Adding more components

Because your application can run on one or more components, you might want to add more. The additional source code that you add can either be from the *same* repository that you used when you created your application, or a *different* Git repository. Remember, we call source code *components*.

In the **Overview** tab, select **Add component**. Follow the process in [How to fork a sample](#how-to-fork-a-sample) to add any additional components.

### Customizing your build pipeline

In [Reviewing and configuring](#reviewing-and-configuring), you used the default built pipeline. To add automation, you can upgrade to custom build pipelines.

Custom build pipelines are pipelines as code, set on your component’s repository. With custom build pipelines, pull requests and commits to your main branch automatically rebuild.

By customizing your build pipeline, you can change the tasks that are included, control when those tasks update to newer versions, and accept any changes to the pipeline when you’re ready for them.

To get started, click **Manage build pipelines** from the **Overview** page. For more information on this topic, go to [Upgrading your build pipeline](../../how-to-guides/configuring-builds/proc_upgrade_build_pipeline/).

### Viewing your activity

You can view your latest commits, as well as your pipeline runs.

#### Viewing your latest commits

Because you forked your repo, you have permissions to commit to the Git repo. We like to focus on commits, rather than pipelines, so that it’s easy to correlate a developer’s work with what’s going on in the system.

To view your recent commits, go to the **Activity** tab and click **Latest commits**.

#### Viewing your pipeline runs

Didn’t fork your repo? Fret not! You can also view your activity by pipeline runs. A pipeline run is a collection of TaskRuns that are arranged in a specific order of execution.

To view your pipeline runs, go to the **Activity**, click **Pipeline runs**, and then select one of the hyperlinks in **Name**. In the previous view, you can see tasks that you can run based on the pipeline definition while the image is being inspected. You can also click an individual task to see its details.

### Viewing your application route

You can find each component’s route in the **Components** tab, next to each component’s details.

### Managing compliance with Enterprise Contract

The Enterprise Contract (EC) is an artifact verifier and customizable policy checker. You can use EC to keep your software supply chain secure and to ensure that container images comply with your organization’s policies.

For more information about EC, refer to [Managing compliance with the Enterprise Contract](../../how-to-guides/proc_managing-compliance-with-the-enterprise-contract/).

### Deploying your app

Check the status of your application in **Environments**. You can view information about your environment such as its type, deployment status, and cluster type.

An environment is a set of compute resources that you can use to develop, test, and stage your applications. There is a development environment included for you so that you can explore Konflux.

For information about creating an application with your own cluster, refer to [Creating your own environment](../../how-to-guides/managing-environments/proc_creating_your_own_environment/).

### Examining your SBOM

A software bill of materials (SBOM) is a list of all the software libraries that a component uses. You can run 'cosign' in your command line interface (CLI) to inspect the image SBOM.

For more information on this topic, go to [Inspecting SBOMs](../../how-to-guides/Secure-your-supply-chain/proc_inspect_sbom/).

### Adding collaborators to your workspace

To add other users to collaborate in your workspace, follow the instructions in [Roles and permissions](../roles_permissions/).

What’s next
-----------

To keep exploring Konflux, we recommend going to [Importing and configuring code](../../how-to-guides/Import-code/proc_importing_code/).

[Why Konflux](../../)[Getting started with CLI](../getting_started_in_cli/)