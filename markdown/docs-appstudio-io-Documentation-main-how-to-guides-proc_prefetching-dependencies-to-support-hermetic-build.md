Prefetching package manager dependencies for a hermetic build
=============================================================

In Konflux, you can run a hermetic build by restricting network access to the build. Consequently, a build might fail if it can’t retrieve dependencies from a repository. To address this, Konflux uses Cachi2 to prefetch package manager dependencies for supported languages. For every build, Cachi2 also generates a software bill of materials (SBOM) of all dependencies included in your builds, for better transparency and build maintainability. For more information about SBOMs, see [Inspecting SBOMs](https://redhat-appstudio.github.io/docs.appstudio.io/Documentation/main/how-to-guides/Secure-your-supply-chain/proc_inspect_sbom/).



Table 1. Supported languages
| **Language** | **Package manager** |
| --- | --- |
| Go | `gomod` |
| Python | `pip` |
| Node.js | `npm` |

Enabling prefetch builds for `gomod`
------------------------------------

Prerequisites* You have an [upgraded build pipeline](https://redhat-appstudio.github.io/docs.appstudio.io/Documentation/main/how-to-guides/configuring-builds/proc_upgrade_build_pipeline/).
* You have a `go.mod` file in your repository that lists all the dependencies.
ProcedureTo create a hermetic build for a component, complete the following steps:

1. Go to the `.tekton` directory in your component repository and find the `.yaml` files related to both the `**pull request**` and `**push**` processes.
2. To configure the hermetic pipeline in both `.yaml` files, add the following hermetic pipeline parameters to the `spec.params` sections:


```
spec:    params:        -   ...        -   name: prefetch-input            value: '{"type": "gomod", "path": "."}' **(1)**
```


| **1** | The `**prefetch-input**` parameter specifies the path to the directory that has the lockfile and the package metadata files. In this example, the `.` indicates that the package manager lockfile is in the repository root. Additionally, if you have multiple directories, you can provide the path to those directories in the JSON array format. For example, `[{"path": ".", "type": "gomod"}, {"path": "subpath/to/the/other/directory", "type": "gomod"}]`. |
| --- | --- |
3. Create a pull request by committing your changes to the repository of the component.
4. Review and merge the pull request.
Verification* From the Konflux **Applications** view, go to **Activity > Pipeline runs**.


	+ Go to the pipeline run with **Build** in the **Type** column and confirm that the `pre-fetch dependencies` stage displays a green checkmark. This indicates that the build process successfully fetched all dependencies.
* From the Konflux **Applications** view, go to **Activity > Latest commits**.
Enabling prefetch builds for `pip`
----------------------------------

Cachi2 supports pip by parsing of `pip` requirements files, including but not limited to, `requirements.txt` files placed in the root of your repository. By generically parsing `pip` requirements files, Cachi2 downloads the specified dependencies.



|  | The requirements file can have a different name because you can use multiple files to provide the dependencies. These requirements files function as lockfiles, encompassing all transitive dependencies. You must actively pin each transitive dependency listed in the requirements file to a specific version. |
| --- | --- |

Prerequisites* You have an [upgraded build pipeline](https://redhat-appstudio.github.io/docs.appstudio.io/Documentation/main/how-to-guides/configuring-builds/proc_upgrade_build_pipeline/).
* You have an environment that closely matches the environment in the container build, meaning it has the same operating system and the same python *$major.$minor* version.
* You have installed the [pip-tools](https://github.com/jazzband/pip-tools) package.
ProcedureTo create a hermetic build for a component, complete the following steps:

1. Download the [pip\_find\_builddeps.py](https://raw.githubusercontent.com/containerbuildsystem/cachito/master/bin/pip_find_builddeps.py) script directly from GitHub.



|  | This script has no runtime dependency other than `pip`. |
| --- | --- |
2. Add the script that you downloaded in a directory that is already included in your $PATH. For example, you can use the `~/bin` directory in your home folder. Ensure that it exists or create it if needed. To add it to the $PATH permanently, you can modify the shell configuration file (for example, `.bashrc`, `.bash_profile`, or `.zshrc`) and restart the terminal after appending the following line:


```
export PATH="$HOME/bin:$PATH"
```
3. Open the terminal and go to the directory where you placed the `pip_find_builddeps.py` script and run the following command to make it executable:


```
chmod +x pip_find_builddeps.py
```
4. Go to your component’s source code.
5. Review the root of your repository for a metadata file, for example, `pyproject.toml`, `setup.py`, or `setup.cfg`. If there is no metadata file, create one, because Cachi2 looks for the name and version of your project in the metadata files.


```
[metadata]name = "my_package"version = "0.1.0"
```


|  | Instead of a `pyproject.toml` file, you can also create a `setup.py` or `setup.cfg` file. For information about the metadata of these files, see [Project metadata](https://github.com/containerbuildsystem/cachi2/blob/main/docs/pip.md#project-metadata). |
| --- | --- |
6. Generate a fully resolved `requirements.txt` file that contains all the transitive dependencies and pins them to a specific version and hash by using the following command:


```
$ pip-compile pyproject.toml --generate-hashes
```


|  | * To successfully run the previous command, your environment must be as close as possible to the environment in the container build. That is, the environment should have the same operating system and the same Python *$major.$minor* version. 	* The previous command assumes that you have defined project dependencies in `pyproject.toml`. However, if you have defined the project dependencies in either the `setup.py`, `requirements.txt`, or `requirements.in` files, make sure you update the command accordingly. |
| --- | --- |
7. Add the `requirements.txt` file to the root of your component source code.
8. In the root of your repository create a `requirements-build.in` file.
9. Copy the build system requirements from the `pyproject.toml` file to the `requirements-build.in` file.
10. Run the `pip_find_builddeps.py` script and `pip-compile` the outputs by using the following command:


```
$ pip_find_builddeps.py requirements.txt \--append \--only-write-on-update \-o requirements-build.in
```
11. Use the `pip-compile` command to convert the `requirements-build.in` file in to the `requirements-build.txt` file by using the following command:


```
$ pip-compile requirements-build.in --allow-unsafe --generate-hashes
```
12. Add the `requirement-build.txt` file to your project. It does not require any changes to your build process.



|  | `pip` automatically installs the build dependencies when needed for explicit installation. The purpose of the `requirement-build.txt` file is to enable Cachi2 to fetch the build dependencies and provide them to `pip` for offline installation in a network-isolated environment. |
| --- | --- |
13. Go to the `.tekton` directory and locate the `.yaml` files related to the `**pull request**` and `**push**` processes.
14. Configure the hermetic pipeline.


	1. Add the following hermetic pipeline parameters in both the `.yaml` files:
	
	
	```
	spec:    params:        -   ...        -   name: prefetch-input            value: '{"type": "pip", "path": "."}' **(1)**
	```
	
	
	| **1** | The `**prefetch-input**` parameter specifies the path to the directory that has the lockfile and the package metadata files. In the previous example, the `.` indicates that the package manager lockfile is located in the root of the repository. Additionally, if you have multiple directories, you can provide the path to those directories in the JSON array format. For example, `[{"path": ".", "type": "pip"}, {"path": "subpath/to/the/other/directory", "type": "pip"}]`. |
	| --- | --- |
	
	
	
	|  | * By default, Cachi2 processes `requirements.txt` and `requirements-build.txt` at a specified path. 	* When adding these parameters, you can safely ignore the default values for the [`pipelineSpec.params`](https://github.com/burrsutter/partner-catalog-stage/blob/e2ebb05ba8b4e842010710898d555ed3ba687329/.tekton/partner-catalog-stage-wgxd-pull-request.yaml#L90) in the `.yaml` files. |
	| --- | --- |
	2. Optional: For requirements files without default names and path, add the following hermetic pipeline parameters in both the `.yaml` files:
	
	
	```
	spec:    params:        -   ...        -   name: prefetch-input            value: '{"type": "pip", "path": ".", "requirements_files": ["requirements.txt", "requirements-extras.txt", "tests/requirements.txt"]}' **(1)**
	```
	
	
	| **1** | The `**prefetch-input**` parameter specifies the path to the directory that has the lockfile and the package metadata files. In the previous example, the `.` indicates that the package manager lockfile is located in the root of the repository. Additionally, if you have multiple directories, you can provide the path to those directories in the JSON array format. For example, `[{"path": ".", "type": "pip", , "requirements_files": ["requirements.txt", "requirements-extras.txt", "tests/requirements.txt"]}, {"path": "subpath/to/the/other/directory", "type": "pip", "requirements_files": ["requirements.txt", "requirements-extras.txt", "tests/requirements.txt"]}]`. |
	| --- | --- |
15. Create a pull request by committing your changes to the repository of the component.
16. Review and merge the pull request.
Verification* From the Konflux **Applications** view, go to **Activity > Pipeline runs**.


	+ Go to the pipeline run with **Build** in the **Type** column and confirm that the `pre-fetch dependencies` stage displays a green checkmark. This indicates that the build process successfully fetched all dependencies.
* From the Konflux **Applications** view, go to **Activity > Latest commits**.
Enabling prefetch builds for `npm`
----------------------------------

Cachi2 supports `npm` by fetching any dependencies you declare in your `package.json` and `package-lock.json` project files. The npm CLI manages the `package-lock.json` file automatically, and Cachi2 fetches any dependencies and enables your build to install them without network access.

Prerequisites* You have an [upgraded build pipeline](https://redhat-appstudio.github.io/docs.appstudio.io/Documentation/main/how-to-guides/configuring-builds/proc_upgrade_build_pipeline/).
* You have an up-to-date [`package-lock.json`](https://docs.npmjs.com/cli/v9/configuring-npm/package-lock-json) file, newer than version 1, in your source repository. To make sure that you have the latest `package-lock.json` file, or to create a lockfile, run the [`npm-install`](https://docs.npmjs.com/cli/v9/commands/npm-install?v=true) command. You can also look at the `lockfileVersion` attribute in your `package-lock.json` file to make sure its value is a number greater than `**1**`.
ProcedureTo create a hermetic build for a component, complete the following steps:

1. Go to the `.tekton` directory and find the `.yaml` files related to the `**pull request**` and `**push**` processes.
2. Configure the hermetic pipeline by adding the following parameters in both `.yaml` files:


```
spec:    params:        -   ...        -   name: prefetch-input            value: '{"type": "npm", "path": "."}' **(1)**
```


| **1** | The `**prefetch-input**` parameter specifies the path to the directory that has the lockfile and the package metadata files. In this example, the `.` indicates that the package manager lockfile is in the repository root. Additionally, if you have multiple directories, you can provide the path to those directories in the JSON array format. For example, `[{"path": ".", "type": "npm"}, {"path": "subpath/to/the/other/directory", "type": "npm"}]`. |
| --- | --- |
3. Create a pull request by committing your changes to the repository of the component.
4. Review and merge the pull request.
Verification* From the Konflux **Applications** view, go to **Activity > Pipeline runs**.


	+ Go to the pipeline run with **Build** in the **Type** column and confirm that the `pre-fetch dependencies` stage displays a green checkmark. This indicates that the build process successfully fetched all dependencies.
* From the Konflux **Applications** view, go to **Activity > Latest commits**.
TroubleshootingIf your build fails, be sure to look at your logs:

In Konflux, from the **Applications** view, select the application build you want to troubleshoot, then from the resulting **Overview** page, select the **Activity** tab. From there, under **Activity By**, select **Pipeline runs**. From the **Name** column, select the build whose logs you want to check, then from the resulting **Pipeline run details** view, do one of the following:

* Select the **Logs** tab.
* Alternatively, you can click **build-container**. When the right panel opens, select the **Logs** tab to see a partial view of the log for that build.
Additional resources
--------------------

* To troubleshoot any issues you might experience when you enable prefetch builds for `pip` or `pip` with source dependencies, see [Troubleshooting](https://github.com/containerbuildsystem/cachi2/blob/main/docs/pip.md#troubleshooting).
* For more information about Cachi2, see [Cachi2](https://github.com/containerbuildsystem/cachi2/blob/main/README.md).
[Enabling hermetic builds](../proc_hermetic-builds/)[Defining component relationships](../configuring-builds/proc_defining_component_relationships/)