from sqlalchemy import create_engine, text
from testcontainers.mysql import MySqlContainer

with MySqlContainer("mysql:5.7.17") as mysql:
    engine = create_engine(mysql.get_connection_url())
    with engine.connect() as connection:
        result = connection.execute(text("SELECT VERSION()"))
        version = result.scalar()

print(version)
