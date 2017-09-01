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

IO - ``rivus.io``
==================

Plotting - ``rivus.io.plot``
-----------------------------

.. raw:: html

  <div>
    <a href="https://plot.ly/~lnksz/46/?share_key=tF3hwedc2XqUAV9IFZNHVM" target="_blank" title="rivus002" style="display: block; text-align: center;"><img src="https://plot.ly/~lnksz/46.png?share_key=tF3hwedc2XqUAV9IFZNHVM" alt="rivus002" style="max-width: 100%;width: 600px;"  width="600" onerror="this.onerror=null;this.src='https://plot.ly/404.png';" /></a>
    <script data-plotly="lnksz:46" sharekey-plotly="tF3hwedc2XqUAV9IFZNHVM" src="https://plot.ly/embed.js" async></script>
  </div>

************
Limitations
************

The works done with rivus were restricted to the the urban level.
Theoretically, there is no barrier for the model to reach for bigger structures. however,
pragmatically a performance boost would push the project to be more fun to work with bigger or more detailed problems.

As for the current state, ``rivus`` does not consider already existing energy infrastructure networks.
Thus the solution always assumes a "from scratch" planning. (Feature is planned to be developed.)
