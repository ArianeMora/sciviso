********
sci-viso
********


Sci-viso is a wrapper around matplotlib and seaborn. These are already great libraries, but as I needed to generate
figures for publication, I found that I had specific formats that I needed, and continually adding these in was
making my code clunky and repetative. I also wanted my charts within a publication to have the same "look and feel",
like palette, font, sizing etc. So I made sciviso so that my figures could come out of python "publication ready" and
asthetic.

I have only made wrappers for charts that I use (obvs) but keen for people to add others or make suggestions (feel free
to do that via github issues).

Charts
======

Barchart
--------

.. figure:: _static/barchart.svg
   :width: 200
   :align: center


Boxplot (with statistics)
-------------------------

.. figure:: _static/boxplot.svg
   :width: 200
   :align: center

Heatmap
-------

.. figure:: _static/heatmap.svg
   :width: 200
   :align: center

Histogram
---------

.. figure:: _static/histogram.svg
   :width: 200
   :align: center

Scatterplot
-----------

.. figure:: _static/scatter2D.svg
   :width: 200
   :align: center

.. figure:: _static/scatter3d.svg
   :width: 200
   :align: center

Violinplot (with statistics)
----------------------------

.. figure:: _static/violin.svg
   :width: 200
   :align: center

Volcanoplot
-----------

.. figure:: _static/volcano.svg
   :width: 200
   :align: center

Each of these charts extends from a base vis which means the styles are set in the same way when the class is instanciated.
Things which come as present:

1) Generating the figures text as elements (for SVG & PDF export)
2) Consistent sizing: figure size & title, and label font sizes and styles
3) Colour (colourmaps, palletes) you can use any colours either as named from matplotlib, or HEX values.
4) X-axis text at 45 degrees for heatmaps & other charts when they have text on the x axis (e.g. boxplot & violinplots).
5) Statistics on box and violin plots (optional) and also colouring each box/violin by a specific colour.
6) Volcanoplot with the option to set colour cutoffs & also labelling of certain points.
7) Scatterplot with labelling of select points (2 and 3D plot).

For details check out the docs page on each of the charts.


Extending sci-viso
=================

1. Make a pull request on github - we have made the code extendable for the loss function etc.


Citing sci-viso
===============
Sci-viso can be cited as in :ref:`references`, where we also provide citations for the used tools (e.g. matplotlib & seaborn).

.. toctree::
   :caption: Getting started
   :maxdepth: 1

   about
   installing/index


.. toctree::
   :caption: Running sci-viso
   :maxdepth: 1

   examples/Barchart
   examples/Boxplot
   examples/Heatmap
   examples/Histogram
   examples/Scatterplot
   examples/Violinplot
   examples/Volcanoplot

.. toctree::
   :caption: About
   :maxdepth: 1

   faq
   changelog
   references
