"""Postgres helpers
Of course after you established a connection to the database, you can do
whatever you are capable of with SQL.
However, to spare some effort, I added these helpers to avoid repetition of
common tasks.
Hopefully, this makes integrating a database easier in the future.

Basic ER diagram:
(Visit [rivus_db](https://github.com/lnksz/rivus_db) or details)

+----------------------+
|         run          |
+----+-----------------+
| PK | run_id          |
|    | date            |
|    | runner          |
|    | status          |
|    | outcome         |
|    | pre_duration    |
|    | solve_duration  |
|    | post_duration   |
|    | plot            |
+----+-----------------+
"""

import psycopg2 as psql
from datetime import datetime

# from psycopg2 import sql

# cur.execute(
#     sql.SQL("insert into {} values (%s, %s)")
#         .format(sql.Identifier('my_table')),
#     [10, 20])


def _get_next_run_id(connection):
    cursor = connection.cursor()
    cursor.exexute("""
        SELECT
        """)
    return


def init_run(connection, runner='Havasi', start_ts=None, status='prepared',
             outcome='not_run', **kwargs):
    try:
        ts = datetime.strptime(start_ts, '%Y-%m-%d %H:%M:%S')
    except:
        ts = datetime.now()
    finally:
        start_ts = ts.strftime('%Y-%m-%d %H:%M:%S')

    run_id = None
    with connection as conn:
        with conn.cursor() as curs:
            curs.execute(
                """
                INSERT INTO run (runner, start_ts, status, outcome)
                VALUES (%s, TIMESTAMP %s, %s, %s)
                RETURNING run_id
                """, (runner, start_ts, status, outcome))
            run_id = curs.fetchone()[0]
    return run_id


def store(connection, run_data, prob, plot_data=None, graph=None):
    if 'run_id' in run_data:
        run_id = run_data['run_id']
    else:
        init_run(connection, **run_data)
    pass

if __name__ == '__main__':
    def tester(prob=None):
        connection = psql.connect(database='rivus', user="postgres")
        # cursor = connection.cursor()
        # cursor.execute("""
        #     SELECT relname FROM pg_class
        #     WHERE relkind='r' and relname !~ '^(pg_|sql_)';
        #     """)
        run_obj = {
            'runner': 'Havasi',
            'start_ts': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'prepared',
            'outcame': 'not_run',
        }
        run_id = init_run(connection, **run_obj)
        print(run_id)

        connection.close()

    tester()
