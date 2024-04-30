Deleting an application
=======================

You can delete an application if you are the owner or if you have admin access to the application.



|  | If you delete an application permanently, you delete all the components and resources from the user interface (UI) and upstream repositories. You cannot undo the deletion. |
| --- | --- |

Deleting an application in the web UI
-------------------------------------

**Prerequisites*** You have successfully signed into Konflux.
* You have at least one application.
**Procedures**1. In the console, select **My applications**.
2. Next to your applications, click **More** ![More](../../_images/more.png) and then select **Delete**.
3. In **Enter application name to delete**, enter the relevant application name and then select **Delete**.



|  | You can also delete an application by selecting **Actions > Delete Application**. |
| --- | --- |
Deleting an application using CLI
---------------------------------

**Prerequisites*** You have successfully signed into Konflux.
* You have at least one application.
**Procedures*** To delete an application, run the following command:


```
oc delete application/<the-application-name>
```
Additional resources
--------------------

* To create your first application in the web UI, refer to [Creating your first application](../../getting-started/get-started/#creating-your-first-application).
* To create your first application using CLI, refer to [Getting started in CLI](#getting-started/getting_started_in_cli).
[Managed services team onboarding](../proc_managed_services_onboarding/)[Managing multiple software versions](../proc_multiversion/)