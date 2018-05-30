# Upgrades

Upgrading xRally is simple task:

```bash
# backup your db
pip install -U rally
rally db upgrade
```

## Database upgrades in depth

### For users

Rally supports DB schema versioning (schema versions are called *revisions*)
and migration (upgrade to the latest revision).

To print current revision use: ```rally db revision```

To upgrade DB to the latest state use: ```rally db upgrade```

!!! warning

    xRally does NOT support DB schema downgrade. One should consider
    backing up existing database in order to be able to rollback the change.

### For developers

DB migration in xRally is implemented via package *alembic*.

It is highly recommended to get familiar with it's 
[documentation](<a href="http://alembic.zzzcomputing.com/en/latest/) before 
proceeding.

If developer is about to change existing DB schema they should
create a new DB revision and a migration script with the following command.

```bash
alembic --config rally/common/db/alembic.ini revision -m <Message>
```

or

```bash
alembic --config rally/common/db/alembic.ini revision --autogenerate -m <Message>
```

It generates migration script -- a file named `YYYY_MM_<UUID>_<Message>.py`
located in `rally/common/db/sqlalchemy/migrations/versions`.

Alembic with parameter ``--autogenerate`` makes some "routine" job for
developer, for example it makes some SQLite compatible batch expressions for
migrations.

Generated script should then be checked, edited if it is needed to be
and added to Rally source tree.

!!! warning

    Even though alembic supports schema downgrade, migration
    scripts provided along with Rally do not contain actual code for downgrade.
