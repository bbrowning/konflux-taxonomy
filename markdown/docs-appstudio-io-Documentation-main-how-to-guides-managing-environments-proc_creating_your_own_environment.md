Creating your own environment
=============================

You can configure Konflux to deploy applications to your own cloud-hosted cluster, outside the default development environment. By using this option to bring your own cluster (BYOC), you can deploy your applications to a static environment that meets your specific needs. And if you bring your own cluster, you can still access all the features and benefits of Konflux.

Prerequisites* You must have credentials with full read and write access to the namespace for your cluster.
ProcedureTo create your own static environment, you first need to create a functional `kubeconfig` file. Then, using that file, you add the cluster as a new environment in the Konflux UI.

1. In your preferred text editor, create a `kubeconfig` file locally based on the following example:


```
apiVersion: v1clusters:- cluster:    server: https://api.sandbox-m2.ll9k.p1.openshiftapps.com:6443 **(1)**  name: api-sandbox-m2-ll9k-p1-openshiftapps-com:6443 **(2)**contexts:- context:    cluster: api-sandbox-m2-ll9k-p1-openshiftapps-com:6443 **(3)**    namespace: rhn-support-csears-dev **(4)**    user: rhn-support-csears/api-sandbox-m2-ll9k-p1-openshiftapps-com:6443 **(5)**  name: rhn-support-csears-dev/api-sandbox-m2-ll9k-p1-openshiftapps-com:6443/rhn-support-csears **(6)**current-context: rhn-support-csears-dev/api-sandbox-m2-ll9k-p1-openshiftapps-com:6443/rhn-support-csears **(7)**kind: Configpreferences: {}users:- name: rhn-support-csears/api-sandbox-m2-ll9k-p1-openshiftapps-com:6443 **(8)**  user:    token: sha256~<remainder of token omitted> **(9)**
```


| **1** | The `server` parameter is the web address of the API server that you use to access your cluster through the CLI. In a web UI, you can find this address by requesting the CLI login command, or searching for the general cluster information. |
| --- | --- |
| **2** | This `name` parameter is the cluster name. It is the same as the server address, only without `https://` at the beginning. |
| **3** | This `cluster` parameter is also the cluster name. |
| **4** | This `namespace` parameter is the namespace of your cluster. |
| **5** | This `user` parameter is your cluster username followed by the cluster name. |
| **6** | This `name` parameter is the namespace of your cluster followed by the cluster name, followed by your username. |
| **7** | This `current-context` parameter should be the same as the `name` parameter before it. |
| **8** | This `name` parameter is your username followed by the cluster name. |
| **9** | This SHA token is the token you use to login to your cluster through the CLI. In a web UI, you can find this token by requesting the CLI login command. |
2. In the Konflux UI, go to **Environments** > **Create Environment**.
3. Enter a name for the new environment.
4. Complete all the required fields for **Cluster information**:


	1. For **Select cluster**, select that you are bringing your own cluster.
	2. For **Cluster type**, select **Non-OpenShift** or **OpenShift**.
	3. Upload your `kubeconfig` file, or paste its contents into the space provided.
	4. Specify the namespace for the cluster that you are using.
5. Select **Create environment**.
6. Confirm that your environment is created and is accessible under **Environments**.
TroubleshootingIf any errors occur while creating your environment, complete the following steps:

1. Make sure the token you provided in your `kubeconfig` file is valid. If the token in your `kubeconfig` file has expired, log in to your cluster and request a new token.
2. Make sure that you entered the correct values in the right places in your `kubeconfig` file. When you read the example file, you might easily mistake the namespace, `rhn-support-csears-dev`, for the username, `rhn-support-csears`, and vice versa.
3. Make sure that your cluster supports another Pod for deploying your application.
4. If you do not find any errors in your `kubeconfig` file, go to **Environments** in the Konflux UI, select the three dots next to the environment you created, select **Delete**, and then create a new environment.
5. If that still does not work, try clearing the cache of your browser. If you are using Chrome, try deleting and creating the environment again using an Incognito window.
Additional resources* If you have the read and write access rights in your cluster to assign the `cluster-admin` role to a Service Account, review the [BYOC step by step](https://gist.github.com/jannfis/07095088c0b5a10681db3b48fd197641) document to create a `kubeconfig` with a token that doesn’t expire.
[Overview of Konflux environments](../con_overview_of_environments/)[Managing a security fix](../../managing-applications/proc-managing_applications/)