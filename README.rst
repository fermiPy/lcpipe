lcpipe
======

This package collects scripts and other tools for performing
lightcurve analysis with fermipy.

Creating Directory Structure
----------------------------

First compose a source list.  This should contain a dictionary with one entry per analysis instance:

.. code-block:: yaml

   source0 :
       selection: {target: source0}

   source1 :
       selection: {target: source1}


To generate the analysis directories call the ``fermipy-clone-config``
script with the baseline configuration and the source list provided to
the ``--source_list`` parameter:

.. code-block:: bash

   $ fermipy-clone-config --source_list=source_list.yaml --script=runLC.py --basedir=lc_runs/v0 base.yaml

This will generate one subdirectory for each entry in
``source_list.yaml`` with the name of the dictionary key.  A bash
script ``{SCRIPTNAME}.sh`` is also written that runs the python script
with its command-line arguments.

Running Batch Jobs
------------------

To dispatch jobs run the ``fermipy-dispatch`` script.  This script
accepts a list of analysis subdirectories and will run an analysis
instance for each directory.  The ``--runscript`` option sets the
analysis script to be run:

.. code-block:: bash

   $ fermipy-dispatch lc_runs/v0 --runscript=runLC.sh  --max_jobs 100 --time_per_cycle=60 --time=1000

The ``--time`` option sets the request time allocation for each job in minutes.  
