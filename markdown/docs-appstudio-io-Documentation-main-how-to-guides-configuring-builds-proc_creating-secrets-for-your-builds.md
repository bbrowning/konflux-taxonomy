Creating secrets for your builds
================================

When you building your pipelines, you might want to add tasks that require **secrets** in order to access external resources.



|  | One such task is the [sast-snyk-check](https://github.com/redhat-appstudio/build-definitions/tree/main/task/sast-snyk-check) task that that uses the third-party service [snyk](https://snyk.io/) to perform static application security testing (SAST) as a part of the default Konflux pipeline. Use this procedure to upload your snyk.io token. Name the secret `sast_snyk_task` so that the snyk task in the Konflux pipeline will recognize it and use it. |
| --- | --- |

Procedure1. In Konflux, from the left navigation menu, select **Secrets**.
2. From the **Secrets** page, click **Add secret**.
3. From the **Add secret** page, choose what stage of your application’s development you want to create a secret for: **Build** or **Deployment**.
4. Select a secret type:


	* **Key/value secret**
	* **Image pull secret**
	* **Source secret**
5. For **Secret name**, enter a unique name for your secret.
6. Under **Key/value secret**, expand **Key/value 1**, then enter a key.
7. For **Upload the file with value for your key or paste its contents**, do one of the following:


	* Click **Upload** to browse to, select, and upload the file that contains your key value.
	* Drag the file that contains your key value into the space under **Upload**.
	* Paste the contents of the file that contains your key value into the space under **Upload**.Click **Clear** to remove the contents of the space under **Upload**.
8. Optional: Click **Add another key/value**.
9. Optional: Under **Labels**, add a label to tag or provide more context for your secret.
10. Click **Add secret**.
[Customizing the pipeline](../proc_customize_build_pipeline/)[Configuration as Code](../../configuration-as-code/proc_configuration_as_code/)