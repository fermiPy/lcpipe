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

Dispatching Jobs
----------------

