from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from fastapi import FastAPI

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.relpath('../'))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from app.orm import Base
from app.database.dbengine import engine, get_db
# This is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Add your model's MetaData object here for 'autogenerate' support.
# This should be a string name, not the actual object.
# For example:
# target_metadata = None
target_metadata = Base.metadata

# other values from the ini file, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


# Interpret the config file for Python logging.
# This line sets up loggers basically.
# from logging.config import fileConfig

# fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# target_metadata = mymodel.Base.metadata

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
    
    context.configure(url=url)

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    # this callback is used to prevent an error caused by SQLAlchemy 1.4
    # see <https://github.com/sqlalchemy/sqlalchemy/issues/6141>
    def process_revision_directives(context, revision, directives):
        if config.cmd_opts.autogenerate:
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                return

        for directive in directives:
            if directive.upgrade_ops.is_empty():
                directives.remove(directive)

    connectable = engine

    # access to the app object from the context
    context.app = FastAPI()
    context.app.dependency_overrides[get_db] = lambda: SessionLocal()
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            process_revision_directives=process_revision_directives,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

