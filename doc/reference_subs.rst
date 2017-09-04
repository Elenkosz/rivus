##########################
Reference - Sub-Packages
##########################

You can get an overview of the purpose of the submodules from the :ref:`previous section <a_tutorial>`.
The (detailed) description of the functions all across rivus.

**************
Prerequisites
**************

In the code examples, we assume that you have a installed rivus (``git clone``) and the required packages for your work. (``conda install`` see in :ref:`installation <a_install>`)


.. _a_subpacks:

**************
Sub-packages
**************

rivus\.main
===================
rivus
-----

.. automodule:: rivus.main.rivus
    :members: read_excel, create_model, get_constants, get_timeseries, plot, result_figures, report, save_log, save, load



rivus\.graph
============

Comparison of the common graph analysis tools:

+ NetworkX_:

    * `+ /-` Pure python implementation.
    * `+` Widely used and tested.
    * `+` Docs are quite good.
    * `+` Easy (platform independent) installation
    * `-` Slower than igraph (and graph-tools)

+ python-igraph_:

    * `+` C based with python wrappers.
    * `+` Mature library package.
    * `+` Included for speed and so for scalability.
    * `×` Docs are OK.
    * `-` Windows install can be somewhat tedious (with unofficial wheel files). But it works.

+ graph-tools_: (maybe added in the future)

    * `+` Self proclaimed: fastest in graph analyses
    * `-` Not really windows user friendly (docker install should be tested)

.. _NetworkX: https://networkx.github.io/
.. _python-igraph: http://igraph.org/python/
.. _graph-tools: https://graph-tool.skewed.de/

to_graph
---------
.. automodule:: rivus.graph.to_graph
    :members:

analysis
--------
.. automodule:: rivus.graph.analysis
    :members:



rivus\.gridder
===============

.. todo:: Grid

    Add gridder visualization

create_grid
------------
.. automodule:: rivus.gridder.create_grid
    :members:

extend\_grid
------------
.. automodule:: rivus.gridder.extend_grid
    :members:


rivus\.io 
==========

rivus\.db
---------

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
------------
.. automodule:: rivus.io.plot
    :members:

rivus\.test
============

test\_db
----------

.. automodule:: rivus.tests.test_db
    :members:

test\_gridder
--------------

.. automodule:: rivus.tests.test_gridder
    :members:

test\_main
-----------

.. automodule:: rivus.tests.test_main
    :members:

test\_utils
------------

.. automodule:: rivus.tests.test_utils
    :members:

rivus\.utils
=============

prerun
--------

.. automodule:: rivus.utils.prerun
    :members:

notify
-------

.. automodule:: rivus.utils.notify
    :members:

runmany
--------

.. automodule:: rivus.utils.runmany
    :members:

pandashp
---------

.. automodule:: rivus.utils.pandashp
    :members: