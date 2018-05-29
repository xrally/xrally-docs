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

<table>
  <thead>
    <tr>
      <th>Argument</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap">
        <a name="db-show-creds"></a>--creds<a href="#db-show-creds"> [ref]</a>
      </td>
      <td>
        <span>Do not hide credentials from connection string</span>
        <br>
      </td>
    </tr>
  </tbody>
</table>


### rally db upgrade

Upgrade Rally database to the latest state.

## Category "env"

Set of commands that allow you to manage envs.

### rally env check

Check availability of all platforms in environment.

<table>
  <thead>
    <tr>
      <th>Argument</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap">
        <a name="env-check-env-uuid"></a>--env &lt;uuid&gt;<a href="#env-check-env-uuid"> [ref]</a>
      </td>
      <td>
        <span>UUID or name of the env.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: env</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="env-check-json"></a>--json<a href="#env-check-json"> [ref]</a>
      </td>
      <td>
        <span>Format output as JSON.</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="env-check-detailed"></a>--detailed<a href="#env-check-detailed"> [ref]</a>
      </td>
      <td>
        <span>Show detailed information.</span>
        <br>
      </td>
    </tr>
  </tbody>
</table>


### rally env create

Create new environment.

<table>
  <thead>
    <tr>
      <th>Argument</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap">
        <a name="env-create-name-name
n-name"></a>--name &lt;name&gt;,<br />-n &lt;name&gt;<a href="#env-create-name-name
n-name"> [ref]</a>
      </td>
      <td>
        <span>Name of the env.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="env-create-description-description
d-description"></a>--description &lt;description&gt;,<br />-d &lt;description&gt;<a href="#env-create-description-description
d-description"> [ref]</a>
      </td>
      <td>
        <span>Env description</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: description</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="env-create-extras-extras
e-extras"></a>--extras &lt;extras&gt;,<br />-e &lt;extras&gt;<a href="#env-create-extras-extras
e-extras"> [ref]</a>
      </td>
      <td>
        <span>JSON or YAML dict with custom non validate info.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: extras</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="env-create-fromsysenv"></a>--from-sysenv<a href="#env-create-fromsysenv"> [ref]</a>
      </td>
      <td>
        <span>Iterate over all available platforms and check system environment for credentials.</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="env-create-spec-path
s-path"></a>--spec &lt;path&gt;,<br />-s &lt;path&gt;<a href="#env-create-spec-path
s-path"> [ref]</a>
      </td>
      <td>
        <span>Path to env spec.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: spec</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="env-create-json"></a>--json<a href="#env-create-json"> [ref]</a>
      </td>
      <td>
        <span>Format output as JSON.</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="env-create-nouse"></a>--no-use<a href="#env-create-nouse"> [ref]</a>
      </td>
      <td>
        <span>Don't set new env as default for future operations.</span>
        <br>
      </td>
    </tr>
  </tbody>
</table>


### rally env delete

Deletes all records related to Env from db.

<table>
  <thead>
    <tr>
      <th>Argument</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap">
        <a name="env-delete-env-uuid"></a>--env &lt;uuid&gt;<a href="#env-delete-env-uuid"> [ref]</a>
      </td>
      <td>
        <span>UUID or name of the env.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: env</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="env-delete-force"></a>--force<a href="#env-delete-force"> [ref]</a>
      </td>
      <td>
        <span>Delete DB records even if env is not destroyed.</span>
        <br>
      </td>
    </tr>
  </tbody>
</table>


### rally env destroy

Destroy existing environment.

<table>
  <thead>
    <tr>
      <th>Argument</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap">
        <a name="env-destroy-env-uuid"></a>--env &lt;uuid&gt;<a href="#env-destroy-env-uuid"> [ref]</a>
      </td>
      <td>
        <span>UUID or name of the env.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: env</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="env-destroy-skipcleanup"></a>--skip-cleanup<a href="#env-destroy-skipcleanup"> [ref]</a>
      </td>
      <td>
        <span>Do not perform platforms cleanup before destroy.</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="env-destroy-json"></a>--json<a href="#env-destroy-json"> [ref]</a>
      </td>
      <td>
        <span>Format output as JSON.</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="env-destroy-detailed"></a>--detailed<a href="#env-destroy-detailed"> [ref]</a>
      </td>
      <td>
        <span>Show detailed information.</span>
        <br>
      </td>
    </tr>
  </tbody>
</table>


### rally env info

Show environment information.

<table>
  <thead>
    <tr>
      <th>Argument</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap">
        <a name="env-info-env-uuid"></a>--env &lt;uuid&gt;<a href="#env-info-env-uuid"> [ref]</a>
      </td>
      <td>
        <span>UUID or name of the env.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: env</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="env-info-json"></a>--json<a href="#env-info-json"> [ref]</a>
      </td>
      <td>
        <span>Format output as JSON.</span>
        <br>
      </td>
    </tr>
  </tbody>
</table>


### rally env list

List existing environments.

<table>
  <thead>
    <tr>
      <th>Argument</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap">
        <a name="env-list-json"></a>--json<a href="#env-list-json"> [ref]</a>
      </td>
      <td>
        <span>Format output as JSON.</span>
        <br>
      </td>
    </tr>
  </tbody>
</table>


### rally env show



<table>
  <thead>
    <tr>
      <th>Argument</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap">
        <a name="env-show-env-uuid"></a>--env &lt;uuid&gt;<a href="#env-show-env-uuid"> [ref]</a>
      </td>
      <td>
        <span>UUID or name of the env.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: env</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="env-show-json"></a>--json<a href="#env-show-json"> [ref]</a>
      </td>
      <td>
        <span>Format output as JSON.</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="env-show-onlyspec"></a>--only-spec<a href="#env-show-onlyspec"> [ref]</a>
      </td>
      <td>
        <span>Print only a spec for the environment.</span>
        <br>
      </td>
    </tr>
  </tbody>
</table>


### rally env use

Set default environment.

<table>
  <thead>
    <tr>
      <th>Argument</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap">
        <a name="env-use-env-uuid"></a>--env &lt;uuid&gt;<a href="#env-use-env-uuid"> [ref]</a>
      </td>
      <td>
        <span>UUID or name of a env.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="env-use-json"></a>--json<a href="#env-use-json"> [ref]</a>
      </td>
      <td>
        <span>Format output as JSON.</span>
        <br>
      </td>
    </tr>
  </tbody>
</table>


## Category "plugin"

Set of commands that allow you to manage Rally plugins.

### rally plugin list

List all Rally plugins that match name and platform.

<table>
  <thead>
    <tr>
      <th>Argument</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap">
        <a name="plugin-list-name-name"></a>--name &lt;name&gt;<a href="#plugin-list-name-name"> [ref]</a>
      </td>
      <td>
        <span>List only plugins that match the given name.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: name</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="plugin-list-platform-platform"></a>--platform &lt;platform&gt;<a href="#plugin-list-platform-platform"> [ref]</a>
      </td>
      <td>
        <span>List only plugins that are in the specified platform.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: platform</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="plugin-list-namespace"></a>--namespace<a href="#plugin-list-namespace"> [ref]</a>
      </td>
      <td>
        <span>[Deprecated since Rally 0.10.0] Use '--platform' instead. </span>
        <br>
        <span>
</span>
        <br>
        <span><i>Defaults</i>: platform</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="plugin-list-pluginbase-plugin-base"></a>--plugin-base &lt;plugin_base&gt;<a href="#plugin-list-pluginbase-plugin-base"> [ref]</a>
      </td>
      <td>
        <span>Plugin base class.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: base_cls</span>
        <br>
      </td>
    </tr>
  </tbody>
</table>


### rally plugin show

Show detailed information about a Rally plugin.

<table>
  <thead>
    <tr>
      <th>Argument</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap">
        <a name="plugin-show-name-name"></a>--name &lt;name&gt;<a href="#plugin-show-name-name"> [ref]</a>
      </td>
      <td>
        <span>Plugin name.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="plugin-show-platform-platform"></a>--platform &lt;platform&gt;<a href="#plugin-show-platform-platform"> [ref]</a>
      </td>
      <td>
        <span>Plugin platform.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: platform</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="plugin-show-namespace"></a>--namespace<a href="#plugin-show-namespace"> [ref]</a>
      </td>
      <td>
        <span>[Deprecated since Rally 0.10.0] Use '--platform' instead. </span>
        <br>
        <span>
</span>
        <br>
        <span><i>Defaults</i>: platform</span>
        <br>
      </td>
    </tr>
  </tbody>
</table>


## Category "task"

Set of commands that allow you to manage tasks and results.

    

### rally task abort

Abort a running task.

<table>
  <thead>
    <tr>
      <th>Argument</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap">
        <a name="task-abort-uuid-uuid"></a>--uuid &lt;uuid&gt;<a href="#task-abort-uuid-uuid"> [ref]</a>
      </td>
      <td>
        <span>UUID of task.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="task-abort-soft"></a>--soft<a href="#task-abort-soft"> [ref]</a>
      </td>
      <td>
        <span>Abort task after current scenario finishes execution.</span>
        <br>
      </td>
    </tr>
  </tbody>
</table>


### rally task delete

Delete task and its results.

<table>
  <thead>
    <tr>
      <th>Argument</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap">
        <a name="task-delete-force"></a>--force<a href="#task-delete-force"> [ref]</a>
      </td>
      <td>
        <span>force delete</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="task-delete-uuid-taskid"></a>--uuid &lt;task-id&gt;<a href="#task-delete-uuid-taskid"> [ref]</a>
      </td>
      <td>
        <span>UUID of task or a list of task UUIDs.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
      </td>
    </tr>
  </tbody>
</table>


### rally task detailed



<table>
  <thead>
    <tr>
      <th>Argument</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap">
        <a name="task-detailed-uuid-uuid"></a>--uuid &lt;uuid&gt;<a href="#task-detailed-uuid-uuid"> [ref]</a>
      </td>
      <td>
        <span>UUID of task. If --uuid is "last" the results of  the most recently created task will be displayed.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="task-detailed-iterationsdata"></a>--iterations-data<a href="#task-detailed-iterationsdata"> [ref]</a>
      </td>
      <td>
        <span>Print detailed results for each iteration.</span>
        <br>
      </td>
    </tr>
  </tbody>
</table>


### rally task export

Export task results to the custom task's exporting system.

<table>
  <thead>
    <tr>
      <th>Argument</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap">
        <a name="task-export-uuid-uuid"></a>--uuid &lt;uuid&gt;<a href="#task-export-uuid-uuid"> [ref]</a>
      </td>
      <td>
        <span>UUIDs of tasks or json reports of tasks</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: tasks</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="task-export-type-type"></a>--type &lt;type&gt;<a href="#task-export-type-type"> [ref]</a>
      </td>
      <td>
        <span>Report type. Out-of-the-box types: JSON, HTML, HTML-Static, Elastic, JUnit-XML. HINT: You can list all types, executing `rally plugin list --plugin-base TaskExporter` command.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: output_type</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="task-export-to-dest"></a>--to &lt;dest&gt;<a href="#task-export-to-dest"> [ref]</a>
      </td>
      <td>
        <span>Report destination. Can be a path to a file (in case of JSON, HTML, HTML-Static, JUnit-XML, Elastic etc. types) to save the report to or a connection string. It depends on the report type.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: output_dest</span>
        <br>
      </td>
    </tr>
  </tbody>
</table>


### rally task import

Import json results of a test into rally database

<table>
  <thead>
    <tr>
      <th>Argument</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap">
        <a name="task-import-file-path"></a>--file &lt;path&gt;<a href="#task-import-file-path"> [ref]</a>
      </td>
      <td>
        <span>JSON file with task results</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: task_file</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="task-import-deployment-uuid"></a>--deployment &lt;uuid&gt;<a href="#task-import-deployment-uuid"> [ref]</a>
      </td>
      <td>
        <span>UUID or name of a deployment.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="task-import-tag-tag"></a>--tag &lt;tag&gt;<a href="#task-import-tag-tag"> [ref]</a>
      </td>
      <td>
        <span>Mark the task with a tag or a few tags.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: tags</span>
        <br>
      </td>
    </tr>
  </tbody>
</table>


### rally task list

List tasks, started and finished.

Displayed tasks can be filtered by status or deployment.  By
default 'rally task list' will display tasks from the active
deployment without filtering by status.

<table>
  <thead>
    <tr>
      <th>Argument</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap">
        <a name="task-list-deployment-uuid"></a>--deployment &lt;uuid&gt;<a href="#task-list-deployment-uuid"> [ref]</a>
      </td>
      <td>
        <span>UUID or name of a deployment.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="task-list-alldeployments"></a>--all-deployments<a href="#task-list-alldeployments"> [ref]</a>
      </td>
      <td>
        <span>List tasks from all deployments.</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="task-list-status-status"></a>--status &lt;status&gt;<a href="#task-list-status-status"> [ref]</a>
      </td>
      <td>
        <span>List tasks with specified status. Available statuses: aborted, aborting, crashed, finished, init, paused, running, sla_failed, soft_aborting, validated, validating, validation_failed</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: status</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="task-list-tag-tag"></a>--tag &lt;tag&gt;<a href="#task-list-tag-tag"> [ref]</a>
      </td>
      <td>
        <span>Tags to filter tasks by.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: tags</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="task-list-uuidsonly"></a>--uuids-only<a href="#task-list-uuidsonly"> [ref]</a>
      </td>
      <td>
        <span>List task UUIDs only.</span>
        <br>
      </td>
    </tr>
  </tbody>
</table>


### rally task report

Generate a report for the specified task(s).

<table>
  <thead>
    <tr>
      <th>Argument</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap">
        <a name="task-report-tasks"></a>--tasks<a href="#task-report-tasks"> [ref]</a>
      </td>
      <td>
        <span>[Deprecated since Rally 0.10.0] Use '--uuid' instead. </span>
        <br>
        <span>
</span>
        <br>
        <span><i>Defaults</i>: tasks</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="task-report-out-path"></a>--out &lt;path&gt;<a href="#task-report-out-path"> [ref]</a>
      </td>
      <td>
        <span>Report destination. Can be a path to a file (in case of HTML, HTML-STATIC, etc. types) to save the report to or a connection string.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: out</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="task-report-open"></a>--open<a href="#task-report-open"> [ref]</a>
      </td>
      <td>
        <span>Open the output in a browser.</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="task-report-html"></a>--html<a href="#task-report-html"> [ref]</a>
      </td>
      <td>
        <span></span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="task-report-htmlstatic"></a>--html-static<a href="#task-report-htmlstatic"> [ref]</a>
      </td>
      <td>
        <span></span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="task-report-json"></a>--json<a href="#task-report-json"> [ref]</a>
      </td>
      <td>
        <span></span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="task-report-junit"></a>--junit<a href="#task-report-junit"> [ref]</a>
      </td>
      <td>
        <span>[Deprecated since Rally 0.10.0] Use 'rally task export --type junit-xml' instead. </span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="task-report-uuid-uuid"></a>--uuid &lt;uuid&gt;<a href="#task-report-uuid-uuid"> [ref]</a>
      </td>
      <td>
        <span>UUIDs of tasks or json reports of tasks</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: tasks</span>
        <br>
      </td>
    </tr>
  </tbody>
</table>


### rally task results

Display raw task results.

This will produce a lot of output data about every iteration.

<table>
  <thead>
    <tr>
      <th>Argument</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap">
        <a name="task-results-uuid-uuid"></a>--uuid &lt;uuid&gt;<a href="#task-results-uuid-uuid"> [ref]</a>
      </td>
      <td>
        <span>UUID of task.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
      </td>
    </tr>
  </tbody>
</table>


### rally task sla-check

Display SLA check results table.

<table>
  <thead>
    <tr>
      <th>Argument</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap">
        <a name="task-slacheck-uuid-uuid"></a>--uuid &lt;uuid&gt;<a href="#task-slacheck-uuid-uuid"> [ref]</a>
      </td>
      <td>
        <span>UUID of task.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="task-slacheck-json"></a>--json<a href="#task-slacheck-json"> [ref]</a>
      </td>
      <td>
        <span>Output in JSON format.</span>
        <br>
      </td>
    </tr>
  </tbody>
</table>


### rally task sla_check

DEPRECATED since Rally 0.8.0, use `rally task sla-check` instead.

<table>
  <thead>
    <tr>
      <th>Argument</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap">
        <a name="task-sla-check-uuid-uuid"></a>--uuid &lt;uuid&gt;<a href="#task-sla-check-uuid-uuid"> [ref]</a>
      </td>
      <td>
        <span>UUID of task.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="task-sla-check-json"></a>--json<a href="#task-sla-check-json"> [ref]</a>
      </td>
      <td>
        <span>Output in JSON format.</span>
        <br>
      </td>
    </tr>
  </tbody>
</table>


### rally task start

Run task.

If both task_args and task_args_file are specified, they are going to
be merged. task_args has a higher priority so it overrides
values from task_args_file.
There are 3 kinds of return codes, 0: no error, 1: running error,
2: sla check failed.

<table>
  <thead>
    <tr>
      <th>Argument</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap">
        <a name="task-start-deployment-uuid"></a>--deployment &lt;uuid&gt;<a href="#task-start-deployment-uuid"> [ref]</a>
      </td>
      <td>
        <span>UUID or name of a deployment.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="task-start-task-path
filename-path"></a>--task &lt;path&gt;,<br />--filename &lt;path&gt;<a href="#task-start-task-path
filename-path"> [ref]</a>
      </td>
      <td>
        <span>Path to the input task file.</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="task-start-taskargs-json"></a>--task-args &lt;json&gt;<a href="#task-start-taskargs-json"> [ref]</a>
      </td>
      <td>
        <span>Input task args (JSON dict). These args are used to render the Jinja2 template in the input task.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Defaults</i>: task_args</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="task-start-taskargsfile-path"></a>--task-args-file &lt;path&gt;<a href="#task-start-taskargsfile-path"> [ref]</a>
      </td>
      <td>
        <span>Path to the file with input task args (dict in JSON/YAML). These args are used to render the Jinja2 template in the input task.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Defaults</i>: task_args_file</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="task-start-tag-tag"></a>--tag &lt;tag&gt;<a href="#task-start-tag-tag"> [ref]</a>
      </td>
      <td>
        <span>Mark the task with a tag or a few tags.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: tags</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="task-start-nouse"></a>--no-use<a href="#task-start-nouse"> [ref]</a>
      </td>
      <td>
        <span>Don't set new task as default for future operations.</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="task-start-abortonslafailure"></a>--abort-on-sla-failure<a href="#task-start-abortonslafailure"> [ref]</a>
      </td>
      <td>
        <span>Abort the execution of a task when any SLA check for it fails for subtask or workload.</span>
        <br>
      </td>
    </tr>
  </tbody>
</table>


### rally task status

Display the current status of a task.

<table>
  <thead>
    <tr>
      <th>Argument</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap">
        <a name="task-status-uuid-uuid"></a>--uuid &lt;uuid&gt;<a href="#task-status-uuid-uuid"> [ref]</a>
      </td>
      <td>
        <span>UUID of task</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
      </td>
    </tr>
  </tbody>
</table>


### rally task trends

Generate workloads trends HTML report.

<table>
  <thead>
    <tr>
      <th>Argument</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap">
        <a name="task-trends-out-path"></a>--out &lt;path&gt;<a href="#task-trends-out-path"> [ref]</a>
      </td>
      <td>
        <span>Path to output file.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="task-trends-open"></a>--open<a href="#task-trends-open"> [ref]</a>
      </td>
      <td>
        <span>Open the output in a browser.</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="task-trends-tasks-tasks"></a>--tasks &lt;tasks&gt;<a href="#task-trends-tasks-tasks"> [ref]</a>
      </td>
      <td>
        <span>UUIDs of tasks, or JSON files with task results</span>
        <br>
      </td>
    </tr>
  </tbody>
</table>


### rally task use

Set active task.

<table>
  <thead>
    <tr>
      <th>Argument</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap">
        <a name="task-use-uuid-uuid"></a>--uuid &lt;uuid&gt;<a href="#task-use-uuid-uuid"> [ref]</a>
      </td>
      <td>
        <span>UUID of the task</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="task-use-task"></a>--task<a href="#task-use-task"> [ref]</a>
      </td>
      <td>
        <span>[Deprecated since Rally 0.2.0] Use '--uuid' instead. </span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
      </td>
    </tr>
  </tbody>
</table>


### rally task validate

Validate a task configuration file.

This will check that task configuration file has valid syntax and
all required options of scenarios, contexts, SLA and runners are set.

If both task_args and task_args_file are specified, they will
be merged. task_args has a higher priority so it will override
values from task_args_file.

<table>
  <thead>
    <tr>
      <th>Argument</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap">
        <a name="task-validate-deployment-uuid"></a>--deployment &lt;uuid&gt;<a href="#task-validate-deployment-uuid"> [ref]</a>
      </td>
      <td>
        <span>UUID or name of a deployment.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="task-validate-task-path
filename-path"></a>--task &lt;path&gt;,<br />--filename &lt;path&gt;<a href="#task-validate-task-path
filename-path"> [ref]</a>
      </td>
      <td>
        <span>Path to the input task file.</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="task-validate-taskargs-json"></a>--task-args &lt;json&gt;<a href="#task-validate-taskargs-json"> [ref]</a>
      </td>
      <td>
        <span>Input task args (JSON dict). These args are used to render the Jinja2 template in the input task.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Defaults</i>: task_args</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="task-validate-taskargsfile-path"></a>--task-args-file &lt;path&gt;<a href="#task-validate-taskargsfile-path"> [ref]</a>
      </td>
      <td>
        <span>Path to the file with input task args (dict in JSON/YAML). These args are used to render the Jinja2 template in the input task.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Defaults</i>: task_args_file</span>
        <br>
      </td>
    </tr>
  </tbody>
</table>


## Category "verify"

Verify an OpenStack cloud via a verifier.

### rally verify add-verifier-ext

Add a verifier extension.

<table>
  <thead>
    <tr>
      <th>Argument</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-addverifierext-id-id"></a>--id &lt;id&gt;<a href="#verify-addverifierext-id-id"> [ref]</a>
      </td>
      <td>
        <span>Verifier name or UUID. HINT: You can list all verifiers, executing command `rally verify list-verifiers`.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: verifier_id</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-addverifierext-source-source"></a>--source &lt;source&gt;<a href="#verify-addverifierext-source-source"> [ref]</a>
      </td>
      <td>
        <span>Path or URL to the repo to clone verifier extension from.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: source</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-addverifierext-version-version"></a>--version &lt;version&gt;<a href="#verify-addverifierext-version-version"> [ref]</a>
      </td>
      <td>
        <span>Branch, tag or commit ID to checkout before installation of the verifier extension (the 'master' branch is used by default).</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: version</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-addverifierext-extrasettings-extra-settings"></a>--extra-settings &lt;extra_settings&gt;<a href="#verify-addverifierext-extrasettings-extra-settings"> [ref]</a>
      </td>
      <td>
        <span>Extra installation settings for verifier extension.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: extra</span>
        <br>
      </td>
    </tr>
  </tbody>
</table>


### rally verify configure-verifier

Configure a verifier for a specific deployment.

<table>
  <thead>
    <tr>
      <th>Argument</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-configureverifier-id-id"></a>--id &lt;id&gt;<a href="#verify-configureverifier-id-id"> [ref]</a>
      </td>
      <td>
        <span>Verifier name or UUID. HINT: You can list all verifiers, executing command `rally verify list-verifiers`.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: verifier_id</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-configureverifier-deploymentid-id"></a>--deployment-id &lt;id&gt;<a href="#verify-configureverifier-deploymentid-id"> [ref]</a>
      </td>
      <td>
        <span>Deployment name or UUID. HINT: You can list all deployments, executing command `rally deployment list`.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-configureverifier-reconfigure"></a>--reconfigure<a href="#verify-configureverifier-reconfigure"> [ref]</a>
      </td>
      <td>
        <span>Reconfigure verifier.</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-configureverifier-extend-path/json/yaml"></a>--extend &lt;path/json/yaml&gt;<a href="#verify-configureverifier-extend-path/json/yaml"> [ref]</a>
      </td>
      <td>
        <span>Extend verifier configuration with extra options. If options are already present, the given ones will override them. Can be a path to a regular config file or just a json/yaml.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: extra_options</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-configureverifier-override-path"></a>--override &lt;path&gt;<a href="#verify-configureverifier-override-path"> [ref]</a>
      </td>
      <td>
        <span>Override verifier configuration by another one from a given source.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: new_configuration</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-configureverifier-show"></a>--show<a href="#verify-configureverifier-show"> [ref]</a>
      </td>
      <td>
        <span>Show verifier configuration.</span>
        <br>
      </td>
    </tr>
  </tbody>
</table>


### rally verify create-verifier

Create a verifier.

<table>
  <thead>
    <tr>
      <th>Argument</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-createverifier-name-name"></a>--name &lt;name&gt;<a href="#verify-createverifier-name-name"> [ref]</a>
      </td>
      <td>
        <span>Verifier name (for example, 'My verifier').</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-createverifier-type-type"></a>--type &lt;type&gt;<a href="#verify-createverifier-type-type"> [ref]</a>
      </td>
      <td>
        <span>Verifier plugin name. HINT: You can list all verifier plugins, executing command `rally verify list-plugins`.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-createverifier-platform-platform"></a>--platform &lt;platform&gt;<a href="#verify-createverifier-platform-platform"> [ref]</a>
      </td>
      <td>
        <span>Verifier plugin platform. Should be specified in case of two verifier plugins with equal names but in different platforms.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: platform</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-createverifier-namespace"></a>--namespace<a href="#verify-createverifier-namespace"> [ref]</a>
      </td>
      <td>
        <span>[Deprecated since Rally 0.10.0] Use '--platform' instead. </span>
        <br>
        <span>
</span>
        <br>
        <span><i>Defaults</i>: platform</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-createverifier-source-source"></a>--source &lt;source&gt;<a href="#verify-createverifier-source-source"> [ref]</a>
      </td>
      <td>
        <span>Path or URL to the repo to clone verifier from.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: source</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-createverifier-version-version"></a>--version &lt;version&gt;<a href="#verify-createverifier-version-version"> [ref]</a>
      </td>
      <td>
        <span>Branch, tag or commit ID to checkout before verifier installation (the 'master' branch is used by default).</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: version</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-createverifier-systemwide"></a>--system-wide<a href="#verify-createverifier-systemwide"> [ref]</a>
      </td>
      <td>
        <span>Use the system-wide environment for verifier instead of a virtual environment.</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-createverifier-extrasettings-extra-settings"></a>--extra-settings &lt;extra_settings&gt;<a href="#verify-createverifier-extrasettings-extra-settings"> [ref]</a>
      </td>
      <td>
        <span>Extra installation settings for verifier.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: extra</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-createverifier-nouse"></a>--no-use<a href="#verify-createverifier-nouse"> [ref]</a>
      </td>
      <td>
        <span>Not to set the created verifier as the default verifier for future operations.</span>
        <br>
      </td>
    </tr>
  </tbody>
</table>


### rally verify delete

Delete a verification or a few verifications.

<table>
  <thead>
    <tr>
      <th>Argument</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-delete-uuid-uuid"></a>--uuid &lt;uuid&gt;<a href="#verify-delete-uuid-uuid"> [ref]</a>
      </td>
      <td>
        <span>UUIDs of verifications. HINT: You can list all verifications, executing command `rally verify list`.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
      </td>
    </tr>
  </tbody>
</table>


### rally verify delete-verifier

Delete a verifier.

<table>
  <thead>
    <tr>
      <th>Argument</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-deleteverifier-id-id"></a>--id &lt;id&gt;<a href="#verify-deleteverifier-id-id"> [ref]</a>
      </td>
      <td>
        <span>Verifier name or UUID. HINT: You can list all verifiers, executing command `rally verify list-verifiers`.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-deleteverifier-deploymentid-id"></a>--deployment-id &lt;id&gt;<a href="#verify-deleteverifier-deploymentid-id"> [ref]</a>
      </td>
      <td>
        <span>Deployment name or UUID. If specified, only the deployment-specific data will be deleted for verifier. HINT: You can list all deployments, executing command `rally deployment list`.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-deleteverifier-force"></a>--force<a href="#verify-deleteverifier-force"> [ref]</a>
      </td>
      <td>
        <span>Delete all stored verifications of the specified verifier. If a deployment specified, only verifications of this deployment will be deleted. Use this argument carefully! You can delete verifications that may be important to you.</span>
        <br>
      </td>
    </tr>
  </tbody>
</table>


### rally verify delete-verifier-ext

Delete a verifier extension.

<table>
  <thead>
    <tr>
      <th>Argument</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-deleteverifierext-id-id"></a>--id &lt;id&gt;<a href="#verify-deleteverifierext-id-id"> [ref]</a>
      </td>
      <td>
        <span>Verifier name or UUID. HINT: You can list all verifiers, executing command `rally verify list-verifiers`.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: verifier_id</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-deleteverifierext-name-name"></a>--name &lt;name&gt;<a href="#verify-deleteverifierext-name-name"> [ref]</a>
      </td>
      <td>
        <span>Verifier extension name.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: name</span>
        <br>
      </td>
    </tr>
  </tbody>
</table>


### rally verify import

Import results of a test run into the Rally database.

<table>
  <thead>
    <tr>
      <th>Argument</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-import-id-id"></a>--id &lt;id&gt;<a href="#verify-import-id-id"> [ref]</a>
      </td>
      <td>
        <span>Verifier name or UUID. HINT: You can list all verifiers, executing command `rally verify list-verifiers`.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: verifier_id</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-import-deploymentid-id"></a>--deployment-id &lt;id&gt;<a href="#verify-import-deploymentid-id"> [ref]</a>
      </td>
      <td>
        <span>Deployment name or UUID. HINT: You can list all deployments, executing command `rally deployment list`.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-import-file-path"></a>--file &lt;path&gt;<a href="#verify-import-file-path"> [ref]</a>
      </td>
      <td>
        <span>File to import test results from.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: file_to_parse</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-import-runargs-run-args"></a>--run-args &lt;run_args&gt;<a href="#verify-import-runargs-run-args"> [ref]</a>
      </td>
      <td>
        <span>Arguments that might be used when running tests. For example, '{concurrency: 2, pattern: set=identity}'.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: run_args</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-import-nouse"></a>--no-use<a href="#verify-import-nouse"> [ref]</a>
      </td>
      <td>
        <span>Not to set the created verification as the default verification for future operations.</span>
        <br>
      </td>
    </tr>
  </tbody>
</table>


### rally verify list

List all verifications.

<table>
  <thead>
    <tr>
      <th>Argument</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-list-id-id"></a>--id &lt;id&gt;<a href="#verify-list-id-id"> [ref]</a>
      </td>
      <td>
        <span>Verifier name or UUID. HINT: You can list all verifiers, executing command `rally verify list-verifiers`.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: verifier_id</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-list-deploymentid-id"></a>--deployment-id &lt;id&gt;<a href="#verify-list-deploymentid-id"> [ref]</a>
      </td>
      <td>
        <span>Deployment name or UUID. HINT: You can list all deployments, executing command `rally deployment list`.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-list-tag-tag"></a>--tag &lt;tag&gt;<a href="#verify-list-tag-tag"> [ref]</a>
      </td>
      <td>
        <span>Tags to filter verifications by.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: tags</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-list-status-status"></a>--status &lt;status&gt;<a href="#verify-list-status-status"> [ref]</a>
      </td>
      <td>
        <span>Status to filter verifications by.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: status</span>
        <br>
      </td>
    </tr>
  </tbody>
</table>


### rally verify list-plugins

List all plugins for verifiers management.

<table>
  <thead>
    <tr>
      <th>Argument</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-listplugins-platform-platform"></a>--platform &lt;platform&gt;<a href="#verify-listplugins-platform-platform"> [ref]</a>
      </td>
      <td>
        <span>Requried patform (e.g. openstack).</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: platform</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-listplugins-namespace"></a>--namespace<a href="#verify-listplugins-namespace"> [ref]</a>
      </td>
      <td>
        <span>[Deprecated since Rally 0.10.0] Use '--platform' instead. </span>
        <br>
        <span>
</span>
        <br>
        <span><i>Defaults</i>: platform</span>
        <br>
      </td>
    </tr>
  </tbody>
</table>


### rally verify list-verifier-exts

List all verifier extensions.

<table>
  <thead>
    <tr>
      <th>Argument</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-listverifierexts-id-id"></a>--id &lt;id&gt;<a href="#verify-listverifierexts-id-id"> [ref]</a>
      </td>
      <td>
        <span>Verifier name or UUID. HINT: You can list all verifiers, executing command `rally verify list-verifiers`.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: verifier_id</span>
        <br>
      </td>
    </tr>
  </tbody>
</table>


### rally verify list-verifier-tests

List all verifier tests.

<table>
  <thead>
    <tr>
      <th>Argument</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-listverifiertests-id-id"></a>--id &lt;id&gt;<a href="#verify-listverifiertests-id-id"> [ref]</a>
      </td>
      <td>
        <span>Verifier name or UUID. HINT: You can list all verifiers, executing command `rally verify list-verifiers`.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: verifier_id</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-listverifiertests-pattern-pattern"></a>--pattern &lt;pattern&gt;<a href="#verify-listverifiertests-pattern-pattern"> [ref]</a>
      </td>
      <td>
        <span>Pattern which will be used for matching. Can be a regexp or a verifier-specific entity (for example, in case of Tempest you can specify 'set=smoke').</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: pattern</span>
        <br>
      </td>
    </tr>
  </tbody>
</table>


### rally verify list-verifiers

List all verifiers.

<table>
  <thead>
    <tr>
      <th>Argument</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-listverifiers-status-status"></a>--status &lt;status&gt;<a href="#verify-listverifiers-status-status"> [ref]</a>
      </td>
      <td>
        <span>Status to filter verifiers by.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: status</span>
        <br>
      </td>
    </tr>
  </tbody>
</table>


### rally verify report

Generate a report for a verification or a few verifications.

<table>
  <thead>
    <tr>
      <th>Argument</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-report-uuid-uuid"></a>--uuid &lt;uuid&gt;<a href="#verify-report-uuid-uuid"> [ref]</a>
      </td>
      <td>
        <span>UUIDs of verifications. HINT: You can list all verifications, executing command `rally verify list`.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: verification_uuid</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-report-type-type"></a>--type &lt;type&gt;<a href="#verify-report-type-type"> [ref]</a>
      </td>
      <td>
        <span>Report type (Defaults to JSON). Out-of-the-box types: HTML, HTML-Static, JSON, JUnit-XML. HINT: You can list all types, executing `rally plugin list --plugin-base VerificationReporter` command.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: output_type</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-report-to-dest"></a>--to &lt;dest&gt;<a href="#verify-report-to-dest"> [ref]</a>
      </td>
      <td>
        <span>Report destination. Can be a path to a file (in case of HTML, JSON, etc. types) to save the report to or a connection string. It depends on the report type.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: output_dest</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-report-open"></a>--open<a href="#verify-report-open"> [ref]</a>
      </td>
      <td>
        <span>Open the output file in a browser.</span>
        <br>
      </td>
    </tr>
  </tbody>
</table>


### rally verify rerun

Rerun tests from a verification for a specific deployment.

<table>
  <thead>
    <tr>
      <th>Argument</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-rerun-uuid-uuid"></a>--uuid &lt;uuid&gt;<a href="#verify-rerun-uuid-uuid"> [ref]</a>
      </td>
      <td>
        <span>Verification UUID. HINT: You can list all verifications, executing command `rally verify list`.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: verification_uuid</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-rerun-deploymentid-id"></a>--deployment-id &lt;id&gt;<a href="#verify-rerun-deploymentid-id"> [ref]</a>
      </td>
      <td>
        <span>Deployment name or UUID. HINT: You can list all deployments, executing command `rally deployment list`.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-rerun-failed"></a>--failed<a href="#verify-rerun-failed"> [ref]</a>
      </td>
      <td>
        <span>Rerun only failed tests.</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-rerun-tag-tag"></a>--tag &lt;tag&gt;<a href="#verify-rerun-tag-tag"> [ref]</a>
      </td>
      <td>
        <span>Mark verification with a tag or a few tags.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: tags</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-rerun-concurrency-N"></a>--concurrency &lt;N&gt;<a href="#verify-rerun-concurrency-N"> [ref]</a>
      </td>
      <td>
        <span>How many processes to be used for running verifier tests. The default value (0) auto-detects your CPU count.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: int</span>
        <br>
        <span><i>Defaults</i>: concur</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-rerun-detailed"></a>--detailed<a href="#verify-rerun-detailed"> [ref]</a>
      </td>
      <td>
        <span>Show verification details such as errors of failed tests.</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-rerun-nouse"></a>--no-use<a href="#verify-rerun-nouse"> [ref]</a>
      </td>
      <td>
        <span>Not to set the finished verification as the default verification for future operations.</span>
        <br>
      </td>
    </tr>
  </tbody>
</table>


### rally verify show

Show detailed information about a verification.

<table>
  <thead>
    <tr>
      <th>Argument</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-show-uuid-uuid"></a>--uuid &lt;uuid&gt;<a href="#verify-show-uuid-uuid"> [ref]</a>
      </td>
      <td>
        <span>Verification UUID. HINT: You can list all verifications, executing command `rally verify list`.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: verification_uuid</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-show-sortby-query"></a>--sort-by &lt;query&gt;<a href="#verify-show-sortby-query"> [ref]</a>
      </td>
      <td>
        <span>Sort tests by 'name', 'duration' or 'status'.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: sort_by</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-show-detailed"></a>--detailed<a href="#verify-show-detailed"> [ref]</a>
      </td>
      <td>
        <span>Show verification details such as run arguments and errors of failed tests.</span>
        <br>
      </td>
    </tr>
  </tbody>
</table>


### rally verify show-verifier

Show detailed information about a verifier.

<table>
  <thead>
    <tr>
      <th>Argument</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-showverifier-id-id"></a>--id &lt;id&gt;<a href="#verify-showverifier-id-id"> [ref]</a>
      </td>
      <td>
        <span>Verifier name or UUID. HINT: You can list all verifiers, executing command `rally verify list-verifiers`.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: verifier_id</span>
        <br>
      </td>
    </tr>
  </tbody>
</table>


### rally verify start

Start a verification (run verifier tests).

<table>
  <thead>
    <tr>
      <th>Argument</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-start-id-id"></a>--id &lt;id&gt;<a href="#verify-start-id-id"> [ref]</a>
      </td>
      <td>
        <span>Verifier name or UUID. HINT: You can list all verifiers, executing command `rally verify list-verifiers`.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: verifier_id</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-start-deploymentid-id"></a>--deployment-id &lt;id&gt;<a href="#verify-start-deploymentid-id"> [ref]</a>
      </td>
      <td>
        <span>Deployment name or UUID. HINT: You can list all deployments, executing command `rally deployment list`.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-start-tag-tag"></a>--tag &lt;tag&gt;<a href="#verify-start-tag-tag"> [ref]</a>
      </td>
      <td>
        <span>Mark verification with a tag or a few tags.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: tags</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-start-pattern-pattern"></a>--pattern &lt;pattern&gt;<a href="#verify-start-pattern-pattern"> [ref]</a>
      </td>
      <td>
        <span>Pattern which will be used for running tests. Can be a regexp or a verifier-specific entity (for example, in case of Tempest you can specify 'set=smoke').</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: pattern</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-start-concurrency-N"></a>--concurrency &lt;N&gt;<a href="#verify-start-concurrency-N"> [ref]</a>
      </td>
      <td>
        <span>How many processes to be used for running verifier tests. The default value (0) auto-detects your CPU count.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: int</span>
        <br>
        <span><i>Defaults</i>: concur</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-start-loadlist-path"></a>--load-list &lt;path&gt;<a href="#verify-start-loadlist-path"> [ref]</a>
      </td>
      <td>
        <span>Path to a file with a list of tests to run.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: load_list</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-start-skiplist-path"></a>--skip-list &lt;path&gt;<a href="#verify-start-skiplist-path"> [ref]</a>
      </td>
      <td>
        <span>Path to a file with a list of tests to skip. Format: json or yaml like a dictionary where keys are test names and values are reasons.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: skip_list</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-start-xfaillist-path"></a>--xfail-list &lt;path&gt;<a href="#verify-start-xfaillist-path"> [ref]</a>
      </td>
      <td>
        <span>Path to a file with a list of tests that will be considered as expected failures. Format: json or yaml like a dictionary where keys are test names and values are reasons.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: xfail_list</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-start-detailed"></a>--detailed<a href="#verify-start-detailed"> [ref]</a>
      </td>
      <td>
        <span>Show verification details such as errors of failed tests.</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-start-nouse"></a>--no-use<a href="#verify-start-nouse"> [ref]</a>
      </td>
      <td>
        <span>Not to set the finished verification as the default verification for future operations.</span>
        <br>
      </td>
    </tr>
  </tbody>
</table>


### rally verify update-verifier

Update a verifier.

<table>
  <thead>
    <tr>
      <th>Argument</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-updateverifier-id-id"></a>--id &lt;id&gt;<a href="#verify-updateverifier-id-id"> [ref]</a>
      </td>
      <td>
        <span>Verifier name or UUID. HINT: You can list all verifiers, executing command `rally verify list-verifiers`.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: verifier_id</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-updateverifier-updatevenv"></a>--update-venv<a href="#verify-updateverifier-updatevenv"> [ref]</a>
      </td>
      <td>
        <span>Update the virtual environment for verifier.</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-updateverifier-version-version"></a>--version &lt;version&gt;<a href="#verify-updateverifier-version-version"> [ref]</a>
      </td>
      <td>
        <span>Branch, tag or commit ID to checkout. HINT: Specify the same version to pull the latest repo code.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
        <span><i>Defaults</i>: version</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-updateverifier-systemwide"></a>--system-wide<a href="#verify-updateverifier-systemwide"> [ref]</a>
      </td>
      <td>
        <span>Switch to using the system-wide environment.</span>
        <br>
      </td>
    </tr>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-updateverifier-nosystemwide"></a>--no-system-wide<a href="#verify-updateverifier-nosystemwide"> [ref]</a>
      </td>
      <td>
        <span>Switch to using the virtual environment. If the virtual environment doesn't exist, it will be created.</span>
        <br>
      </td>
    </tr>
  </tbody>
</table>


### rally verify use

Choose a verification to use for the future operations.

<table>
  <thead>
    <tr>
      <th>Argument</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-use-uuid-uuid"></a>--uuid &lt;uuid&gt;<a href="#verify-use-uuid-uuid"> [ref]</a>
      </td>
      <td>
        <span>Verification UUID. HINT: You can list all verifications, executing command `rally verify list`.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
      </td>
    </tr>
  </tbody>
</table>


### rally verify use-verifier

Choose a verifier to use for the future operations.

<table>
  <thead>
    <tr>
      <th>Argument</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap">
        <a name="verify-useverifier-id-id"></a>--id &lt;id&gt;<a href="#verify-useverifier-id-id"> [ref]</a>
      </td>
      <td>
        <span>Verifier name or UUID. HINT: You can list all verifiers, executing command `rally verify list-verifiers`.</span>
        <br>
        <span>
</span>
        <br>
        <span><i>Type</i>: str</span>
        <br>
      </td>
    </tr>
  </tbody>
</table>
