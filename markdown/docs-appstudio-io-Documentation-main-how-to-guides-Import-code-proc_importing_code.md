Importing and configuring code
==============================

After you click **Create application**, the **Grab some code** page opens. From here, choose one of the following source code options to begin building your application:

* **Bring in your own code**
* **Start with a sample**
Using a code sample
-------------------

1. Optional: In the code sample **Search** field, begin typing the name of the code you want to work with. If Konflux has code samples in that language stack, the code sample results filter accordingly.
2. When you see a language stack or framework that you want to work with, click **Import sample**.


	* Optional: If you click **Open Git repository**, a new tab opens to the GitHub repository for the code framework you chose.
	* When you click **Import sample**, Konflux creates and deploys a new application with the sample code you chose. Check out the open **Overview** tab to monitor your continuous integration/continuous deployment (CI/CD) activity.


|  | When you create an application from a code sample, Konflux names your application for you. |
| --- | --- |

Importing code from your GitHub repository
------------------------------------------

To use your own code to build your application, complete the following steps:

1. Enter the link to your repository in the **Git repository URL** field. Note that this should be a public repository. Konflux verifies your URL right away. You don’t even have to press **Enter**.
2. Optional: Add a **Git reference** to point to code in a specific branch, tag, or commit that you want to use to build your application.
3. Optional: Indicate a **Context directory** to specify the subdirectory for the source code you want to use.


|  | Make sure this path is correct. You might get an error if your build context folder is your root directory but your Dockerfile is in a subdirectory of that folder. If you have a Dockerfile, you can check its path in the **Build & deploy configuration** section. |
| --- | --- |

4. Click **Import code**.


|  | If you want to use a custom pipeline build, or to grant access to and install the Konflux GitHub app on the repository you indicated, you must have the necessary GitHub permissions. If you don’t own that repository, or if you don’t have the necessary GitHub permissions, you must fork that repository and then specify the new fork URL to add a new component. |
| --- | --- |



|  | If Konflux can’t access your Git repository, see [Importing code from a private GitHub repository](#importing-code-from-private-repo) for help. |
| --- | --- |

Konflux scans and analyzes your Git repository to determine how many components to add to your application and which runtime to use. The types of files in your repository, and also your Git directory file hierarchy, determine the number and type of components to add. For example, Konflux looks for devfiles and Dockerfiles, and also language-specific build configuration files like pom.xml for Java or package.json for Node.js.

Konflux can build applications that are written in the following language stacks and frameworks:



| Language | Framework |
| --- | --- |
| Java | Spring Boot, Quarkus |
| JavaScript | Node.js, Express |
| Python | Flask |
| Go | N/A |

### Importing code from a private GitHub repository

To use your code from a private repository to build your application, complete the following steps:

1. Enter the link to your private repository in the **Git repository URL** field. Konflux displays the following message: “Looks like your repository is private, so we’re not able to access it.”
2. Grant Konflux access to your repository.


	1. On the **Grab some code** page, enter the URL to your repository. After Konflux detects that it needs access, the **Authorization** section opens.
	2. Under **Authorization**, click **Sign in**. The **OAuth Redirection** page opens in a new tab and redirects you to **GitHub Authorize OAuth**.


|  | If you’re not already logged in to GitHub, follow the login prompt. If you configured two-factor authentication, GitHub might prompt you to enter a one-time authentication code. |
| --- | --- |

3. Click **Authorize *redhat-appstudio***. A **Login successful** page opens, which you can close.
4. On the **Grab some code** page, enter your repository URL again. Konflux checks its access to your repository.
5. After Konflux validates access, click **Import code**.
What’s next**Configure your components for deployment** opens. From here, configure your components before you deploy them. You can also review or change any values that Konflux populated for you. When you’re finished here, you’re one click away from creating your application.

Reviewing and configuring components
------------------------------------

If you imported your own code, from the **Review and configure for deployment** view, make sure to define, review, or change your application and component settings before you finish importing. You can rename a component here, too.

1. Make sure that **Component name** is correct. Click the GitHub link under this field if you want to check your repository URL.
2. Confirm that Konflux detected the right **Runtime**. If so, you should notice that the suggested deployment options are appropriate. If you want to change your runtime, expand the menu next to your runtime name and make a selection.


|  | If you change the runtime, your component builds and deploys using the runtime devfile instead of the repository devfile or Dockerfile. |
| --- | --- |

In the **Build & deploy configuration** section, look over these fields:

3. **Target port**: Is it correct? If not, click in the field to modify it.
4. **Dockerfile**: If you specified **Dockerfile** as your runtime, make sure Konflux detected the right one. Click in the field if you need to modify it.
5. **Default build pipeline**: To specify how to trigger rebuilds, toggle to choose either the default build pipeline or a custom one.


	1. **Default build pipeline**: This runs faster because it makes only critical image checks. Consider starting here to make sure Konflux can successfully build and deploy your component.
	2. **Custom build pipeline**: This is triggered when you make commits to your source code repository. This pipeline runs more checks and security scans than the default pipeline, but it takes a bit more time because it’s more thorough. **NOTE:** To use a custom pipeline, you must be the owner of your repository so that you can authorize the installation of our application in your GitHub instance and then grant the app access to your repository. If someone else owns your repository, fork it, then go back to the **Add components** page and start again.
6. **CPU**, **Memory**, and **Instances**: Choose how many of each of these you want for your application, and in what unit, depending on your deployment requirements. **Instances** refers to the number of instances of your system image.
7. In the **Environment variables** section, enter a variable name and value to customize how Konflux deploys your application.
When you’re satisfied with your component configuration settings, click **Create application**.

* After you create your application, you can adjust your configuration settings anytime from the **Application** view.
* From the **Secrets** page, you can add a build or deployment secret to keep your data private. For more information about secrets, see [Creating secrets for your builds](https://redhat-appstudio.github.io/docs.appstudio.io/Documentation/main/how-to-guides/configuring-builds/proc_creating-secrets-for-your-builds/).
Resolving issues with importing code
------------------------------------

When you import code, Konflux analyzes your repository to determine the right runtime to use to build and deploy your application. In some cases, however, Konflux is unable to find the right runtime, and this can cause your code import to fail. These are the most common causes of issues with importing code to Konflux:

* **Your repository contains a Dockerfile in an unexpected directory.**

If Konflux finds a Dockerfile in your repository, it determines that a Dockerfile runtime is the most suitable for building and deploying you application. However, if the Dockerfile is not saved in one of the following expected locations, an error in determining the right runtime for your components can occur:

Expected Dockerfile locations
	+ Dockerfile
	+ docker/Dockerfile
	+ .docker/Dockerfile/build/Dockerfile
	+ Containerfile
	+ docker/Containerfile
	+ .docker/Containerfile/build/Containerfile
	
	**Solutions**
	+ On the **Review and configure for deployment** page, make sure **Runtime** is set to **Dockerfile**, then verify that you saved your Dockerfile in one of the expected directories.
	+ In the **Build & deploy configuration** section, in the **Dockerfile** field, confirm that the file path is correct.
	
	
	
	|  | Test your Dockerfile in a local environment first to make sure it’s valid. |
	| --- | --- |
* **Your repository does not contain a Dockerfile or devfile.**

If your code import fails because your repository is missing either a Dockerfile or devfile, check one of the following readme files for guidance, depending on the runtime you want to build and deploy with. These readme files provide details like required ports, file locations, commands, and more.

**Solutions**


	+ [Go](https://github.com/devfile-samples/devfile-sample-go-basic.git)
	+ [Node.js](https://github.com/nodeshift-starters/devfile-sample.git)
	+ [Python](https://github.com/devfile-samples/devfile-sample-python-basic.git)
	+ [Quarkus](https://github.com/devfile-samples/devfile-sample-code-with-quarkus.git)
	+ [Spring Boot](https://github.com/devfile-samples/devfile-sample-java-springboot-basic.git)
* **Your repository contains a devfile, a Dockerfile, and a Kubernetes YAML file.**

Konflux looks for a devfile to get custom instructions for building and deploying your application. If your devfile references both a Dockerfile and a Kubernetes YAML file, your code import could fail if those two resources are not accessible at the file locations your devfile points to.

**Solutions**


	+ Make sure that your `devfile.yaml` points to the correct directories for both your Dockerfile and your Kubernetes YAML file.
	+ Make sure that neither of these resources is in a private repository that requires access authentication.
	+ Make sure that your devfile is in one of these expected locations:
	
	Expected devfile locations
		- devfile.yaml
		- .devfile.yaml
		- .devfile/devfile.yaml
		- .devfile/.devfile.yaml
* **Your repository does not fit within the predefined Konflux supported runtime list.**

Some repositories require custom build or deployment instructions; for example, a deployment that includes a Kubernetes resource other than a YAML file.

**Solutions**


	+ **Configure a custom build.** Include a Dockerfile that can build your application, then save it to one of the [expected Dockerfile locations](#expected-dockerfile-locations). **Note:** If your build is custom but your deployment is not, you do not have to include a `devfile.yaml` file in your repository.
	+ **Configure a custom deployment.** Include the following files in your repository to provide Konflux with custom deployment instructions:
	
	
		- A standard Kubernetes YAML file
		- A custom-build Dockerfile
		- A devfile that points to your Kubernetes YAML file and Dockerfile. **Note:** Make sure that your devfile is in one of the [expected devfile locations](#expected-devfile-locations).
		
		
		
		|  | For more information about devfile contents requirements, see the "What is outerloop?" section of [Devfile.io: Innerloop versus outerloop](https://devfile.io/docs/2.2.0/innerloop-vs-outerloop). |
		| --- | --- |
* **Konflux couldn’t detect a port number.**

Konflux detects your application port number when it’s looking for your repository components.

**Solution:** From the **Review and configure for deployment** view, in the **Build & deploy configuration** section, make sure your target port number is correct.
* **Konflux couldn’t detect the appropriate runtime.**

**Solution:** Select a predefined runtime type from the **Review and configure for deployment** view. Make sure you meet all of the Konflux [repository requirements](#repository-requirements) for the runtime you select, or configure your own [custom build and deployment instructions](#custom-build).
### Creating a Red Hat Container Registry token

After importing your code, configure a Red Hat Container Registry token to improve your application-building experience. You can access this token by creating Red Hat registry service accounts. The registry service accounts enable you to retrieve content from **registry.redhat.io**. **Registry.redhat.io** helps you manage the automation of your applications.

ProcedureCreate the Red Hat Container Registry token by following these steps:

1. Go to [registry service accounts](https://access.redhat.com/terms-based-registry/#/).
2. Create a registry service account by clicking **New Service Account**. You are taken to the page, **Create a New Registry Service Account**.
3. Fill in the **Name** and **Description** field.
4. Click **Create**. You are taken to the page, **Token Information**.
5. Click **OpenShift Secret**.
6. Download the secret for the new service account
7. If click **view its contents,** it should have the form:

```
apiVersion: v1kind: Secretmetadata:  name: <name-corresponding-to-the-service-account>data:  .dockerconfigjson: MTEwNzAxOTl8-redacted-c2Jvc2U6ZZlNDQ=type: kubernetes.io/dockerconfigjson
```
1. Change the name in the downloaded file from the service account name to **registry-redhat-io-docker** and save the file
### Configuring your application to use a Red Hat Container Registry token

After creating the Red Hat Container Registry token, include the token in your application. When your application includes the Red Hat Container Registry token, you can access **registry.redhat.io** which improves your automation.

Procedure1. Edit the downloaded secret to change the name in the downloaded file from the service account name to **registry-redhat-io-docker** and save the file.
2. From your command line, ensure that you are in your workspace’s project by running the command `oc project`.


	1. If the project returned is not the proper appropriate project, see all available projects by running the command `oc get projects`. Change to the proper project by running the command `oc project <project-name>`.
3. From your command line, create the secret from the downloaded file by running the `oc create -f ~/path/to/secret.yaml` command.
4. From your command line, run the `oc secrets link appstudio-pipeline registry-redhat-io-docker` command.


	1. If you need to delete the secret, you will also need to unlink it with the command `oc secrets unlink appstudio-pipeline registry-redhat-io-docker` before builds can work again.
5. Retrigger the Konflux pipeline.
Additional resourcesFor information about importing and configuring code to Konflux using the CLI, see [Getting started with CLI](https://redhat-appstudio.github.io/docs.appstudio.io/Documentation/main/getting-started/getting_started_in_cli/#getting-started-in-the-cli).

[Getting started with CLI](../../../getting-started/getting_started_in_cli/)[Upgrading to a custom build pipeline](../../configuring-builds/proc_upgrade_build_pipeline/)