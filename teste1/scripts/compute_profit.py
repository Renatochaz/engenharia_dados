"""Script to run raw sql with SQLAlchemy as ORM manager.

The results from the query are writted to the console
and a results.csv is sent to the docker-compose directory.

@author Renato Chavez
"""

import os
import logging
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text


class SQLRun():
    """Run raw sql queries with SQLAlchemy as ORM manager.

    Args:
        conn(dict): A `dictionary` object containing the following keys
            to instantiate a `Engine` object from the SQLalchemy package:
            "user", "pwd", "server", "port", "db".

    Attributes:
        logger(logging.logger): Custom `logger` object from
            the base python logging package.
        _engine_address(str): URL used by the SQLalchemy package to
            instantiate a `Engine` object.
    """

    def __init__(self, conn:dict) -> None:
        self._engine_address = (
            f"mssql+pymssql://{conn['user']}:{conn['pwd']}@"
            f"{conn['server']}:{conn['port']}/{conn['db']}"
            )

        self.logger = logging.getLogger(__name__)

        # Custom configuration to the logging object.
        logging.basicConfig(
            level=logging.INFO,
            format="%(levelname)s:%(message)s"
        )

    def run_sql(self, sql_file: str) -> None:
        """Executes a SQL query using the engine from SQLalchemy.

        The results are writted to the user console and a
        results.csv is generated to the user docker directory.

        Args:
            sql_file(str): PATH to the sql query to be executed.
        """

        engine = create_engine(self._engine_address)

        with open(sql_file, encoding="utf-8") as sql:
            query = text(sql.read())
            results = pd.read_sql_query(query, engine)

            self.logger.info(
                "%s result: \n %s \n",
                sql_file,
                results.to_string(index=False)
            )

            results.to_csv("results.csv", index=False)
            self.logger.info("Successfully generated results.csv")


if __name__ == '__main__':
    db_params = {
        "user":os.environ['USERNAME'],
        "pwd":os.environ['SA_PASSWORD'],
        "server": "localhost",
        "port":1433,
        "db":"desafio_engenheiro"
        }
    query_executor = SQLRun(conn=db_params)
    query_executor.run_sql('compute_profit.sql')
