import os
from logging.config import fileConfig
from sqlalchemy import create_engine
from alembic import context

# додаємо шлях до модулів
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from decouple import config

from models.car import Base as CarBase
from models.car_link import Base as CarLinkBase

# metadata всіх моделей
target_metadata = [CarBase.metadata, CarLinkBase.metadata]

# читаємо DATABASE_URL через Decouple
DATABASE_URL = config("DATABASE_URL")
print(f"DEBUG: Connecting to {DATABASE_URL}")
# logging
fileConfig(context.config.config_file_name)

def run_migrations_offline():
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = create_engine(DATABASE_URL)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
