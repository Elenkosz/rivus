import os
import sys
from copy import deepcopy
from pandas import Series
from numpy import arange
from datetime import datetime
from time import time as timenow
from rivus.main import rivus
# =========================================================
# Constants - Inputs
import json
config = []
with open('./config.json') as conf:
    config = json.load(conf)
SOLVER = config['use_solver']
PLOTTER = config['make_plot']
STORE_DB = config['store_db']
GRAPHS = config['g_analysis']
SPANNER = config['calc_minimal']
RUN_BUNCH = config['run_bunch']
# ---- Solver = True to create and solve new problem
# ---- Solver = False to load an already solved model and investigate it
# =========================================================
if SOLVER or RUN_BUNCH:
    import pyomo.environ
    from pyomo.opt.base import SolverFactory
    from pyomo.opt import SolverStatus
    from pyomo.opt import TerminationCondition

    from rivus.utils.prerun import setup_solver
    from rivus.gridder.create_grid import create_square_grid
    from rivus.gridder.create_grid import get_source_candidates
    from rivus.gridder.extend_grid import extend_edge_data
    from rivus.gridder.extend_grid import vert_init_commodities
if PLOTTER or RUN_BUNCH:
    # import matplotlib.pyplot as plt
    from rivus.io.plot import fig3d
    from plotly.offline import plot as plot3d
if STORE_DB or RUN_BUNCH:
    # from datetime import datetime
    from sqlalchemy import create_engine
    from rivus.io import db as rdb
if GRAPHS or RUN_BUNCH:
    import networkx as nx
    # import igraph as pig
    from rivus.graph.to_graph import to_nx
    from rivus.graph.analysis import minimal_graph_anal
    from rivus.main.rivus import get_constants


def _geo_variations(create_params):
    pass


def _source_variations(vertex, dim_x, dim_y):
    """Generate vertex dataframe variations with difference locations for the
    source vertices.
    Todo?: Here maybe also extend_edge_data()?

    Parameters
    ----------
    vertex : DataFrame
        Typical vertex dataframe, as returned by create_square_grid()
    dim_x : int
        Number of vertices alongside the x-axis
    dim_y : int
        Number of vertices alongside the y-axis

    Yields
    ------
    Dataframe
        Ready to be fead into the create_model() function as parameter.
    """

    # max commodity capacity, the source can generate
    MAX_ELEC = 160000
    MAX_GAS = 500000

    src_inds = get_source_candidates(vertex, dim_x, dim_y, logic='sym')
    source_setups = [[('Elec', S, MAX_ELEC), ('Gas', S, MAX_GAS)]
                     for S in src_inds]
    flip = src_inds.copy()
    flip.reverse()
    src_pairs_opposite = zip(src_inds, flip)
    for E, G in src_pairs_opposite:
        this_srcs = [('Elec', E, MAX_ELEC), ('Gas', G, MAX_GAS)]
        if this_srcs not in source_setups:
            source_setups.append(this_srcs)

    src_corners = get_source_candidates(vertex, dim_x, dim_y, logic='extrema')
    for E, G in src_corners:
        this_srcs = [('Elec', E, MAX_ELEC), ('Gas', G, MAX_GAS)]
        if this_srcs not in source_setups:
            source_setups.append(this_srcs)

    for sources in source_setups:
        print('\nCurrent sources: \n{}'.format(sources))
        variant = vert_init_commodities(vertex, ('Elec', 'Gas', 'Heat'),
                                        sources=sources, inplace=False)
        yield variant


def _parameter_range(data_df, index, column, lim_lo=None, lim_up=None,
                     step=None):
    """Yield values of the parameter in a given range
    Parameters
    ----------
    xls: dict of DataFrames
        As returned from rivus.main.read_excel
    data_df : str
        To select DataFrame from xls
    index : valid pandas DataFrame row label
        DataFrame .loc parameter to locate the parameter value.
        E.g.: ['Gas power plant', 'CO2', 'Out'] or 'Gas'
    column : str
        Label of the column, where the parameter is.
        E.g.: 'ratio' or 'cap-max'
    lim_lo : None, optional
        Proportional parameter. If omitted, 90% of the original.
    lim_up : None, optional
        Proportional parameter. If omitted 110% of the original.
    step : None, optional
        Proportional parameter. The difference between
        two following yielded values.

    Returns
    -------
    DataFrame
        A modified version of xls[df_name]
    """
    df = data_df  # Naming
    is_multi = len(df.index.names) > 1
    if is_multi:
        original = df.loc[tuple(index)][column]
    else:
        original = df.loc[index][column]
    LO_PROP = 0.9
    UP_PROP = 1.1
    STEP_PROP = 0.05
    lim_lo = LO_PROP * original if lim_lo is None else lim_lo * original
    lim_up = UP_PROP * original if lim_up is None else lim_up * original
    step = STEP_PROP * original if step is None else step * original
    if step == 0:
        step = None
    print('\n> Parameter {} was: {} now changing from {} to {} by {}'.
          format(column, original, lim_lo, lim_up, step))
    for mod in arange(lim_lo, lim_up, step):
        if is_multi:
            df.loc[tuple(index)][column] = mod
        else:
            df.loc[index, column] = mod
        yield df


def run_bunch(use_email=False):
    """Run a bunch of optimizations and analysis automated. """
    # Files Access | INITs
    proj_name = 'runbunch'
    base_directory = os.path.join('data', proj_name)
    data_spreadsheet = os.path.join(base_directory, 'data.xlsx')
    profile_log = Series(name='{}-profiler'.format(proj_name))

    # DB connection
    _user = config['db']['user']
    _pass = config['db']['pass']
    _host = config['db']['host']
    _base = config['db']['base']
    engine_string = ('postgresql://{}:{}@{}/{}'
                     .format(_user, _pass, _host, _base))
    engine = create_engine(engine_string)

    if use_email:
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText

        robo_user = config['email']['s_user']
        robo_pass = config['email']['s_pass']
        recipient = config['email']['r_user']
        smtp_addr = config['email']['smtp_addr']
        smtp_port = config['email']['smtp_port']

        smtp_msg = MIMEMultipart()
        smtp_msg['From'] = robo_user
        smtp_msg['To'] = recipient
        smtp_msg['Subject'] = 'Run status update [rivus][simius]'

        mailServer = smtplib.SMTP(smtp_addr, smtp_port)
        try:
            mailServer.ehlo()
            mailServer.starttls()
            mailServer.ehlo()
            mailServer.login(robo_user, robo_pass)
        except Exception as email_error:
            print(email_error)

    # Input Data
    # ----------
    # Spatial
    street_lengths = arange(50, 300, 25)
    num_edge_xs = list(range(5, 6))
    # Non-spatial
    data = rivus.read_excel(data_spreadsheet)
    original_data = deepcopy(data)
    interesting_parameters = [
        {'df_name': 'commodity',
         'args': {'index': 'Heat',
                  'column': 'cost-inv-fix',
                  'lim_lo': 0.5, 'lim_up': 1.5, 'step': 0.25}},
        # {'df_name': 'commodity',
        #  'args': {'index': 'Elec',
        #           'column': 'cost-var',
        #           'step': 0.1}}
    ]
    # Model Creation
    solver = SolverFactory(config['solver'])
    solver = setup_solver(solver, log_to_console=False)
    # Solve | Analyze | Store | Change | Repeat
    for dx in street_lengths:
        for len_x, len_y in [(dx, dx), (dx, dx / 2)]:
            for num_edge_x in num_edge_xs:
                vdf, edf = create_square_grid(num_edge_x=num_edge_x, dx=len_x,
                                              dy=len_y)
                extend_edge_data(edf)
                dim_x = num_edge_x + 1
                dim_y = dim_x
                for _vdf in _source_variations(vdf, dim_x, dim_y):
                    for param in interesting_parameters:
                        counter = 1
                        for variant in _parameter_range(data[param['df_name']],
                                                        **param['args']):
                            print('{0}\n\t{1}x{1} grid - variant <{2}>\n{0}'
                                  .format('=' * 10, num_edge_x, counter))
                            counter = counter + 1
                            data[param['df_name']] = variant
                            __vdf = deepcopy(_vdf)
                            __edf = deepcopy(edf)
                            _p_model = timenow()
                            prob = rivus.create_model(data, __vdf, __edf)
                            profile_log['model_creation'] = (timenow() -
                                                             _p_model)
                            _p_solve = timenow()
                            try:
                                results = solver.solve(prob, tee=True)
                            except Exception as solve_error:
                                print(solve_error)
                                if use_email:
                                    message = repr(solve_error)
                                    smtp_msg.attach(MIMEText(message))
                                    mailServer.sendmail(robo_user, recipient,
                                                        smtp_msg.as_string())

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
                            profile_log['solve'] = (timenow() - _p_solve)
                            # Plot
                            _p_plot = timenow()
                            plotcomms = ['Gas', 'Heat', 'Elec']
                            fig = fig3d(prob, plotcomms, linescale=8,
                                        use_hubs=True)
                            profile_log['3d_plot_prep'] = (timenow() - _p_plot)
                            # Graph
                            _p_graph = timenow()
                            _, pmax, _, _ = get_constants(prob)
                            graphs = to_nx(_vdf, edf, pmax)
                            graph_results = minimal_graph_anal(graphs)
                            profile_log['all_graph_related'] = (timenow() -
                                                                _p_graph)

                            # Store
                            this_run = {
                                'comment': config['run_comment'],
                                'status': status,
                                'outcome': outcome,
                                'runner': 'lnksz',
                                'plot_dict': fig,
                                'profiler': profile_log}
                            rdb.store(engine, prob, run_data=this_run,
                                      graph_results=graph_results)
                            del __vdf
                            del __edf
                            print('\tRun ended with: <{}>\n'.format(outcome))
                        data = original_data
                if use_email:
                    status_txt = ('Finished iteration with edge number {}\n'
                                  'did: [source-var, param-seek]'
                                  .format(num_edge_x))
                    smtp_msg.attach(MIMEText(status_txt))
                    mailServer.sendmail(robo_user, recipient,
                                        smtp_msg.as_string())
        if use_email:
            status_txt = ('Finished iteration with street lengths {}-{}\n'
                          'did: [dim-shift, source-var, param-seek]'
                          .format(len_x, len_y))
            smtp_msg.attach(MIMEText(status_txt))
            mailServer.sendmail(robo_user, recipient, smtp_msg.as_string())

    if use_email:
        status_txt = ('Finished run-bunch at {}\n'
                      'did: [street-length, dim-shift, source-var, param-seek]'
                      .format(timenow()))
        smtp_msg.attach(MIMEText(status_txt))
        mailServer.sendmail(robo_user, recipient, smtp_msg.as_string())
        mailServer.close()


if RUN_BUNCH:
    run_bunch(use_email=True)
    sys.exit()


# loosly structered run parts
lat, lon = [48.13512, 11.58198]  # You can copy LatLon into this list
proj_name = 'chessboard'
datenow = datetime.now().strftime('%y%m%dT%H%M')
result_dir = os.path.join('result', '{}-{}'.format(proj_name, datenow))
profile_log = Series(name='runchess-profiler')

if SOLVER:
    base_directory = os.path.join('data', proj_name)
    data_spreadsheet = os.path.join(base_directory, 'data.xlsx')
    # Create Rivus Inputs
    creategrid = timenow()
    vertex, edge = create_square_grid(origo_latlon=(lat, lon), num_edge_x=3,
                                      dx=1000)
    profile_log['grid_creation'] = round(timenow() - creategrid, 2)

    extendgrid = timenow()
    extend_edge_data(edge)  # only residential, with 1000 kW init
    vert_init_commodities(vertex, ('Elec', 'Gas', 'Heat'),
                          [('Elec', 0, 100000), ('Gas', 0, 5000)])
    profile_log['grid_data'] = timenow() - extendgrid
    # ---- load spreadsheet data
    excelread = timenow()
    data = rivus.read_excel(data_spreadsheet)
    profile_log['excel_read'] = timenow() - excelread

    # Create and solve model
    rivusmain = timenow()
    prob = rivus.create_model(data, vertex, edge)
    profile_log['rivus_main'] = timenow() - rivusmain

    solver = SolverFactory(config['solver'])
    solver = setup_solver(solver)
    startsolver = timenow()
    result = solver.solve(prob, tee=True)
    profile_log['solver'] = timenow() - startsolver

    # Handling results
    # ---- create result directory if not existing already
    # if not os.path.exists(result_dir):
    #     os.makedirs(result_dir)

    # print('Saving pickle...')
    # rivuspickle = timenow()
    # rivus.save(prob, os.path.join(result_dir, 'prob.pgz'))
    # profile_log['save_data'] = timenow() - rivuspickle
    # print('Pickle saved')
    # rivusreport = timenow()
    # rivus.report(prob, os.path.join(result_dir, 'report.xlsx'))
    # profile_log['rivus_report'] = timenow() - rivusreport
else:
    print('Loading pickled modell...')
    arch_dir = os.path.join('result', 'chessboard_light')
    arch_path = os.path.join(arch_dir, 'prob.pgz')
    rivusload = timenow()
    prob = rivus.load(arch_path)
    profile_log['rivus_load'] = timenow() - rivusload
    print('Loaded.')

# Plotting
# rivus.result_figures(prob, os.path.join(result_dir, 'figs/'))
if PLOTTER:
    print("Plotting...")
    myprintstart = timenow()
    plotcomms = ['Gas', 'Heat', 'Elec']
    fig = fig3d(prob, plotcomms, linescale=8, usehubs=True)
    if SOLVER:
        plot3d(fig, filename=os.path.join(result_dir, 'rivus_result.html'))
    else:
        plot3d(fig, filename=os.path.join(arch_dir, 'rivus_result.html'))
    profile_log['plotting'] = timenow() - myprintstart

if GRAPHS:
    print('Graph handling.')
    graph_prep = timenow()
    _, pmax, _, _ = get_constants(prob)
    graphs = to_nx(prob.params['vertex'], prob.params['edge'], pmax)
    profile_log['graph_prep'] = timenow() - graph_prep

    graph_anal_sum = timenow()
    graph_data = []
    for G in graphs:
        print('Analysing <{}> graph'.format(G.graph['Commodity']))
        g_data = {
            'commodity': G.graph['Commodity'],
            'is_connected': nx.is_connected(G),
            'connected_components': nx.number_connected_components(G)}
        if SPANNER:
            spanner = nx.minimum_spanning_tree(G)
            g_data['is_minimal'] = nx.is_isomorphic(G, spanner)
        graph_data.append(g_data)
    profile_log['graph_anal_sum'] = timenow() - graph_anal_sum

if STORE_DB:
    print('Using DB')
    dbstart = timenow()

    _user = config['db']['user']
    _pass = config['db']['pass']
    _host = config['db']['host']
    _base = config['db']['base']
    engine_string = ('postgresql://{}:{}@{}/{}'
                     .format(_user, _pass, _host, _base))
    engine = create_engine(engine_string)
    this_run = dict(comment='testing graph table and features with networx',
                    profiler=profile_log)
    if GRAPHS:
        rdb.store(engine, prob, run_data=this_run, graph_results=graph_data)
    else:
        rdb.store(engine, prob, run_data=this_run)
    # fetched_df = rdb.df_from_table(engine, 'time', 2)
    # print('Fetched table:\n', fetched_df)

    profile_log['db'] = timenow() - dbstart

    # import pandas as pd
    # with pd.ExcelWriter('./fetched.xlsx') as writer:
    #     fetched_df.to_excel(writer, 'edge')


print('{1} Script parts took: (sec) {1}\n{0:s}\n{1}{1}{1}{1}'.format(
      profile_log.to_string(), '=' * 6))
