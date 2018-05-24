# Command Line Interface Reference

## Category "db"

CLI commands for DB management.

### rally db create

Create Rally database.

### rally db ensure

Creates Rally database if it doesn't exists.

### rally db recreate

Drop and create Rally database.

This will delete all existing data.

### rally db revision

Print current Rally database revision UUID.

### rally db show

Show the connection string.

**Command arguments**:

<a name=db-show-creds></a>

* *--creds* [[ref]](#db-show-creds)  
  Do not hide credentials from connection string

### rally db upgrade

Upgrade Rally database to the latest state.

## Category "env"

Set of commands that allow you to manage envs.

### rally env check

Check availability of all platforms in environment.

**Command arguments**:

<a name=env-check-env-uuid></a>

* *--env &lt;uuid&gt;* [[ref]](#env-check-env-uuid)  
  UUID or name of the env.  
  
    _Type_: str  
  
    _Defaults_: env

<a name=env-check-json></a>

* *--json* [[ref]](#env-check-json)  
  Format output as JSON.

<a name=env-check-detailed></a>

* *--detailed* [[ref]](#env-check-detailed)  
  Show detailed information.

### rally env create

Create new environment.

**Command arguments**:

<a name=env-create-name-name-n-name></a>

* *--name &lt;name&gt;, -n &lt;name&gt;* [[ref]](#env-create-name-name-n-name)  
  Name of the env.  
  
    _Type_: str

<a name=env-create-description-description-d-description></a>

* *--description &lt;description&gt;, -d &lt;description&gt;* [[ref]](#env-create-description-description-d-description)  
  Env description  
  
    _Type_: str  
  
    _Defaults_: description

<a name=env-create-extras-extras-e-extras></a>

* *--extras &lt;extras&gt;, -e &lt;extras&gt;* [[ref]](#env-create-extras-extras-e-extras)  
  JSON or YAML dict with custom non validate info.  
  
    _Type_: str  
  
    _Defaults_: extras

<a name=env-create-fromsysenv></a>

* *--from-sysenv* [[ref]](#env-create-fromsysenv)  
  Iterate over all available platforms and check system environment for credentials.

<a name=env-create-spec-path-s-path></a>

* *--spec &lt;path&gt;, -s &lt;path&gt;* [[ref]](#env-create-spec-path-s-path)  
  Path to env spec.  
  
    _Type_: str  
  
    _Defaults_: spec

<a name=env-create-json></a>

* *--json* [[ref]](#env-create-json)  
  Format output as JSON.

<a name=env-create-nouse></a>

* *--no-use* [[ref]](#env-create-nouse)  
  Don't set new env as default for future operations.

### rally env delete

Deletes all records related to Env from db.

**Command arguments**:

<a name=env-delete-env-uuid></a>

* *--env &lt;uuid&gt;* [[ref]](#env-delete-env-uuid)  
  UUID or name of the env.  
  
    _Type_: str  
  
    _Defaults_: env

<a name=env-delete-force></a>

* *--force* [[ref]](#env-delete-force)  
  Delete DB records even if env is not destroyed.

### rally env destroy

Destroy existing environment.

**Command arguments**:

<a name=env-destroy-env-uuid></a>

* *--env &lt;uuid&gt;* [[ref]](#env-destroy-env-uuid)  
  UUID or name of the env.  
  
    _Type_: str  
  
    _Defaults_: env

<a name=env-destroy-skipcleanup></a>

* *--skip-cleanup* [[ref]](#env-destroy-skipcleanup)  
  Do not perform platforms cleanup before destroy.

<a name=env-destroy-json></a>

* *--json* [[ref]](#env-destroy-json)  
  Format output as JSON.

<a name=env-destroy-detailed></a>

* *--detailed* [[ref]](#env-destroy-detailed)  
  Show detailed information.

### rally env info

Show environment information.

**Command arguments**:

<a name=env-info-env-uuid></a>

* *--env &lt;uuid&gt;* [[ref]](#env-info-env-uuid)  
  UUID or name of the env.  
  
    _Type_: str  
  
    _Defaults_: env

<a name=env-info-json></a>

* *--json* [[ref]](#env-info-json)  
  Format output as JSON.

### rally env list

List existing environments.

**Command arguments**:

<a name=env-list-json></a>

* *--json* [[ref]](#env-list-json)  
  Format output as JSON.

### rally env show



**Command arguments**:

<a name=env-show-env-uuid></a>

* *--env &lt;uuid&gt;* [[ref]](#env-show-env-uuid)  
  UUID or name of the env.  
  
    _Type_: str  
  
    _Defaults_: env

<a name=env-show-json></a>

* *--json* [[ref]](#env-show-json)  
  Format output as JSON.

<a name=env-show-onlyspec></a>

* *--only-spec* [[ref]](#env-show-onlyspec)  
  Print only a spec for the environment.

### rally env use

Set default environment.

**Command arguments**:

<a name=env-use-env-uuid></a>

* *--env &lt;uuid&gt;* [[ref]](#env-use-env-uuid)  
  UUID or name of a env.  
  
    _Type_: str

<a name=env-use-json></a>

* *--json* [[ref]](#env-use-json)  
  Format output as JSON.

## Category "plugin"

Set of commands that allow you to manage Rally plugins.

### rally plugin list

List all Rally plugins that match name and platform.

**Command arguments**:

<a name=plugin-list-name-name></a>

* *--name &lt;name&gt;* [[ref]](#plugin-list-name-name)  
  List only plugins that match the given name.  
  
    _Type_: str  
  
    _Defaults_: name

<a name=plugin-list-platform-platform></a>

* *--platform &lt;platform&gt;* [[ref]](#plugin-list-platform-platform)  
  List only plugins that are in the specified platform.  
  
    _Type_: str  
  
    _Defaults_: platform

<a name=plugin-list-namespace></a>

* *--namespace* [[ref]](#plugin-list-namespace)  
  [Deprecated since Rally 0.10.0] Use '--platform' instead.   
  
    _Defaults_: platform

<a name=plugin-list-pluginbase-plugin-base></a>

* *--plugin-base &lt;plugin_base&gt;* [[ref]](#plugin-list-pluginbase-plugin-base)  
  Plugin base class.  
  
    _Type_: str  
  
    _Defaults_: base_cls

### rally plugin show

Show detailed information about a Rally plugin.

**Command arguments**:

<a name=plugin-show-name-name></a>

* *--name &lt;name&gt;* [[ref]](#plugin-show-name-name)  
  Plugin name.  
  
    _Type_: str

<a name=plugin-show-platform-platform></a>

* *--platform &lt;platform&gt;* [[ref]](#plugin-show-platform-platform)  
  Plugin platform.  
  
    _Type_: str  
  
    _Defaults_: platform

<a name=plugin-show-namespace></a>

* *--namespace* [[ref]](#plugin-show-namespace)  
  [Deprecated since Rally 0.10.0] Use '--platform' instead.   
  
    _Defaults_: platform

## Category "task"

Set of commands that allow you to manage tasks and results.

    

### rally task abort

Abort a running task.

**Command arguments**:

<a name=task-abort-uuid-uuid></a>

* *--uuid &lt;uuid&gt;* [[ref]](#task-abort-uuid-uuid)  
  UUID of task.  
  
    _Type_: str

<a name=task-abort-soft></a>

* *--soft* [[ref]](#task-abort-soft)  
  Abort task after current scenario finishes execution.

### rally task delete

Delete task and its results.

**Command arguments**:

<a name=task-delete-force></a>

* *--force* [[ref]](#task-delete-force)  
  force delete

<a name=task-delete-uuid-taskid></a>

* *--uuid &lt;task-id&gt;* [[ref]](#task-delete-uuid-taskid)  
  UUID of task or a list of task UUIDs.  
  
    _Type_: str

### rally task detailed



**Command arguments**:

<a name=task-detailed-uuid-uuid></a>

* *--uuid &lt;uuid&gt;* [[ref]](#task-detailed-uuid-uuid)  
  UUID of task. If --uuid is "last" the results of  the most recently created task will be displayed.  
  
    _Type_: str

<a name=task-detailed-iterationsdata></a>

* *--iterations-data* [[ref]](#task-detailed-iterationsdata)  
  Print detailed results for each iteration.

### rally task export

Export task results to the custom task's exporting system.

**Command arguments**:

<a name=task-export-uuid-uuid></a>

* *--uuid &lt;uuid&gt;* [[ref]](#task-export-uuid-uuid)  
  UUIDs of tasks or json reports of tasks  
  
    _Type_: str  
  
    _Defaults_: tasks

<a name=task-export-type-type></a>

* *--type &lt;type&gt;* [[ref]](#task-export-type-type)  
  Report type. Out-of-the-box types: JSON, HTML, HTML-Static, Elastic, JUnit-XML. HINT: You can list all types, executing `rally plugin list --plugin-base TaskExporter` command.  
  
    _Type_: str  
  
    _Defaults_: output_type

<a name=task-export-to-dest></a>

* *--to &lt;dest&gt;* [[ref]](#task-export-to-dest)  
  Report destination. Can be a path to a file (in case of JSON, HTML, HTML-Static, JUnit-XML, Elastic etc. types) to save the report to or a connection string. It depends on the report type.  
  
    _Type_: str  
  
    _Defaults_: output_dest

### rally task import

Import json results of a test into rally database

**Command arguments**:

<a name=task-import-file-path></a>

* *--file &lt;path&gt;* [[ref]](#task-import-file-path)  
  JSON file with task results  
  
    _Type_: str  
  
    _Defaults_: task_file

<a name=task-import-deployment-uuid></a>

* *--deployment &lt;uuid&gt;* [[ref]](#task-import-deployment-uuid)  
  UUID or name of a deployment.  
  
    _Type_: str

<a name=task-import-tag-tag></a>

* *--tag &lt;tag&gt;* [[ref]](#task-import-tag-tag)  
  Mark the task with a tag or a few tags.  
  
    _Type_: str  
  
    _Defaults_: tags

### rally task list

List tasks, started and finished.

Displayed tasks can be filtered by status or deployment.  By
default 'rally task list' will display tasks from the active
deployment without filtering by status.

**Command arguments**:

<a name=task-list-deployment-uuid></a>

* *--deployment &lt;uuid&gt;* [[ref]](#task-list-deployment-uuid)  
  UUID or name of a deployment.  
  
    _Type_: str

<a name=task-list-alldeployments></a>

* *--all-deployments* [[ref]](#task-list-alldeployments)  
  List tasks from all deployments.

<a name=task-list-status-status></a>

* *--status &lt;status&gt;* [[ref]](#task-list-status-status)  
  List tasks with specified status. Available statuses: aborted, aborting, crashed, finished, init, paused, running, sla_failed, soft_aborting, validated, validating, validation_failed  
  
    _Type_: str  
  
    _Defaults_: status

<a name=task-list-tag-tag></a>

* *--tag &lt;tag&gt;* [[ref]](#task-list-tag-tag)  
  Tags to filter tasks by.  
  
    _Type_: str  
  
    _Defaults_: tags

<a name=task-list-uuidsonly></a>

* *--uuids-only* [[ref]](#task-list-uuidsonly)  
  List task UUIDs only.

### rally task report

Generate a report for the specified task(s).

**Command arguments**:

<a name=task-report-tasks></a>

* *--tasks* [[ref]](#task-report-tasks)  
  [Deprecated since Rally 0.10.0] Use '--uuid' instead.   
  
    _Defaults_: tasks

<a name=task-report-out-path></a>

* *--out &lt;path&gt;* [[ref]](#task-report-out-path)  
  Report destination. Can be a path to a file (in case of HTML, HTML-STATIC, etc. types) to save the report to or a connection string.  
  
    _Type_: str  
  
    _Defaults_: out

<a name=task-report-open></a>

* *--open* [[ref]](#task-report-open)  
  Open the output in a browser.

<a name=task-report-html></a>

* *--html* [[ref]](#task-report-html)  
  

<a name=task-report-htmlstatic></a>

* *--html-static* [[ref]](#task-report-htmlstatic)  
  

<a name=task-report-json></a>

* *--json* [[ref]](#task-report-json)  
  

<a name=task-report-junit></a>

* *--junit* [[ref]](#task-report-junit)  
  [Deprecated since Rally 0.10.0] Use 'rally task export --type junit-xml' instead. 

<a name=task-report-uuid-uuid></a>

* *--uuid &lt;uuid&gt;* [[ref]](#task-report-uuid-uuid)  
  UUIDs of tasks or json reports of tasks  
  
    _Type_: str  
  
    _Defaults_: tasks

### rally task results

Display raw task results.

This will produce a lot of output data about every iteration.

**Command arguments**:

<a name=task-results-uuid-uuid></a>

* *--uuid &lt;uuid&gt;* [[ref]](#task-results-uuid-uuid)  
  UUID of task.  
  
    _Type_: str

### rally task sla-check

Display SLA check results table.

**Command arguments**:

<a name=task-slacheck-uuid-uuid></a>

* *--uuid &lt;uuid&gt;* [[ref]](#task-slacheck-uuid-uuid)  
  UUID of task.  
  
    _Type_: str

<a name=task-slacheck-json></a>

* *--json* [[ref]](#task-slacheck-json)  
  Output in JSON format.

### rally task sla_check

DEPRECATED since Rally 0.8.0, use `rally task sla-check` instead.

**Command arguments**:

<a name=task-sla-check-uuid-uuid></a>

* *--uuid &lt;uuid&gt;* [[ref]](#task-sla-check-uuid-uuid)  
  UUID of task.  
  
    _Type_: str

<a name=task-sla-check-json></a>

* *--json* [[ref]](#task-sla-check-json)  
  Output in JSON format.

### rally task start

Run task.

If both task_args and task_args_file are specified, they are going to
be merged. task_args has a higher priority so it overrides
values from task_args_file.
There are 3 kinds of return codes, 0: no error, 1: running error,
2: sla check failed.

**Command arguments**:

<a name=task-start-deployment-uuid></a>

* *--deployment &lt;uuid&gt;* [[ref]](#task-start-deployment-uuid)  
  UUID or name of a deployment.  
  
    _Type_: str

<a name=task-start-task-path-filename-path></a>

* *--task &lt;path&gt;, --filename &lt;path&gt;* [[ref]](#task-start-task-path-filename-path)  
  Path to the input task file.

<a name=task-start-taskargs-json></a>

* *--task-args &lt;json&gt;* [[ref]](#task-start-taskargs-json)  
  Input task args (JSON dict). These args are used to render the Jinja2 template in the input task.  
  
    _Defaults_: task_args

<a name=task-start-taskargsfile-path></a>

* *--task-args-file &lt;path&gt;* [[ref]](#task-start-taskargsfile-path)  
  Path to the file with input task args (dict in JSON/YAML). These args are used to render the Jinja2 template in the input task.  
  
    _Defaults_: task_args_file

<a name=task-start-tag-tag></a>

* *--tag &lt;tag&gt;* [[ref]](#task-start-tag-tag)  
  Mark the task with a tag or a few tags.  
  
    _Type_: str  
  
    _Defaults_: tags

<a name=task-start-nouse></a>

* *--no-use* [[ref]](#task-start-nouse)  
  Don't set new task as default for future operations.

<a name=task-start-abortonslafailure></a>

* *--abort-on-sla-failure* [[ref]](#task-start-abortonslafailure)  
  Abort the execution of a task when any SLA check for it fails for subtask or workload.

### rally task status

Display the current status of a task.

**Command arguments**:

<a name=task-status-uuid-uuid></a>

* *--uuid &lt;uuid&gt;* [[ref]](#task-status-uuid-uuid)  
  UUID of task  
  
    _Type_: str

### rally task trends

Generate workloads trends HTML report.

**Command arguments**:

<a name=task-trends-out-path></a>

* *--out &lt;path&gt;* [[ref]](#task-trends-out-path)  
  Path to output file.  
  
    _Type_: str

<a name=task-trends-open></a>

* *--open* [[ref]](#task-trends-open)  
  Open the output in a browser.

<a name=task-trends-tasks-tasks></a>

* *--tasks &lt;tasks&gt;* [[ref]](#task-trends-tasks-tasks)  
  UUIDs of tasks, or JSON files with task results

### rally task use

Set active task.

**Command arguments**:

<a name=task-use-uuid-uuid></a>

* *--uuid &lt;uuid&gt;* [[ref]](#task-use-uuid-uuid)  
  UUID of the task  
  
    _Type_: str

<a name=task-use-task></a>

* *--task* [[ref]](#task-use-task)  
  [Deprecated since Rally 0.2.0] Use '--uuid' instead.   
  
    _Type_: str

### rally task validate

Validate a task configuration file.

This will check that task configuration file has valid syntax and
all required options of scenarios, contexts, SLA and runners are set.

If both task_args and task_args_file are specified, they will
be merged. task_args has a higher priority so it will override
values from task_args_file.

**Command arguments**:

<a name=task-validate-deployment-uuid></a>

* *--deployment &lt;uuid&gt;* [[ref]](#task-validate-deployment-uuid)  
  UUID or name of a deployment.  
  
    _Type_: str

<a name=task-validate-task-path-filename-path></a>

* *--task &lt;path&gt;, --filename &lt;path&gt;* [[ref]](#task-validate-task-path-filename-path)  
  Path to the input task file.

<a name=task-validate-taskargs-json></a>

* *--task-args &lt;json&gt;* [[ref]](#task-validate-taskargs-json)  
  Input task args (JSON dict). These args are used to render the Jinja2 template in the input task.  
  
    _Defaults_: task_args

<a name=task-validate-taskargsfile-path></a>

* *--task-args-file &lt;path&gt;* [[ref]](#task-validate-taskargsfile-path)  
  Path to the file with input task args (dict in JSON/YAML). These args are used to render the Jinja2 template in the input task.  
  
    _Defaults_: task_args_file

## Category "verify"

Verify an OpenStack cloud via a verifier.

### rally verify add-verifier-ext

Add a verifier extension.

**Command arguments**:

<a name=verify-addverifierext-id-id></a>

* *--id &lt;id&gt;* [[ref]](#verify-addverifierext-id-id)  
  Verifier name or UUID. HINT: You can list all verifiers, executing command `rally verify list-verifiers`.  
  
    _Type_: str  
  
    _Defaults_: verifier_id

<a name=verify-addverifierext-source-source></a>

* *--source &lt;source&gt;* [[ref]](#verify-addverifierext-source-source)  
  Path or URL to the repo to clone verifier extension from.  
  
    _Type_: str  
  
    _Defaults_: source

<a name=verify-addverifierext-version-version></a>

* *--version &lt;version&gt;* [[ref]](#verify-addverifierext-version-version)  
  Branch, tag or commit ID to checkout before installation of the verifier extension (the 'master' branch is used by default).  
  
    _Type_: str  
  
    _Defaults_: version

<a name=verify-addverifierext-extrasettings-extra-settings></a>

* *--extra-settings &lt;extra_settings&gt;* [[ref]](#verify-addverifierext-extrasettings-extra-settings)  
  Extra installation settings for verifier extension.  
  
    _Type_: str  
  
    _Defaults_: extra

### rally verify configure-verifier

Configure a verifier for a specific deployment.

**Command arguments**:

<a name=verify-configureverifier-id-id></a>

* *--id &lt;id&gt;* [[ref]](#verify-configureverifier-id-id)  
  Verifier name or UUID. HINT: You can list all verifiers, executing command `rally verify list-verifiers`.  
  
    _Type_: str  
  
    _Defaults_: verifier_id

<a name=verify-configureverifier-deploymentid-id></a>

* *--deployment-id &lt;id&gt;* [[ref]](#verify-configureverifier-deploymentid-id)  
  Deployment name or UUID. HINT: You can list all deployments, executing command `rally deployment list`.  
  
    _Type_: str

<a name=verify-configureverifier-reconfigure></a>

* *--reconfigure* [[ref]](#verify-configureverifier-reconfigure)  
  Reconfigure verifier.

<a name=verify-configureverifier-extend-path/json/yaml></a>

* *--extend &lt;path/json/yaml&gt;* [[ref]](#verify-configureverifier-extend-path/json/yaml)  
  Extend verifier configuration with extra options. If options are already present, the given ones will override them. Can be a path to a regular config file or just a json/yaml.  
  
    _Type_: str  
  
    _Defaults_: extra_options

<a name=verify-configureverifier-override-path></a>

* *--override &lt;path&gt;* [[ref]](#verify-configureverifier-override-path)  
  Override verifier configuration by another one from a given source.  
  
    _Type_: str  
  
    _Defaults_: new_configuration

<a name=verify-configureverifier-show></a>

* *--show* [[ref]](#verify-configureverifier-show)  
  Show verifier configuration.

### rally verify create-verifier

Create a verifier.

**Command arguments**:

<a name=verify-createverifier-name-name></a>

* *--name &lt;name&gt;* [[ref]](#verify-createverifier-name-name)  
  Verifier name (for example, 'My verifier').  
  
    _Type_: str

<a name=verify-createverifier-type-type></a>

* *--type &lt;type&gt;* [[ref]](#verify-createverifier-type-type)  
  Verifier plugin name. HINT: You can list all verifier plugins, executing command `rally verify list-plugins`.  
  
    _Type_: str

<a name=verify-createverifier-platform-platform></a>

* *--platform &lt;platform&gt;* [[ref]](#verify-createverifier-platform-platform)  
  Verifier plugin platform. Should be specified in case of two verifier plugins with equal names but in different platforms.  
  
    _Type_: str  
  
    _Defaults_: platform

<a name=verify-createverifier-namespace></a>

* *--namespace* [[ref]](#verify-createverifier-namespace)  
  [Deprecated since Rally 0.10.0] Use '--platform' instead.   
  
    _Defaults_: platform

<a name=verify-createverifier-source-source></a>

* *--source &lt;source&gt;* [[ref]](#verify-createverifier-source-source)  
  Path or URL to the repo to clone verifier from.  
  
    _Type_: str  
  
    _Defaults_: source

<a name=verify-createverifier-version-version></a>

* *--version &lt;version&gt;* [[ref]](#verify-createverifier-version-version)  
  Branch, tag or commit ID to checkout before verifier installation (the 'master' branch is used by default).  
  
    _Type_: str  
  
    _Defaults_: version

<a name=verify-createverifier-systemwide></a>

* *--system-wide* [[ref]](#verify-createverifier-systemwide)  
  Use the system-wide environment for verifier instead of a virtual environment.

<a name=verify-createverifier-extrasettings-extra-settings></a>

* *--extra-settings &lt;extra_settings&gt;* [[ref]](#verify-createverifier-extrasettings-extra-settings)  
  Extra installation settings for verifier.  
  
    _Type_: str  
  
    _Defaults_: extra

<a name=verify-createverifier-nouse></a>

* *--no-use* [[ref]](#verify-createverifier-nouse)  
  Not to set the created verifier as the default verifier for future operations.

### rally verify delete

Delete a verification or a few verifications.

**Command arguments**:

<a name=verify-delete-uuid-uuid></a>

* *--uuid &lt;uuid&gt;* [[ref]](#verify-delete-uuid-uuid)  
  UUIDs of verifications. HINT: You can list all verifications, executing command `rally verify list`.  
  
    _Type_: str

### rally verify delete-verifier

Delete a verifier.

**Command arguments**:

<a name=verify-deleteverifier-id-id></a>

* *--id &lt;id&gt;* [[ref]](#verify-deleteverifier-id-id)  
  Verifier name or UUID. HINT: You can list all verifiers, executing command `rally verify list-verifiers`.  
  
    _Type_: str

<a name=verify-deleteverifier-deploymentid-id></a>

* *--deployment-id &lt;id&gt;* [[ref]](#verify-deleteverifier-deploymentid-id)  
  Deployment name or UUID. If specified, only the deployment-specific data will be deleted for verifier. HINT: You can list all deployments, executing command `rally deployment list`.  
  
    _Type_: str

<a name=verify-deleteverifier-force></a>

* *--force* [[ref]](#verify-deleteverifier-force)  
  Delete all stored verifications of the specified verifier. If a deployment specified, only verifications of this deployment will be deleted. Use this argument carefully! You can delete verifications that may be important to you.

### rally verify delete-verifier-ext

Delete a verifier extension.

**Command arguments**:

<a name=verify-deleteverifierext-id-id></a>

* *--id &lt;id&gt;* [[ref]](#verify-deleteverifierext-id-id)  
  Verifier name or UUID. HINT: You can list all verifiers, executing command `rally verify list-verifiers`.  
  
    _Type_: str  
  
    _Defaults_: verifier_id

<a name=verify-deleteverifierext-name-name></a>

* *--name &lt;name&gt;* [[ref]](#verify-deleteverifierext-name-name)  
  Verifier extension name.  
  
    _Type_: str  
  
    _Defaults_: name

### rally verify import

Import results of a test run into the Rally database.

**Command arguments**:

<a name=verify-import-id-id></a>

* *--id &lt;id&gt;* [[ref]](#verify-import-id-id)  
  Verifier name or UUID. HINT: You can list all verifiers, executing command `rally verify list-verifiers`.  
  
    _Type_: str  
  
    _Defaults_: verifier_id

<a name=verify-import-deploymentid-id></a>

* *--deployment-id &lt;id&gt;* [[ref]](#verify-import-deploymentid-id)  
  Deployment name or UUID. HINT: You can list all deployments, executing command `rally deployment list`.  
  
    _Type_: str

<a name=verify-import-file-path></a>

* *--file &lt;path&gt;* [[ref]](#verify-import-file-path)  
  File to import test results from.  
  
    _Type_: str  
  
    _Defaults_: file_to_parse

<a name=verify-import-runargs-run-args></a>

* *--run-args &lt;run_args&gt;* [[ref]](#verify-import-runargs-run-args)  
  Arguments that might be used when running tests. For example, '{concurrency: 2, pattern: set=identity}'.  
  
    _Type_: str  
  
    _Defaults_: run_args

<a name=verify-import-nouse></a>

* *--no-use* [[ref]](#verify-import-nouse)  
  Not to set the created verification as the default verification for future operations.

### rally verify list

List all verifications.

**Command arguments**:

<a name=verify-list-id-id></a>

* *--id &lt;id&gt;* [[ref]](#verify-list-id-id)  
  Verifier name or UUID. HINT: You can list all verifiers, executing command `rally verify list-verifiers`.  
  
    _Type_: str  
  
    _Defaults_: verifier_id

<a name=verify-list-deploymentid-id></a>

* *--deployment-id &lt;id&gt;* [[ref]](#verify-list-deploymentid-id)  
  Deployment name or UUID. HINT: You can list all deployments, executing command `rally deployment list`.  
  
    _Type_: str

<a name=verify-list-tag-tag></a>

* *--tag &lt;tag&gt;* [[ref]](#verify-list-tag-tag)  
  Tags to filter verifications by.  
  
    _Type_: str  
  
    _Defaults_: tags

<a name=verify-list-status-status></a>

* *--status &lt;status&gt;* [[ref]](#verify-list-status-status)  
  Status to filter verifications by.  
  
    _Type_: str  
  
    _Defaults_: status

### rally verify list-plugins

List all plugins for verifiers management.

**Command arguments**:

<a name=verify-listplugins-platform-platform></a>

* *--platform &lt;platform&gt;* [[ref]](#verify-listplugins-platform-platform)  
  Requried patform (e.g. openstack).  
  
    _Type_: str  
  
    _Defaults_: platform

<a name=verify-listplugins-namespace></a>

* *--namespace* [[ref]](#verify-listplugins-namespace)  
  [Deprecated since Rally 0.10.0] Use '--platform' instead.   
  
    _Defaults_: platform

### rally verify list-verifier-exts

List all verifier extensions.

**Command arguments**:

<a name=verify-listverifierexts-id-id></a>

* *--id &lt;id&gt;* [[ref]](#verify-listverifierexts-id-id)  
  Verifier name or UUID. HINT: You can list all verifiers, executing command `rally verify list-verifiers`.  
  
    _Type_: str  
  
    _Defaults_: verifier_id

### rally verify list-verifier-tests

List all verifier tests.

**Command arguments**:

<a name=verify-listverifiertests-id-id></a>

* *--id &lt;id&gt;* [[ref]](#verify-listverifiertests-id-id)  
  Verifier name or UUID. HINT: You can list all verifiers, executing command `rally verify list-verifiers`.  
  
    _Type_: str  
  
    _Defaults_: verifier_id

<a name=verify-listverifiertests-pattern-pattern></a>

* *--pattern &lt;pattern&gt;* [[ref]](#verify-listverifiertests-pattern-pattern)  
  Pattern which will be used for matching. Can be a regexp or a verifier-specific entity (for example, in case of Tempest you can specify 'set=smoke').  
  
    _Type_: str  
  
    _Defaults_: pattern

### rally verify list-verifiers

List all verifiers.

**Command arguments**:

<a name=verify-listverifiers-status-status></a>

* *--status &lt;status&gt;* [[ref]](#verify-listverifiers-status-status)  
  Status to filter verifiers by.  
  
    _Type_: str  
  
    _Defaults_: status

### rally verify report

Generate a report for a verification or a few verifications.

**Command arguments**:

<a name=verify-report-uuid-uuid></a>

* *--uuid &lt;uuid&gt;* [[ref]](#verify-report-uuid-uuid)  
  UUIDs of verifications. HINT: You can list all verifications, executing command `rally verify list`.  
  
    _Type_: str  
  
    _Defaults_: verification_uuid

<a name=verify-report-type-type></a>

* *--type &lt;type&gt;* [[ref]](#verify-report-type-type)  
  Report type (Defaults to JSON). Out-of-the-box types: HTML, HTML-Static, JSON, JUnit-XML. HINT: You can list all types, executing `rally plugin list --plugin-base VerificationReporter` command.  
  
    _Type_: str  
  
    _Defaults_: output_type

<a name=verify-report-to-dest></a>

* *--to &lt;dest&gt;* [[ref]](#verify-report-to-dest)  
  Report destination. Can be a path to a file (in case of HTML, JSON, etc. types) to save the report to or a connection string. It depends on the report type.  
  
    _Type_: str  
  
    _Defaults_: output_dest

<a name=verify-report-open></a>

* *--open* [[ref]](#verify-report-open)  
  Open the output file in a browser.

### rally verify rerun

Rerun tests from a verification for a specific deployment.

**Command arguments**:

<a name=verify-rerun-uuid-uuid></a>

* *--uuid &lt;uuid&gt;* [[ref]](#verify-rerun-uuid-uuid)  
  Verification UUID. HINT: You can list all verifications, executing command `rally verify list`.  
  
    _Type_: str  
  
    _Defaults_: verification_uuid

<a name=verify-rerun-deploymentid-id></a>

* *--deployment-id &lt;id&gt;* [[ref]](#verify-rerun-deploymentid-id)  
  Deployment name or UUID. HINT: You can list all deployments, executing command `rally deployment list`.  
  
    _Type_: str

<a name=verify-rerun-failed></a>

* *--failed* [[ref]](#verify-rerun-failed)  
  Rerun only failed tests.

<a name=verify-rerun-tag-tag></a>

* *--tag &lt;tag&gt;* [[ref]](#verify-rerun-tag-tag)  
  Mark verification with a tag or a few tags.  
  
    _Type_: str  
  
    _Defaults_: tags

<a name=verify-rerun-concurrency-N></a>

* *--concurrency &lt;N&gt;* [[ref]](#verify-rerun-concurrency-N)  
  How many processes to be used for running verifier tests. The default value (0) auto-detects your CPU count.  
  
    _Type_: int  
  
    _Defaults_: concur

<a name=verify-rerun-detailed></a>

* *--detailed* [[ref]](#verify-rerun-detailed)  
  Show verification details such as errors of failed tests.

<a name=verify-rerun-nouse></a>

* *--no-use* [[ref]](#verify-rerun-nouse)  
  Not to set the finished verification as the default verification for future operations.

### rally verify show

Show detailed information about a verification.

**Command arguments**:

<a name=verify-show-uuid-uuid></a>

* *--uuid &lt;uuid&gt;* [[ref]](#verify-show-uuid-uuid)  
  Verification UUID. HINT: You can list all verifications, executing command `rally verify list`.  
  
    _Type_: str  
  
    _Defaults_: verification_uuid

<a name=verify-show-sortby-query></a>

* *--sort-by &lt;query&gt;* [[ref]](#verify-show-sortby-query)  
  Sort tests by 'name', 'duration' or 'status'.  
  
    _Type_: str  
  
    _Defaults_: sort_by

<a name=verify-show-detailed></a>

* *--detailed* [[ref]](#verify-show-detailed)  
  Show verification details such as run arguments and errors of failed tests.

### rally verify show-verifier

Show detailed information about a verifier.

**Command arguments**:

<a name=verify-showverifier-id-id></a>

* *--id &lt;id&gt;* [[ref]](#verify-showverifier-id-id)  
  Verifier name or UUID. HINT: You can list all verifiers, executing command `rally verify list-verifiers`.  
  
    _Type_: str  
  
    _Defaults_: verifier_id

### rally verify start

Start a verification (run verifier tests).

**Command arguments**:

<a name=verify-start-id-id></a>

* *--id &lt;id&gt;* [[ref]](#verify-start-id-id)  
  Verifier name or UUID. HINT: You can list all verifiers, executing command `rally verify list-verifiers`.  
  
    _Type_: str  
  
    _Defaults_: verifier_id

<a name=verify-start-deploymentid-id></a>

* *--deployment-id &lt;id&gt;* [[ref]](#verify-start-deploymentid-id)  
  Deployment name or UUID. HINT: You can list all deployments, executing command `rally deployment list`.  
  
    _Type_: str

<a name=verify-start-tag-tag></a>

* *--tag &lt;tag&gt;* [[ref]](#verify-start-tag-tag)  
  Mark verification with a tag or a few tags.  
  
    _Type_: str  
  
    _Defaults_: tags

<a name=verify-start-pattern-pattern></a>

* *--pattern &lt;pattern&gt;* [[ref]](#verify-start-pattern-pattern)  
  Pattern which will be used for running tests. Can be a regexp or a verifier-specific entity (for example, in case of Tempest you can specify 'set=smoke').  
  
    _Type_: str  
  
    _Defaults_: pattern

<a name=verify-start-concurrency-N></a>

* *--concurrency &lt;N&gt;* [[ref]](#verify-start-concurrency-N)  
  How many processes to be used for running verifier tests. The default value (0) auto-detects your CPU count.  
  
    _Type_: int  
  
    _Defaults_: concur

<a name=verify-start-loadlist-path></a>

* *--load-list &lt;path&gt;* [[ref]](#verify-start-loadlist-path)  
  Path to a file with a list of tests to run.  
  
    _Type_: str  
  
    _Defaults_: load_list

<a name=verify-start-skiplist-path></a>

* *--skip-list &lt;path&gt;* [[ref]](#verify-start-skiplist-path)  
  Path to a file with a list of tests to skip. Format: json or yaml like a dictionary where keys are test names and values are reasons.  
  
    _Type_: str  
  
    _Defaults_: skip_list

<a name=verify-start-xfaillist-path></a>

* *--xfail-list &lt;path&gt;* [[ref]](#verify-start-xfaillist-path)  
  Path to a file with a list of tests that will be considered as expected failures. Format: json or yaml like a dictionary where keys are test names and values are reasons.  
  
    _Type_: str  
  
    _Defaults_: xfail_list

<a name=verify-start-detailed></a>

* *--detailed* [[ref]](#verify-start-detailed)  
  Show verification details such as errors of failed tests.

<a name=verify-start-nouse></a>

* *--no-use* [[ref]](#verify-start-nouse)  
  Not to set the finished verification as the default verification for future operations.

### rally verify update-verifier

Update a verifier.

**Command arguments**:

<a name=verify-updateverifier-id-id></a>

* *--id &lt;id&gt;* [[ref]](#verify-updateverifier-id-id)  
  Verifier name or UUID. HINT: You can list all verifiers, executing command `rally verify list-verifiers`.  
  
    _Type_: str  
  
    _Defaults_: verifier_id

<a name=verify-updateverifier-updatevenv></a>

* *--update-venv* [[ref]](#verify-updateverifier-updatevenv)  
  Update the virtual environment for verifier.

<a name=verify-updateverifier-version-version></a>

* *--version &lt;version&gt;* [[ref]](#verify-updateverifier-version-version)  
  Branch, tag or commit ID to checkout. HINT: Specify the same version to pull the latest repo code.  
  
    _Type_: str  
  
    _Defaults_: version

<a name=verify-updateverifier-systemwide></a>

* *--system-wide* [[ref]](#verify-updateverifier-systemwide)  
  Switch to using the system-wide environment.

<a name=verify-updateverifier-nosystemwide></a>

* *--no-system-wide* [[ref]](#verify-updateverifier-nosystemwide)  
  Switch to using the virtual environment. If the virtual environment doesn't exist, it will be created.

### rally verify use

Choose a verification to use for the future operations.

**Command arguments**:

<a name=verify-use-uuid-uuid></a>

* *--uuid &lt;uuid&gt;* [[ref]](#verify-use-uuid-uuid)  
  Verification UUID. HINT: You can list all verifications, executing command `rally verify list`.  
  
    _Type_: str

### rally verify use-verifier

Choose a verifier to use for the future operations.

**Command arguments**:

<a name=verify-useverifier-id-id></a>

* *--id &lt;id&gt;* [[ref]](#verify-useverifier-id-id)  
  Verifier name or UUID. HINT: You can list all verifiers, executing command `rally verify list-verifiers`.  
  
    _Type_: str