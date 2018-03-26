# Terms and their meanings

## Common Terms


xRally is testing framework and tool that unifies all testing approaches: functional, concurrency, regression, performance, load, scale and even chaos using composition of plugins. It's designed to solve problem of testing complex platforms and it's suitable for testing of any platforms or service: like OpenStack, Kubernetes, Mesos, Docker, AWS, Google Cloud, Azure, (put your here)

<table>
    <thead>
        <tr>
            <th nowrap> Term </th>
            <th> Meaning </th>
        <tr>
    </thead>
    <tbody>
        <tr>
            <td nowrap>Alembic</td>
            <td> Lightweight database migration tool which powers Rally migrations. Read more at <a href="http://alembic.readthedocs.io/en/latest/"> Official Alembic documentation</a></td>
        </tr>
        <tr>
            <td nowrap>DB Migrations</td>
            <td>Rally supports database schema and data transformations, which are also known as migrations. This allows you easily update to newer version of Rally keeping all your data in sync.</td>
        </tr>
        <tr>
            <td nowrap>xRally config</td>
            <td>Rally behavior can be customized by editing its configuration file, <b>rally.conf*</b>, in <a href="https://docs.python.org/3.4/library/configparser.html">configparser format</a> . While being installed, Rally generates a config with default values from its <a href="https://github.com/openstack/rally/blob/master/etc/rally/rally.conf.sample">sample</a> When started, Rally searches for its config in next directories: "<sys.prefix>/etc/rally/rally.conf", "~/.rally/rally.conf", "/etc/rally/rally.conf"</td>
        </tr>
        <tr>
            <td nowrap>Rally DB</td>
            <td>Rally uses a relational database as data storage. Several database backends are supported: SQLite (default), PostgreSQL, and MySQL. The database connection can be set via the configuration file option <b>[database]/connection</b></td>.
        </tr>
        <tr>
            <td nowrap>Rally Plugin</td>
            <td>Rally is heavily plugable product. It's core is relative small, that just glue and executes properly plugins and persist the results to DB. Plugins are responsible to do actually work, like calling APIs, checking results, exporting data and so on. Plugins are just regular python classes grouped by their type (base plugin) which defines interface that should be implemented.
            <a href="/plugins">Read more about plugins here</a>
            </td>
        </tr>
    </tbody>
</table>

## Env Terms

Env component is one of key component in xRally, It manages and stores information
about tested platforms. Env manager is using platform plugins to:
create, delete, cleanup, check health, obtain information about platforms.
Every Env consists of:

- unique name and UUID
- dates when it was created and updated
- default config override
- platform plugins spec which are used to create platform
- as well as platform & plugin data which are used by other platform commands

Env data is consumed by other rally components, like task and verify


<table>
    <thead>
        <tr>
            <th nowrap> Term </th>
            <th> Meaning </th>
        <tr>
    </thead>
    <tbody>
        <tr>
            <td nowrap>Env Spec</td>
            <td>YAML file with with complete information about env, used by env create command to create env record</td>
        </tr>
        <tr>
            <td nowrap>Env Platform</td>
            <td>Plugin that is used to manage platform data (creds) and state. Samples of platforms: OpenStack, Kubernetes, Docker, AWS, Azure, Libvirt, ... </td>
        </tr>
    </tbody>
</table>

## Task Terms

Task component is responsible for executing tests defined in task specs,
persisting and reporting results.

<table>
    <thead>
        <tr>
            <th nowrap> Term </th>
            <th> Meaning </th>
        <tr>
    </thead>
    <tbody>
        <tr>
            <td nowrap>Task Plugin: Context </td>
            <td>Context plugins are responsible for creating environment in which scenario is run. For example, creating users, adding roles, setting up quotas and so on</td>
        </tr>
        <tr>
            <td nowrap>Task Plugin: Runner</td>
            <td>Plugin tha executes scenario plugin multiple time to achieve required load profile.</td>
        </tr>
        <tr>
            <td nowrap>Task Plugin: Scneario</td>
            <td>Set of actions by user against the platform. Authenticate, Create product, delete product. Scenario is executed by runner multiple time inside the context created by contexts plugins.</td>
        </tr>
        <tr>
            <td nowrap>Task Plugin: SLA</td>
            <td>Plugin that recieves the results of scenario execution and decides whatever results are matching SLA</td>
        </tr>
        <tr>
            <td nowrap>Task Plugin: Hook</td>
            <td>Plugin that allows to introduce custom action after some iteration or some time. Makes it possible to do chaos and performance testing together!<td>
        </tr>
        <tr>
            <td nowrap> Task Iteration</td>
            <td> One of scenario runs, sometimes points order number of scenario execution used by task runner.</td>
        </tr>
        <tr>
            <td nowrap>Task Spec</td>
            <td>A file that describes how to run a Rally Task. It can be in JSON or YAML format.  The <b>rally task start</b> command needs this file to run the task. The input task is pre-processed by the <a href="http://jinja.pocoo.org/">Jinja2</a> templating engine so it is very easy to create repeated parts or calculate specific values at runtime. It is also possible to pass values via CLI arguments, using the <b>--task-args</b> or <b>--task-args-file</b> options.
            </td>
        </tr>

        <tr>
            <td nowrap>Task Spec: Subtask</td>
            <td>Task consists of multiple subtasks, basically subtask is just a test case</td>
        </tr>
        <tr>
            <td nowrap>Task Spec: Workload</td>
            <td>Every subtask consists of workloads, and how to execute workloads (serial or parallel). Workload combines scenario, runner, context and SLA defining minimal executable entity.</td>
        </tr>

    </tbody>
</table>

## Verify Terms

Verify Component allows to wrap subunit-based testing tools and provide
complete tool on top of them with allow to do pre configuration, post
cleanup as well process and persist results to Rally DB for future use
like reporting and results comparing.

<table>
    <thead>
        <tr>
            <th nowrap> Term </th>
            <th> Meaning </th>
        <tr>
    </thead>
    <tbody>
        <tr>
            <td>Verification</td>
            <td>Process of execution xrally verify command that runs underlying tool, collecting results and storing them in xRally database</td>
        </tr>
    </tbody>
</table>
