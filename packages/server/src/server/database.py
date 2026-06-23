from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

# URL for Database connection
DB_URL = 'sqlite:///./byte_server.db'

# database connection
engine = create_engine(
    DB_URL, connect_args={'check_same_thread': False}
)

# Creates the database session for Object Relational Mapping (orm)
# Allows for editing on the session before committing changes to the database
# (refer to a crud file; notice the query calls made before the commit)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """
    Executes the following commands when the database is connected.
    :param dbapi_connection:
    :param connection_record:
    :return:
    """
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")  # checks for foreign key constraints in SQLite
    cursor.execute("PRAGMA journal_mode=WAL")  # WriteAheadLogging; allows for tasks to happen instantly in the database
    cursor.close()
