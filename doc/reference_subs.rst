##########################
Reference - Sub-Packages
##########################

You can get an overview of the purpose of the sub-packages from the :ref:`previous section <a_tutorial>`.
The (detailed) description of all user-relevant functions in rivus are listed below. In addition to the documentation of the individual functions, a brief description is provided per sub-package or module to enlighten the used packages or design logic.

.. note::

    Prerequisites:
        In the code examples, we assume that you have a installed rivus (``git clone``) and the required packages for your work. (``conda install`` see in :ref:`installation <a_install>`)

.. _a_subpacks:


***********************
rivus\.main
***********************
rivus
----------------

The formulation of the :abbr:`MILP (mixed integer linear programming)` model is implemented
with the help of Pyomo_'s ConcreteModel_. That means, the needed constrains are formulated with the help of python functions. These have descriptive names following the ``*_rule`` or ``*_balance`` naming convention. In general, you do not have to touch them.

As for now, the object returned by :func:`create_model()` (often named as ``prob``) serves as the base type of input for the other function. This may change in future versions. But as for now, it is important you get familiar with its format. Following attributes are directly accessible and esp. interesting in the first round.

+ peak : (Pandas.DataFrame) - Maximum demands per edge.
+ r_in, r_out : (Pandas.Series) - Process-Commodity ratios split by direction.
+ params : (dict)
    
    - ``commodity`` - processed Excel sheet
    - ``process`` - processed Excel sheet
    - ``hub`` - filtered version of ``process``
    - ``process_commodity`` - processed Excel sheet
    - ``time`` - processed Excel sheet
    - ``area_demand`` - processed Excel sheet
    - ``vertex`` - processed spatial input
    - ``edge`` - processed spatial input

.. _Pyomo: http://www.pyomo.org/
.. _ConcreteModel: https://software.sandia.gov/downloads/pub/coopr/CooprGettingStarted.html#_a_simple_concrete_pyomo_model

.. warning::

    Following functions will be migrated to the ``io`` sub-package:

    + ``read_excel``
    + ``plot`` - ``result_figures``
    + ``save`` - ``load``
    + ``save_log``

    Following function will be migrated to ``rivus.main.getters``:

    + ``get_entity`` - ``get_entities`` - ``list_entities``
    + ``get_onset_names``
    + ``get_constants``
    + ``get_timeseries``

Modelling
^^^^^^^^^^

.. automodule:: rivus.main.rivus
    :members: create_model, line_length

IO
^^^
Following functions will be migrated to the ``io`` sub-package

.. automodule:: rivus.main.rivus
    :members: read_excel, plot, result_figures, report, save_log, save, load

Getters
^^^^^^^^
Following function will be migrated to ``rivus.main.getters``

.. automodule:: rivus.main.rivus
    :members: get_entity, get_entities, list_entities, get_onset_names, get_constants, get_timeseries

***********************
rivus\.graph
***********************

Comparison of the common graph analysis tools:

+ NetworkX_ (preferred):

    * `+ /-` Pure python implementation.
    * `+` Widely used and tested.
    * `+` Docs are quite good.
    * `+` Easy (platform independent) installation
    * `-` Slower than igraph (and graph-tools)

+ python-igraph_(fall-back):

    * `+` C based with python wrappers.
    * `+` Mature library package.
    * `+` Included for speed and so for scalability.
    * `×` Docs are OK.
    * `-` Windows install can be somewhat tedious (with unofficial wheel files). But it works.

+ graph-tools_: (eventually added in the future, if there is reeeaaly big need for efficiency..)

    * `+` Self proclaimed: fastest in graph analyses
    * `-` Not really windows user friendly (docker install should be tested)

These all facilitate pretty advanced graph theoretical analysis. Moreover, the file export functions of the used libraries were bridged through the ``to_graph`` module. Preferred file format is ``.gml`` which is supported by all common graph analysis tools. As such, specialized, stand-alone tools for graph visualisation and analysis can be used. E.g. Gephi_ with its exceptional geolayout_ plug-in can be of tremendous help for deeper graph visualization and analysis.

.. _Gephi: https://gephi.org/
.. _geolayout: https://gephi.wordpress.com/tag/geolayout/
.. _NetworkX: https://networkx.github.io/
.. _python-igraph: http://igraph.org/python/
.. _graph-tools: https://graph-tool.skewed.de/

to_graph
----------------
.. automodule:: rivus.graph.to_graph
    :members:

analysis
----------------
.. automodule:: rivus.graph.analysis
    :members:



***********************
rivus\.gridder
***********************

.. todo:: Grid

    Add gridder visualization

create_grid
----------------
.. automodule:: rivus.gridder.create_grid
    :members:

extend\_grid
----------------
.. automodule:: rivus.gridder.extend_grid
    :members:


***********************
rivus\.io 
***********************

rivus\.db
----------------

To advocate the possibilities provided by a good database connection, 
a throughout description of the set-up process is documented in rivus-db_.
There you can find help from the entry level (install, create database) to more
advanced topics (queries, data archive).

In this module presents a convenient way to interact with the your PostgreSQL database.

Store example
::

    from sqlalchemy import create_engine
    from rivus.io import db as rdb
    engine = create_engine('postgresql://postgres:pass@localhost/rivus')
    # ...
    # Modelling, Solving, Analysing
    # ...
    this_run = dict(comment='testing graph table and features with networx',
                profiler=profile_log)
    rdb.store(engine, rivus_model, run_data=run_dict)

Import example
::

    from sqlalchemy import create_engine
    from rivus.io import db as rdb
    from rivus.main.rivus import create_model
    engine = create_engine('postgresql://postgres:pass@localhost/rivus')
    run_id = 4242
    data_dfs = ['process', 'commodity', 'process_commodity', 'time', 'area_demand']
    data = {df_name: rdb.df_from_table(engine, df_name, run_id)
            for df_name in data_dfs}
    vertex = rdb.df_from_table(engine, 'vertex', run_id)
    edge = rdb.df_from_table(engine, 'edge', run_id)

    prob = create_model(data, vertex, edge, hub_only_in_edge=False)

.. _rivus-db: http://rivus-db.readthedocs.io

.. automodule:: rivus.io.db
    :members:

rivus\.plot
----------------
.. automodule:: rivus.io.plot
    :members:

***********************
rivus\.test
***********************

test\_db
----------------

.. automodule:: rivus.tests.test_db
    :members:

test\_gridder
----------------

.. automodule:: rivus.tests.test_gridder
    :members:

test\_main
----------------

.. automodule:: rivus.tests.test_main
    :members:

test\_utils
----------------

.. automodule:: rivus.tests.test_utils
    :members:

***********************
rivus\.utils
***********************

prerun
----------------

.. automodule:: rivus.utils.prerun
    :members:

notify
----------------

.. automodule:: rivus.utils.notify
    :members:

runmany
----------------

.. automodule:: rivus.utils.runmany
    :members:

pandashp
----------------

.. automodule:: rivus.utils.pandashp
    :members: