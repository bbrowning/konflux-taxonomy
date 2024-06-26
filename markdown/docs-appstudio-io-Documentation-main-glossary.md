Glossary
========

**Konflux**  
A platform to automate the process of building, testing, and deploying applications to the hybrid cloud. Konflux offers enterprise-grade security and customizable feature sets.

**build pipeline customization**  
The ability to update and manage build pipelines for each component in an application.

**cluster**  
A Kubernetes deployment with nodes that run containerized applications and a control plane that manages the nodes.

**commit**  
A change to one or more files. In Konflux, commits that you make to a linked Git repository move through the pipeline and automatically get published.

**component**  
An image that Konflux builds from source code in a repository. One or more components that run together form an application.

**Conftest**  
A utility for testing structured configuration data. Use Conftest to validate container information.

**enterprise contract (EC)**  
A set of release policies that you apply to your managed environment. Use the EC to prevent releases that are not compliant with Supply-chain Levels for Software Artifacts (SLSA) guidelines.

**ephemeral environment**  
A temporary environment that executes each integration scenario. The system creates ephemeral environments dynamically on demand, and then removes them after it completes the build pipeline.

**integration test**  
A pipeline that you set up in GitHub. When you add components, it tests each one individually, and then tests the application as a whole.

**IntegrationTestScenario**  
A parameter that the integration service uses to test application components.

**Java build service**  
A group of utilities that accelerates build times, locates dependencies in final images, and meets product security requirements by managing the construction of Java dependencies.

**lifecycle run**  
The processes that automatically occur after a merge or pull request is resolved. These processes can include build tests, integration tests, and TaskRuns.

**managed environment**  
An application release target. A separate managed environment team, such as an Site Reliability Engineering (SRE) team, manages the environment. The environment is in an external workspace.

**managed workspace**  
A workspace that mirrors some details of an already existing workspace. Supporting teams can create a managed workspace to grant limited permissions to development teams in the production environment.

**OSBS features**  
The layered image build service, or OSBS (derived from OpenShift Build Service), is a tool for building layered images. With OSBS features, you can build base RHEL images, layered images, and the builder image itself.

**persister**  
A component that moves all of the relevant PipelineRun information, known as the Pipeline output, to an external storage that is outside of the cluster’s etcd database. The persister runs after the system completes the PipelineRun.

**pipelines as code**  
A practice that defines pipelines by using source code in Git. Pipelines as Code is also the name of [a subsystem](https://pipelinesascode.com) that executes those pipelines.

**pipeline results**  
Systems that retain the history and details of builds.

**PipelineRun**  
A collection of TaskRuns that are arranged in a specific order of execution. A valid pipeline is compliant with the customer’s enterprise contract.

**pipeline service**  
A managed service that securely runs Tekton pipelines. It also stores the metadata and pipeline logs that are related to an executed pipeline in a separate database.

**product security test**  
A test that assesses the security of build inputs and outputs with vulnerability scanning, code scanning, image testing, and result reporting. It also identifies outdated images, applications, and build pipelines.

**pruner**  
A component that removes resources that are associated with the completed PipelineRuns. The system assigns resources, such as pods, to every PipelineRun. Without a pruner, these resources remain in the cluster indefinitely, even after the system completes the PipelineRun.

**release pipeline**  
A pipeline that defines the process for validating snapshots against the enterprise contract. They also provide an array of release destinations other than GitOps deployments.

**security testing**  
A process that determines if images meet security quality standards.

**signature and provenance**  
Mechanisms that use Tekton chains to extract and store the metadata of the PipelineRuns, sign that metadata, and then store it in the image registry that is next to the component image.

**snapshot**  
A set of component and container images that specifies which components the system should deploy with which container images. The system creates a snapshot when it finishes running a component’s build pipeline.

**static environment**  
A set of compute resources that you can use to develop, test, and stage your applications before you release them. You can share static environments in all applications in the workspace.

**Supply-chain Levels for Software Artifacts (SLSA)**  
A [security framework](https://slsa.dev/) that helps prevent tampering by securing the packages and infrastructure of customers’ projects.

**task**  
One or more steps that run container images. Each container image performs a piece of construction work.

**TaskRun**  
A process that executes a task on a cluster with inputs, outputs, and execution parameters. The system creates a TaskRun on its own, or as a part of a PipelineRun for each task in a pipeline.

**Tekton**  
A Knative-based framework for CI/CD pipelines. Tekton is decoupled which means that you can use one pipeline to deploy to any Kubernetes cluster in multiple hybrid cloud providers. Tekton stores everything that is related to a pipeline in the cluster.

**Tekton chains**  
A mechanism to secure the software supply chain by recording events in a user-defined pipeline.

**Tekton integration testing**  
A process that uses Tekton tasks to support the setup and execution of dynamic application tests against container images.

**workspace**  
A storage volume that a task requires at runtime to receive input or provide output.

[Java build service components](../concepts/java-build-service/java-build-service-components/)[Contribute to documentation](../contribute/)