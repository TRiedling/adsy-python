adsy-python
===========

Adfinis-Sygroup Python Tools is the typical inhomogeneous collection of helpers and tools you always get when developing software. I [blog](http://ganwellresource.blogspot.ch) about the more interesting tools in adsy-python, the less interesting code is nonetheless useful.

Installation
------------

1. cd to a location in your PYTHONPATH. (ie subdirectory of your app)
2. git clone git://github.com/adfinis-sygroup/adsy-python.git adsy

The code is python 2.6, 2.7 and 3.x compatible

List of tools
-------------

* ipython notebook display tools (display.py)
  * display cursors and multidicts as tables
  * wrap and pretty print other data
* ipython notebook hide input (display.py)
  * nbconvert your ipython notebooks and hide the input
  * useful when sending notebooks to non-programmers
* helper to formulate queries as list comprehenions (iterator.py)
* Helpful tools for ipython notebooks (contains everything above)
  * Also contains a method to enable autoreload
  * A helper for automatic git bisect
