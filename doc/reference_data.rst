########################
Reference - Data Formats
########################

.. _a_datafromats:

**************
Data Formats
**************

How data is expected so that it will work.

.. _a_spreadsheet:

Spreadsheet
============

Let a short description of the columns ease your unerstaning of input variables.


Commodity
----------------
cost-inv-fix
    Fixed investment costs ``€/m``
    Capacity-independent investment costs for pipe/cable to transmit that commodity.   

cost-inv-var
    Variable invest costs ``€/kW/m``
    Capacity-dependent investment costs for transmission capacity of a commodity from one vertex to another.   

cost-fix
    Variable fixed costs ``€/kW/m``
    Capacity-dependent fixed costs for maintaining transmission capacity.  

cost-var
    Purchase costs ``€/kWh``
    Cost for buying that commodity at source vertices, if any exist in the vertex_shapefile.   

loss-fix
    Fixed loss fraction ``kW/m``
    Powerflow-independent loss of energy per meter of transmission length through the network. The fixed loss is calculated by (length * loss-fix).

loss-var
    Variable power loss ``1/kW/m``
    Relative loss term, dependent on input power flow through a ""pipe"":
    Ingoing power flow per edge is multiplied by (1 - length * loss-var)

cap-max
    Maximum capacity ``kW``
    Maximum possible transmission capacity per edge.

allowed-max
    Maximum allowed generation
    Limits the net amount of generation of this commodity (e.g. CO2). Note that processes that consume a commodity (e.g. CCS) can reduce the net amount.

Process
----------------

cost-inv-fix
    Fixed investment costs ``€``

    Up-front investment for building a plant, independent of size.
    Has value zero mainly for small-scale technologies.

cost-inv-var
    Specific investment costs ``€/kW``

    Size-dependent part for building a plant.

cost-fix
    Specific fixed costs ``€/kW``

    Size-dependent part for maintaining a plant.

cost-var
    Variable costs ``€/kWh``

    Operational costs to produce one unit of output, excluding fuel costs. Has value zero e.g. for PV or wind turbines (or if no sources are available).

cap-min
    Minimum capacity ``kW``

    Smallest size a plant is typically available in. Has value zero for domestic technologies.

cap-max
    Maximum capacity ``kW``

    Biggest capacity a plant typically is available in.


Process-Commodity
------------------

ratio
	Input/output ratio
    Flows in and out of processes, relative to 1 unit of throughput. For CO2, unit is kg/kWh (for example)

Time
------

weight
	Timestep weight ``hours``
    Length of timestep in hours. Sum of all weights == 8760

Elec
	Scaling factor Elec ``1``
    Relative scaling factor of demand 'Elec' per time step. Interpret like y-values of a normalised annual load duration curve.    

Heat
	Scaling factor Heat ``1``
    Relative scaling factor of demand 'Heat' per time step. Interpret like y-values of a normalised annual load duration curve.

Area-Demand
-------------

peak
	Building peak demand ``kW/ |m2|``
    Peak demand of building type (must be present in building_shapefile) normalised to building area. Annual demand is encoded in timestep weights on sheet Time.


.. _a_vertex:

Vertex 
=======

.. _a_edge:

Edge 
=======

