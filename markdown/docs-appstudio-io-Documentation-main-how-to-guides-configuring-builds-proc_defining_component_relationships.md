Defining component relationships
================================

When an application includes multiple components, their repositories might contain references to image builds of another component. For instance, an application might include multiple child components that, using a Dockerfile `FROM` clause, reference the image build of a common parent.

In such instances, whenever you build a new image of the common parent component, you need to update the references to it. Specifically, you need to copy and paste the pullspec and image digest of that new image to your other source repositories. This process is tedious and error-prone.

If you build an application with Konflux and make references between components with image digests (`sha256:…​`), Konflux can automatically generate pull requests to update those references. To use this functionality, simply define the relationships between your components in the Konflux UI.

ProcedureTo define the relationships between components in an application, complete the following steps in the Konflux UI:

1. Navigate to your application.
2. On any tab, use the **Actions** drop-down menu to select **Define component relationships**.


	1. Alternatively, go to the **Components** tab and select the **Define component relationships**.
3. In the **Component relationships** window, select one component from the **Select a component** drop-down menu.
4. Select **Nudges** or **Is nudged by**, depending on the relationship you wish to define.



|  | Component A nudges Component B (or Component B is nudged by Component A) if Component B contains a reference by image digest to a build of Component A. |
| --- | --- |
5. Use the remaining drop-down menu to choose which other components belong to this relationship.
6. To define multiple relationships, select **Add another component relationship**.
7. Once you have defined all necessary relationships, select **Save relationships**.
VerificationTo verify a relationship between your components, complete the following steps:

1. Go to the **Components** tab for your application.
2. Select a component that belongs to the relationship you defined.
3. Scroll to the end of the page and select **Show related components**.
4. Merge a pull request for Component A. When the build completes, you should see a new pull request appear for Component B. This new pull request contains the image digest for the new build of Component A.
TroubleshootingTo resolve any issues with relationships between components, complete the following steps:

1. On any tab, use the **Actions** drop-down menu to select **Define component relationships**. If you do not see the relationship, try to define it again and then make sure to select **Save relationships**.
2. Ensure that the existing references in the repositories of your components are correct.
[Prefetching package manager dependencies for hermetic build](../../proc_prefetching-dependencies-to-support-hermetic-build/)[Preventing redundant rebuilds](../proc_preventing_redundant_rebuilds/)