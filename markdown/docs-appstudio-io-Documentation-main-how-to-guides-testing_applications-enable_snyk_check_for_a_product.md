Enabling a Snyk task
====================


> The `sast-snyk-check` task uses the Snyk Code tool to perform static application security testing (SAST).Specifically, the Snyk check scans an application’s source code for potential security vulnerabilities,including SQL injection, cross-site scripting (XSS), and code injection attack vulnerabilities.


> |  | You can run a Snyk task only if you have a Snyk token stored in a namespace secret.You should also include the name of your secret in the **snyk-secret** pipeline parameter. |
> | --- | --- |

Enabling a Snyk task
--------------------

1. Register for a Snyk account or log in at <https://app.snyk.io/>.
2. Get a Snyk token.


	1. In the lower left of the home page, click your name, then select **Account settings**.
	2. From the Account Settings page, select **General**, which is the default, then **Auth Token**.
	3. Under the **Auth Token** section, click **Click to View** to see the **KEY** value of the automatically generated token.
3. Enable Snyk Code.


	1. From the left panel, go to **Settings** > **Snyk Code**, then scroll to the **Enable Snyk Code** section.
	2. Toggle **Disabled** to **Enabled**.
	3. Click **Save** changes.
4. Add your new secret to your workspace.


	1. Log in to the [Red Hat Hybrid Cloud Console Konflux Overview page](https://console.redhat.com/preview/application-pipeline).
	2. From the left menu, click **Secrets**.
	3. Click **Add secret**.
	4. The **Add secret** page displays options for your new secret. Specify the following:
	
	
		1. For **Secret for**, select **Build**.
		2. From the **Secret type** drop-down menu, choose **Key/value secret**.
		3. From the **Secret name** drop-down menu, select **snyk-secret**.
		4. Paste your Snyk token into the **Upload the file with value for your key or paste its contents** field.
		5. Click **Add secret** to save it.
You’ve enabled the Snyk task for your build pipeline.

Additional resources
--------------------

For more information about Snyk, see [the Snyk website](https://snyk.io/product/snyk-code/).

[Surface-level tests](../surface-level_tests/)[Adding an integration test](../proc_adding_an_integration_test/)