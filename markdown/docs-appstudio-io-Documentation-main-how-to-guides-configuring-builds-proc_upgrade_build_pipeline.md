Upgrading to a custom build pipeline
====================================

By default, Konflux builds the components of your applications using, as the name suggests, the default build pipeline. This pipeline offers quick and easy containerized deployment. It also secures your supply chain, by conforming to the specification for SLSA Build Level 3.

However, there are three reasons you might want to upgrade your build pipeline to a custom build:

* Customize: Upgrading the build pipeline enables you to tailor the build process that Konflux uses for the components of your application, to better meet your specific needs.
* Reinforce security: When you upgrade, Konflux adds a variety of security checks and scans on your pipeline that get run on each build.
* Continuous integration: Upgraded build pipelines automatically rebuild your components every time a new commit is added to a pull request or merged into the configured branch of their repositories.
Prerequisites* You must have an application that Konflux has successfully built and deployed using the default build pipeline.
ProcedureTo upgrade the build pipeline:

1. In the **Overview** tab of your application, scroll down and select **Manage build pipelines**.
2. If you have not already installed the Konflux GitHub application, select Install GitHub application on the “Manage build pipelines” popup page.



|  | If you want to restrict the GitHub application’s access to certain repositories only, use the Only select repositories option in GitHub during the installation. |
| --- | --- |
3. Returning to the “Manage build pipelines” page in Konflux, for any component whose build pipeline you would like to upgrade, select **Send pull request**.
4. Select **Merge in GitHub**.
5. In GitHub, merge the pull request from the “red-hat-konflux” bot.
6. Let Konflux complete another PipelineRun for the newly-upgraded build pipeline.
VerificationConfirm that most of the build pipeline tasks that Konflux previously skipped are now included in the recent PipelineRun:

1. Go to **Activity > Pipeline runs**.
2. Select the most recent **PipelineRun**.
3. View the build pipeline tasks and scroll down to view the vulnerabilities scan, which summarizes the results of the `clair-scan`.
Continuous IntegrationAfter upgrading the build pipeline, PipelineRuns will be started to build and test commits in pull requests. The status of the completed PipelineRuns will be visible in the pull requests.



|  | Konflux sets an expiration date for images produced from pull request commits. The produced images will be deleted fromquay.io after five days. In order to prevent an image reference from becoming invalid, the image should either be copied to an externallocation or the pull request should be merged, triggering a new image build without an expiration set. |
| --- | --- |

UpdatesIf you upgrade your build pipeline for a component, then whenever we release a new `build-definition` for upgraded pipelines, the Konflux bot submits a pull request (PR) to the git repository of your component. These PRs only change the `.tekton` directory of the component repository; they do not alter the source code specific to your component in any way.

When you see a PR from the Konflux bot, please merge it to keep your pipeline updated. If you do not merge these PRs, Konflux might not be able to build or test your components correctly.

SecurityTo further reinforce the security of your custom build pipeline, complete the following steps:

* Add an `OWNERS` file to the root of your repository and list trusted contributors there.


	+ To learn more, see Kubernetes docs about [OWNERS files](https://www.kubernetes.dev/docs/guide/owners/).
* Review all pull requests carefully. Avoid commenting `/ok-to-test` on PRs from untrusted authors. The `/ok-to-test` comment runs the PipelineRun, and malicious code in a PR can change your build and compromise the security of your application.


	+ To learn more about running the PipelineRun, see the [Running the PipelineRun guide](https://pipelinesascode.com/docs/guide/running/#running-the-pipelinerun) from Pipelines as Code docs.
* Consider changing the PipelineRun definition source by setting the `pipelinerun_provenance` setting to `default_branch`. With this setting, Pipelines as Code uses the PipelineRun definition from the default branch of the repository, usually `main` or `master`, and only contributors with default branch merge rights can modify the PipelineRun.

If you don’t set `pipelinerun_provenance`, you allow the default behavior: the PipelineRun definition is fetched from the branch where the PipelineRun event is triggered, and [submitters who are allowed to run a PipelineRun](https://pipelinesascode.com/docs/guide/running/) can modify the PipelineRun. External submitters cannot run a PipelineRun and need a repository owner to comment `/ok-to-test` on a PR. In these cases `pipelinerun_provenance: default_branch` still applies, and the PipelineRun definition is taken from the default branch.

Testing changes to the PipelineRun is easier with the default behavior because PipelineRun changes are tested when a user submits a pull request, before the merge.

Setting the `pipelinerun_provenance` setting to `default_branch` is more cautious because PipelineRun changes are tested only after a repository owner reviews and merges them. We recommend that repository owners review all changes to PipelineRun very carefully before the merge. If a proposed change doesn’t work correctly, a repository owner might need to merge a few changes to debug the PipelineRun.


	+ To learn more about setting the PipelineRun definition source, see [PipelineRun definition provenance](https://pipelinesascode.com/docs/guide/repositorycrd/#pipelinerun-definition-provenance).
[Importing and configuring code](../../Import-code/proc_importing_code/)[Customizing the pipeline](../proc_customize_build_pipeline/)