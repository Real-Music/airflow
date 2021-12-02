import os
import glob
from logging.config import fileConfig
import traceback

from sqlalchemy import engine_from_config
from sqlalchemy import pool
import sqlalchemy

from alembic import context
from alembic.util.exc import CommandError
from app import Base_Model
from app.utils.terminal import print_to_console

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base_Model.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


def run_migrations():
    print_to_console("Running migrations...")

    if context.is_offline_mode():
        run_migrations_offline()

    else:
        run_migrations_online()

    print_to_console("Done running migrations...")


def migration_helper():
    database_url = config.get_main_option("sqlalchemy.url")
    engine = sqlalchemy.create_engine(database_url)

    # Get latest alembic revision id from file system.
    alembic_version_files = glob.glob(
        os.path.join(os.path.abspath(os.path.dirname(__file__)), "versions/*.py")
    )
    latest_alembic_version_file = max(alembic_version_files, key=os.path.getctime)
    latest_alembic_version_filename = os.path.basename(latest_alembic_version_file)
    latest_alembic_version = latest_alembic_version_filename.split("_")[0]

    # with engine.connect() as connection:
    with engine.connect() as connection:
        connection.execute(
            statement=sqlalchemy.text("DROP TABLE IF EXISTS alembic_version")
        )
        connection.execute(
            statement=sqlalchemy.text(
                "CREATE TABLE alembic_version (version_num VARCHAR(32), PRIMARY KEY (version_num))"
            )
        )
        connection.execute(
            statement=sqlalchemy.text(
                f"INSERT INTO alembic_version (version_num) VALUES ('{latest_alembic_version}')"
            )
        )


def run():
    # Ensure versions directory exist
    versions_dir_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "versions"
    )
    if not os.path.exists(versions_dir_path):
        os.makedirs(versions_dir_path)

    migration_passed = False

    while not migration_passed:
        try:
            run_migrations()

            # Migration Done
            migration_passed = True
            break

        except CommandError:
            # Run Migration Helper
            migration_helper()

            # Run migrations
            run_migrations()

            # Migration Done
            migration_passed = True
            break

        except Exception as exception:
            traceback.print_exc()
            print_to_console(exception)


# Run Migrations
run()
