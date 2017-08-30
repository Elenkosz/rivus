#########
Overview
#########

This section will:

* Get an understanding how rivus is built up and why.
* Introduce you to the sub packages and direct you to their documentation.
* Clearify what data is aspected as input and what you can aspect as output.

.. _a_tutorial:

***********************
Targets and Data-Flow
***********************

OSM - abstract.

.. todo::
  + Explain differences. OSM extract, QGIS layer, Abstraction
  + Add flow-charts
  + Explain input parameters

*************
Structuring
*************

``rivus`` after version 0.1 became self-contained. Its restructuring is still not
complete, but the sub packages aim to bundle the similar functions together.
Goals to achieve with it:

* Plug-in opportunity for new functionality.
* Smaller, and thus easier maintainable files.
* Easier code reusability.
* "Structural documentation"

Main - ``rivus.main``
=======================

Core binding to the Pyomo model. The most 'mathematically programmed' part of the code base.

Mathematical documentation
---------------------------

.. todo::
  Extract description from ojdo's thesis

Utils - ``rivus.utils``
=========================

Universal code snippets, which can get handy generally. From setting up solver parameters to parameter range generator,
you can find here the


************
Limitations
************

The works done with rivus were restricted to the the urban level.
Theoretically, there is no barrier for the model to reach for bigger structures. however,
pragmatically a performance boost would push the project to be more fun to work with bigger or more detailed problems.

As for the current state, ``rivus`` does not consider already existing energy infrastructure networks.
Thus the solution always assumes a "from scratch" planning. (Feature is planned to be developed.)
