##########
Reference
##########

You can get an overview of the purpose of the submodules from the :ref:`previous section <a_tutorial>`.
The (detailed) description of the functions all across rivus.

**************
Prerequisites
**************

We assume that you have a installed rivus (``git clone``) and the required packages
for your work. (``conda install`` in see :ref:`installation <a_install>`)

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

.. _a_main:

rivus.main
===================
Core functions to be able to create and solve the optimization problem.

rivus
-----

.. py:module:: rivus.main.rivus

.. function:: read_excel(filepath)
    
    Reads an Excel spreadsheet that adheres to the structure shown in the
    example dataset data/mnl/mnl.xlsx. Must contain

    Args:
        filepath: file path to an Excel spreadsheet.

    Returns:
        a dict of 5 DataFrames, one for each sheet

    .. note::

        This function will be moved into ``rivus.io`` in the next version.

.. function:: create_model(data, vertex, edge, peak_multiplier=None)

    Return a rivus model instance from input file and spatial input.

    Args:
        spreadsheet: Excel spreadsheet with entity sheets Commodity, Process,
            Process-Commodity, Time and Area-Demand
        vertex: GeoDataFrame with vertex IDs as column 'Vertex' and other columns
            named like source commodities (e.g. 'Gas', 'Elec', 'Pellets'),
            containing source vertex capacities (in kW)
        edge: GeoDataFrame woth vertex IDs in columns 'Vertex1' and 'Vertex2' and
            other columns named like area types (in spreadsheet/Area-Demand),
            containing total areas (square metres) to be supplied
        peak_multiplier: callable, optional
            If not None, will be called with the model as single argument

    Returns:
        Pyomo ConcreteModel object

.. function:: get_constants(prob)

    Retrieve time-independent variables/quantities.

    Usage:
        costs, pmax, kappa_hub, kappa_process = get_constants(prob)

    Args:
        prob: a rivus model instance

    Returns:
        (costs, pmax, kappa_hub, kappa_process) tuple
    
.. function:: get_timeseries(prob)

    Retrieve time-dependent variables/quantities.

    Usage:
        source, flows, hubs, proc_io, proc_tau = get_timeseries(prob)

    Args:
        prob: a rivus model instance

    Returns:
        (source, flows, hubs, proc_io, proc_tau) tuple
    
.. function:: plot(prob, commodity, plot_demand=False, mapscale=False, tick_labels=True,
         annotations=True, buildings=None, shapefiles=None, decoration=True, boundary=False)

    Plot a map of supply, conversion, transport and consumption.

    For given commodity, plot a map of all locations where the commodity is
    introduced (Rho), transported (Pin/Pot/Pmax), converted (Epsilon_*) and
    consumed (Sigma, peak).

    Args:
        prob:
        commodity:
        plot_demand: If True, plot demand, else plot capacities
        mapscale: If True, add mapscale to plot (default: False)
        tick_labels: If True, add lon/lat tick labels (default: True)
        annotations: If True, add numeric labels to graph (default: True)
        buildings: tuple of (filename to shapefile, boolean)
                   if true, color buildings according to attribute column
                   "type" and colors in constan rivus.COLORS; else use default
                   COLOR['building'] for all
        shapefiles: list of dicts of shapefiles that shall be drawn by
                    basemap function readshapefile. is passed as **kwargs
        decoration: Switch for map decoration (meridian, parallels)
    Returns:
        fig: the map figure object
    

.. function:: result_figures(prob, file_basename, buildings=None, shapefiles=None)

    Call rivus.plot with hard-coded combinations of plot_type and commodity.

    This is a convenience wrapper to shorten scripts.
    TODO: Generalise so that no hard-coding of commodity names is needed.

    Args:
        prob: a rivus model instance
        file_basename: filename prefix for figures
        buildings: optional filename to buildings shapefile
        shapefiles: list of dicts of shapefiles that shall be drawn by
                    basemap function readshapefile. is passed as **kwargs
    Returns:
        Nothing
    
.. function:: report(prob, filepath)

    Write result summary to a spreadsheet file.

    Create a concise result spreadsheet with values of all key variables,
    inclduing costs, pipe capacities, process and hub capacities, source flows,
    and process input/output/throughput per time step.

    Args:
        prob: a rivus model instance
        filepath: relative or absolute filepath of the Excel spreadsheet to be crated.
            It will be overwrite a file with the same path if such exists.

    Returns:
        Nothing
    
    
.. function:: save(prob, filepath)

    Save rivus model instance to a gzip'ed pickle file

    `Pickle <https://docs.python.org/2/library/pickle.html>`_ is the standard Python way of serializing and de-serializing Python
    objects. By using it, saving any object, in case of this function a
    Pyomo ConcreteModel, becomes a twoliner.
    
    `GZip <https://docs.python.org/2/library/gzip.html>`_ is a standard Python compression library that is used to transparently
    compress the pickle file further.

    Args:
        prob:
            a rivus model instance
        filepath:
            relative or abolute name of the file to be written

    Returns:
        Nothing

    .. todo::

        Change to HDF5 data fromat.

    .. note::

        Function will be magrated into ``rivus.io``.
    
.. function:: load(filepath)

    Load a rivus model instance from a gzip'ed pickle file

    Args:
        filepath: string, path to an archived pickle file

    Returns:
        prob: the unpickled rivus model instance

    .. todo::

        Change to HDF5 data fromat.

    .. note::

        Function will be magrated into ``rivus.io``.

.. function:: line_length(line)

    Calculate length of a line in meters, given in geographic coordinates.

    Args:
        line: a shapely LineString object with WGS 84 coordinates

    Returns:
        Length of line in meters

.. function:: pairs(iterable):
    
    Iterate over a list in overlapping pairs without wrap-around.

    Args:
        iterable: an iterable/list

    Returns:
        Yields a pair of consecutive elements (lst[k], lst[k+1]) of lst. Last
        call yields the last two elements.

    Example:
        lst = [4, 7, 11, 2]
        pairs(lst) yields (4, 7), (7, 11), (11, 2)

.. _a_utils:

rivus.utils
===================
notify
------

.. py:module:: rivus.utils.notify

.. function:: email_me(message, sender, send_pass, recipient, smtp_addr, smtp_port,
             subject='[rivus][notification]')

    Send notification message through email server.
    
    Args:
        message (str): Body of the e-mail
        sender (str): The e-mail account through which the email will be sent.
            E.g. tum.robot@gmail.com
        send_pass (str): Password of sender. Hopefully read from a file,
            which is not added to Git...
        recipient (str): The e-mail account of you, where you want to get the notification.
        smtp_addr (str): SMTP Address. Like "smtp.gmail.com"
        smtp_port (int): SMTP Port. Like 587
        subject (str, optional): The subject of the mail...
    
    Returns:
        integer: 0  - if run through without exception
            -1 - if encountered with a problem (mainly for unittest)

.. function:: test()

    Send notification message through email server.

    Parameters
    ----------
    message : str
        Body of the e-mail
    sender : str
        The e-mail account through which the email will be sent.
        E.g. tum.robot@gmail.com
    send_pass : str
        Password of sender. Hopefully read from a file,
        which is not added to Git...
    recipient : str
        The e-mail account of you, where you want to get the notification.
    smtp_addr : str
        SMTP Address. Like "smtp.gmail.com"
    smtp_port : int
        SMTP Port. Like 587
    subject : str, optional
        The subject of the mail...

    Returns
    -------
    integer
        0  - if run through without exception
        -1 - if encountered with a problem (mainly for unittest)



pandashp
---------

.. py:module:: rivus.utils.pandashp



runmany
--------

.. py:module:: rivus.utils.runmany



prerun
-------

.. py:module:: rivus.utils.prerun



shapelytools
-------------

.. py:module:: rivus.utils.shapelytools




.. _a_io:

rivus.io
===================

plot
-----

.. py:module:: rivus.io.plot

.. function:: fig3d(prob:ConcreteModel)

  Interactive viszalization.


db
-----

.. py:module:: rivus.io.db


.. todo::
  reference rivus.io

.. _a_graph:

rivus.graph
===================

to_graph
---------
.. py:module:: rivus.graph.to_graph

analysis
---------
.. py:module:: rivus.graph.analysis


.. _a_gridder:

rivus.gridder
===================

create_grid
------------

Create basic geometrical structure from origo and parameters.

.. py:module:: rivus.graph.create_grid


extend_grid
------------

.. py:module:: rivus.graph.extend_grid



.. _a_tests:

rivus.tests
===================


.. py:module:: rivus.main.rivus

.. automodule:: rivus.main.rivus

Short description of test logic.

test_main
----------

.. py:module:: rivus.tests.test_main



test_utils
-----------

.. py:module:: rivus.tests.test_utils



test_gridder
-------------

.. py:module:: rivus.tests.test_gridder



test_db
--------

.. py:module:: rivus.tests.test_db



.. todo::
  reference rivus.tests

.. _a_converter:

rivus.converter
===================

building_to_edge
------------------

.. py:module:: rivus.converter.building_to_edge


streets_to_edge
----------------

.. py:module:: rivus.converter.streets_to_edge
