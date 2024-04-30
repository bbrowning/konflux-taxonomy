Creating a team workspace
=========================

When you first login to Konflux, you are granted a personal workspace dedicated to your username. But, sometimes, you want a workspace to organize work for your **team**, not just yourself.

Because workspace creation is tied to SSO login identities in Konflux, in order to create a team workspace you need to create and login as an SSO identity that bears the same name as the team

Key steps include:

* **Create an SSO account for the team:** A prerequisite, giving Konflux the information it needs to create the team workspace.
* **Login to Konflux and join the waitlist:** Triggering the creation of the workspace.
* **Add team members to the shared workspace:** Allowing the team to get down to work.
**Prerequisite*** You are [logged out](https://www.redhat.com/wapps/ugc/sso/logout) of the Konflux SSO provider.
**Procedure**1. As in [Getting started](../../../getting-started/get-started/), visit [Konflux](https://console.redhat.com/preview/hac/application-pipeline).
2. When prompted to login, select the link to register for a new account.
3. Follow the account creation steps.


|  | For the login name, choose a name that reflects the identity of your team. This will become your team’s workspace name. |
| --- | --- |



|  | For the email address, choose an address that you can access. Use a team mailing list, or a modified form of your personal email like `<your_username>+<team_name>@<domain>.com`. |
| --- | --- |

1. Once the account is created, use it to log in to [Konflux](https://console.redhat.com/preview/hac/application-pipeline).
2. As in [Getting started](../../../getting-started/get-started/), join the waitlist.
3. Once approved, visit the [User Access](https://console.redhat.com/preview/application-pipeline/access) section of the user interface to grant the [owner role](../../../getting-started/roles_permissions/) to your normal user identity.
4. [Log out](https://www.redhat.com/wapps/ugc/sso/logout) and log back in as your normal user identity, and confirm you have access to the team workspace via the workspace switcher.


|  | Once your normal user identity is granted admin, you should be able to add and manage other team members' access as your normal user identity by using the **User Access** section of the user interface. |
| --- | --- |

[Managing a security fix](../../managing-applications/proc-managing_applications/)[Inspecting SBOMs](../../Secure-your-supply-chain/proc_inspect_sbom/)