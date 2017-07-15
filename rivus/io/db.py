"""Postgres helpers
Of course after you established a connection to the database, you can do
whatever you are capable of with SQL.
However, to spare some effort, I added these helpers to avoid repetition of
common tasks. Hopefully, this makes database integration easier in the future.

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
from pandas import DataFrame

# from psycopg2 import sql

# cur.execute(
#     sql.SQL("insert into {} values (%s, %s)")
#         .format(sql.Identifier('my_table')),
#     [10, 20])


def _get_insert(table, df):
    if 'edge' == table:
        # also include edge_demand TODO
        cols = ['run_id', 'edge_num', 'vertex1', 'vertex2', 'geometry']
    elif 'vertex' == table:
        # also include vertex_source TODO
        # ['vertex_id', 'commodity_id', 'value']
        cols = ['run_id', 'vertex_num', 'geometry']
    elif 'process' == table:
        cols = ['run_id', 'process', 'cost_inv_fix', 'cost_inv_var',
                'cost_fix', 'cost_var', 'cost_min', 'cost_max']
    elif 'commodity' == table:
        cols = ['run_id', 'commodity', 'unit', 'cost_inv_fix', 'cost_inv_var',
                'cost_fix', 'cost_var', 'loss_fix', 'loss_var', 'allowed_max']
    elif 'process_commodity' == table:
        cols = ['process_id', 'commodity_id', 'direction', 'ratio']
    elif 'time' == table:
        # time_demand
        # ['time_id', 'commodity_id', 'scale']
        cols = ['run_id', 'time_step', 'weight']
    elif 'area_demand' == table:
        # area
        # ['area_id', 'run_id', 'building_type']
        cols = ['area_id', 'commodity_id', 'peak']
    else:
        # Not implemented or non-existent table
        return None

    cols = ','.join(cols)
    vals = ','.join(['%s'] * len(cols))
    string_query = """
        INSERT INTO {0} ({1})
        VALUES ({2});
        """.format(table, cols, vals)
    return string_query


def init_run(engine, runner='Havasi', start_ts=None, status='prepared',
             outcome='not_run'):
    try:
        ts = datetime.strptime(start_ts, '%Y-%m-%d %H:%M:%S')
    except:
        ts = datetime.now()
    finally:
        start_ts = ts.strftime('%Y-%m-%d %H:%M:%S')

    run_id = None
    connection = engine.raw_connection()
    try:
        with connection.cursor() as curs:
            curs.execute(
                """
                INSERT INTO run (runner, start_ts, status, outcome)
                VALUES (%s, TIMESTAMP %s, %s, %s)
                RETURNING run_id;
                """, (runner, start_ts, status, outcome))
            run_id = curs.fetchone()[0]
    finally:
        connection.close()
    return run_id


def store(engine, prob, run_data=None, run_id=None, plot_data=None, graph=None):
    if run_id is not None:
        run_id = int(run_id)
    else:
        run_id = init_run(engine, **run_data) if run_data else init_run(engine)

    col_map = {
        'Edge': 'edge_num',
        'allowed-max': 'allowed_max',
        'cap-max': 'cap_max',
        'cap-min': 'cap_min',
        'cost-fix': 'cost_fix',
        'cost-inv-fix': 'cost_inv_fix',
        'cost-inv-var': 'cost_inv_var',
        'cost-var': 'cost_var',
        'loss-fix': 'loss_fix',
        'loss-var': 'loss_var',
    }

    # PARAMETERS
    # para_names = ['edge', 'vertex', 'process', 'hub', 'commodity',
    #               'process_commodity', 'time', 'area_demand']
    for para in prob.params:
        df = prob.params[para]
        print('para has <{}>'.format(para))
        if para is 'commodity':
            sql_df = df.rename(columns=col_map)
            sql_df['run_id'] = run_id
            sql_df.to_sql(para, engine, if_exists='append',
                          index_label=para)
        if para is 'process':
            sql_df = df.loc[:, 'cost-inv-fix':'cap-max'].rename(columns=col_map)
            sql_df['run_id'] = run_id
            sql_df.to_sql(para, engine, if_exists='append',
                          index_label=para)
        if para is 'edge':
            sql_df = df.loc[:, ('Edge', 'geometry')].rename(columns=col_map)
            sql_df['run_id'] = run_id
            sql_df.to_sql(para, engine, if_exists='append',
                          index_label=('vertex1', 'vertex2'))
        if para is 'vertex':
            sql_df = df.geometry.to_frame()
            sql_df['run_id'] = run_id
            sql_df.to_sql(para, engine, if_exists='append',
                          index_label='vertex_num')
        if para is 'area_demand':
            area_types = df.unstack(level='Commodity').index.values
            sql_df = DataFrame({
                'building_type': area_types,
                'run_id': [run_id] * len(area_types)
            })
            sql_df.to_sql('area', engine, if_exists='append', index=False)
            # TODO table `area_demand`
        if para is 'process_commodity':
            pass
        if para is 'time':
            sql_df = df.loc[:, 'weight']
            sql_df['run_id'] = run_id
            sql_df.to_sql(para, engine, if_exists='append',
                          index_label='time_step')
        # sql_str = _get_insert(para, prob.params[para])
        # with connection.cursor() as curs:
        #     curs.executemany(sql_str, )
    return

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
