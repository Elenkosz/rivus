##########
Reference
##########

You can get an overview of the purpose of the submodules from the :ref:`previous section <a_tutorial>`.
The (detailed) description of the functions all across rivus.

**************
Prerequisites
**************

We assume that you have a installed rivus (``git clone``) and the required packages
for your work. (``conda install`` see in :ref:`installation <a_install>`)

.. _a_datafromats:

**************
Data Formats
**************

How data is expected so that it will work.

.. _a_spreadsheet:

Spreadsheet
============


.. _a_vertex:

Vertex 
=======

.. _a_edge:

Edge 
=======



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

.. automodule:: rivus.graph.analysis
    :members:

.. automodule:: rivus.graph.to_graph
    :members:


rivus\.gridder
==============
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