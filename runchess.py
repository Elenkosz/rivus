import os
from pandas import Series
from datetime import datetime
from time import time as timenow
from rivus.main import rivus
# =========================================================
# Constants - Inputs
lat, lon = [48.13512, 11.58198]  # You can copy LatLon into this list
import json
config = []
with open('./config.json') as conf:
    config = json.load(conf)
SOLVER = config['use_solver']
PLOTTER = config['make_plot']
STORE_DB = config['store_db']
GRAPHS = config['g_analysis']
SPANNER = config['calc_minimal']
# ---- Solver = True to create and solve new problem
# ---- Solver = False to load an already solved model and investigate it
# =========================================================
if SOLVER:
    import pyomo.environ
    from pyomo.opt.base import SolverFactory
    from pyomo.opt import SolverStatus
    from pyomo.opt import TerminationCondition

    from rivus.utils.prerun import setup_solver
    from rivus.gridder.create_grid import create_square_grid
    from rivus.gridder.extend_grid import extend_edge_data
    from rivus.gridder.extend_grid import vert_init_commodities
if PLOTTER:
    # import matplotlib.pyplot as plt
    from rivus.io.plot import fig3d
    from plotly.offline import plot as plot3d
if STORE_DB:
    # from datetime import datetime
    from sqlalchemy import create_engine
    from rivus.io import db as rdb
if GRAPHS:
    import networkx as nx
    # import igraph as pig
    from rivus.graph.to_graph import to_nx
    from rivus.graph.analysis import minimal_graph_anal
    from rivus.main.rivus import get_constants


# Files Access | INITs
datenow = datetime.now().strftime('%y%m%dT%H%M')
proj_name = 'chessboard'
base_directory = os.path.join('data', proj_name)
data_spreadsheet = os.path.join(base_directory, 'data.xlsx')
result_dir = os.path.join('result', '{}-{}'.format(proj_name, datenow))
prob_dir = os.path.join('result', proj_name)
profile_log = Series(name='minimal-profiler')


def _source_variations(vertex, num_row, nom_col):
    pass
    # should be a generator (yield to spare memory)
    # generate vertex  dataframe variations for source points.
    # src_set = calc_destination space()
    # for src in src_set:
    #   vert_init_commodities()
    # Here maybe extend_edge_data()?


def _parameter_slider(non_spatial_df, param_id, modifier):
    """Modify a parameter of a non spatial dataframe from the Excel input.
    Use modifier to calculate the new value.
    """
    pass


def _parameter_range(xls, df, locator, min=None, max=None):
    """Yield values of the parameter in a given range
    original
    for x in xs:
        yield original-changed

    Will it return original?
    Parameters
    ----------
    df : TYPE
        Description
    locator : TYPE
        Description
    min : None, optional
        If omitted, 90% of the original.
    max : None, optional
        If omited 110% of the original.
    """
    pass


def run_bunch():
    """Run a bunch of optimizations and analysis automated.
    """
    # DB connection
    _user = config['db']['user']
    _pass = config['db']['pass']
    _host = config['db']['host']
    _base = config['db']['base']
    engine_string = ('postgresql://{}:{}@{}/{}'
                     .format(_user, _pass, _host, _base))
    engine = create_engine(engine_string)

    # Input Data
    data = rivus.read_excel(data_spreadsheet)
    vdf, edf = create_square_grid(num_edge_x=3, dx=1000)
    interesting_parameters = [
        {'df': 'commodity',
         'locator': ('Elec', 'cost-fix'),
         'min': None, 'max': None},
        {'df': 'process',
         'locator': ('Elec heating domestic', 'cost-inv-var')},
        {'df': 'process_commodity',
         'locator': (['Heat pump domestic',  'Heat', 'Out'], 'ratio')},
    ]
    # Model Creation
    solver = SolverFactory(config['solver'])
    solver = setup_solver(solver)
    # Solve | Analyze | Store | Change | Repeat
    for _vdf in _source_variations(vdf):
        for param in interesting_parameters:
            for variant in _parameter_range(data, **param):
                prob = rivus.create_model(variant, _vdf, edf)
                results = solver.solve(prob, tee=True)
                if (results.solver.status != SolverStatus.ok):
                    status = 'error'
                    outcome = 'error'
                else:
                    status = 'run'
                    if (results.solver.termination_condition !=
                            TerminationCondition.optimal):
                        outcome = 'optimum_not_reached'
                    else:
                        outcome = 'optimum'
                # Plot
                plotcomms = ['Gas', 'Heat', 'Elec']
                fig = fig3d(prob, plotcomms, linescale=8, usehubs=True)

                # Graph
                _, pmax, _, _ = get_constants(prob)
                graphs = to_nx(variant, edf, pmax)
                graph_results = minimal_graph_anal(graphs)

                # Store
                this_run = {
                    'status': status,
                    'outcome': outcome,
                    'runner': 'lnksz',
                    'plot': fig}
                rdb.store(engine, prob, run_data=this_run,
                          graph_results=graph_results)

# if SOLVER:
#     # Create Rivus Inputs
#     creategrid = timenow()
#     vertex, edge = create_square_grid(origo_latlon=(lat, lon), num_edge_x=3,
#                                       dx=1000)
#     profile_log['grid_creation'] = round(timenow() - creategrid, 2)

#     extendgrid = timenow()
#     extend_edge_data(edge)  # only residential, with 1000 kW init
#     vert_init_commodities(vertex, ('Elec', 'Gas', 'Heat'),
#                           [('Elec', 0, 100000), ('Gas', 0, 5000)])
#     profile_log['grid_data'] = timenow() - extendgrid
#     # ---- load spreadsheet data
#     excelread = timenow()
#     data = rivus.read_excel(data_spreadsheet)
#     profile_log['excel_read'] = timenow() - excelread

#     # Create and solve model
#     rivusmain = timenow()
#     prob = rivus.create_model(data, vertex, edge)
#     profile_log['rivus_main'] = timenow() - rivusmain

#     solver = SolverFactory(config['solver'])
#     solver = setup_solver(solver)
#     startsolver = timenow()
#     result = solver.solve(prob, tee=True)
#     profile_log['solver'] = timenow() - startsolver

#     # Handling results
#     # ---- create result directory if not existing already
#     # if not os.path.exists(result_dir):
#     #     os.makedirs(result_dir)

#     # print('Saving pickle...')
#     # rivuspickle = timenow()
#     # rivus.save(prob, os.path.join(result_dir, 'prob.pgz'))
#     # profile_log['save_data'] = timenow() - rivuspickle
#     # print('Pickle saved')
#     # rivusreport = timenow()
#     # rivus.report(prob, os.path.join(result_dir, 'report.xlsx'))
#     # profile_log['rivus_report'] = timenow() - rivusreport
# else:
#     print('Loading pickled modell...')
#     arch_dir = os.path.join('result', 'chessboard_light')
#     arch_path = os.path.join(arch_dir, 'prob.pgz')
#     rivusload = timenow()
#     prob = rivus.load(arch_path)
#     profile_log['rivus_load'] = timenow() - rivusload
#     print('Loaded.')

# # Plotting
# # rivus.result_figures(prob, os.path.join(result_dir, 'figs/'))
# if PLOTTER:
#     print("Plotting...")
#     myprintstart = timenow()
#     plotcomms = ['Gas', 'Heat', 'Elec']
#     fig = fig3d(prob, plotcomms, linescale=8, usehubs=True)
#     if SOLVER:
#         plot3d(fig, filename=os.path.join(result_dir, 'rivus_result.html'))
#     else:
#         plot3d(fig, filename=os.path.join(arch_dir, 'rivus_result.html'))
#     profile_log['plotting'] = timenow() - myprintstart

# if GRAPHS:
#     print('Graph handling.')
#     graph_prep = timenow()
#     _, pmax, _, _ = get_constants(prob)
#     graphs = to_nx(prob.params['vertex'], prob.params['edge'], pmax)
#     profile_log['graph_prep'] = timenow() - graph_prep

#     graph_anal_sum = timenow()
#     graph_data = []
#     for G in graphs:
#         print('Analysing <{}> graph'.format(G.graph['Commodity']))
#         g_data = {
#             'commodity': G.graph['Commodity'],
#             'is_connected': nx.is_connected(G),
#             'connected_components': nx.number_connected_components(G)}
#         if SPANNER:
#             spanner = nx.minimum_spanning_tree(G)
#             g_data['is_minimal'] = nx.is_isomorphic(G, spanner)
#         graph_data.append(g_data)
#     profile_log['graph_anal_sum'] = timenow() - graph_anal_sum

# if STORE_DB:
#     print('Using DB')
#     dbstart = timenow()

#     _user = config['db']['user']
#     _pass = config['db']['pass']
#     _host = config['db']['host']
#     _base = config['db']['base']
#     engine_string = ('postgresql://{}:{}@{}/{}'
#                      .format(_user, _pass, _host, _base))
#     engine = create_engine(engine_string)
#     this_run = dict(comment='testing graph table and features with networx',
#                     profiler=profile_log)
#     if GRAPHS:
#         rdb.store(engine, prob, run_data=this_run, graph_results=graph_data)
#     else:
#         rdb.store(engine, prob, run_data=this_run)
#     # fetched_df = rdb.df_from_table(engine, 'time', 2)
#     # print('Fetched table:\n', fetched_df)

#     profile_log['db'] = timenow() - dbstart

#     # import pandas as pd
#     # with pd.ExcelWriter('./fetched.xlsx') as writer:
#     #     fetched_df.to_excel(writer, 'edge')


# print('{1} Script parts took: (sec) {1}\n{0:s}\n{1}{1}{1}{1}'.format(
#       profile_log.to_string(), '=' * 6))
