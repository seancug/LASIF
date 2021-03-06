Synthetics
----------

Now that everything is set up, you have to actually perform the simulations.
Please keep in mind that the adjoint forward simulations require a very large
amount of disc space due to the need to store the forward wavefield. Even
this very small toy example requires 10 GB per forward adjoint simulation.
This easily increases 100 fold for real simulations.

Copy the generated input files and the model for Iteration 1 to your SES3D
installation, adjust the ``ses3d_modules.f90`` file and run the adjoint
forwards simulations for the two events. Please refer to the SES3D manual
for additional details. The simulations should only take a couple of minutes
each on a run-of-the-mill computer. No need to turn to an HPC for this
tutorial.

Once the two simulations have run, copy the resulting synthetics to the
``SYNTHETICS/{{EVENT_NAME}}/ITERATION_{{ITERATION_NAME}}`` folder. Use the
raw SES3D output files. These have been calculated in the possibly different
simulation domain and not the physical domain. Never convert these to the
physical domain; **LASIF** does it for you and doing it twice is wrong.

Now might be a good time to fire up the :doc:`../webinterface` if you did not
already check if out. It features boil down to being an interactive
visualization platform of the current state of a LASIF project. You should
be able to see the two events including different types of waveform data.


Recap
^^^^^

Just a short recap, but at this point in the tutorial your folder structure
should look similar to this:

.. code-block:: none

    Tutorial/
    ├── DATA/
    │   ├── GCMT_event_NORTHERN_ITALY_Mag_4.9_2000-8-21-17-14/
    │   │   ├── preprocessed_hp_0.01000_lp_0.02500_npts_2000_dt_0.300000/
    │   │   └── raw
    │   └── GCMT_event_NORTHWESTERN_BALKAN_REGION_Mag_5.9_1980-5-18-20-2/
    │       ├── preprocessed_hp_0.01000_lp_0.02500_npts_2000_dt_0.300000/
    │       └── raw
    ├── EVENTS/
    │   ├── GCMT_event_NORTHERN_ITALY_Mag_4.9_2000-8-21-17-14.xml
    │   └── GCMT_event_NORTHWESTERN_BALKAN_REGION_Mag_5.9_1980-5-18-20-2.xml
    ├── ITERATIONS/
    │   └── ITERATION_1.xml
    ├── SYNTHETICS/
    │   ├── GCMT_event_NORTHERN_ITALY_Mag_4.9_2000-8-21-17-14/
    │   │   └── ITERATION_1/
    │   └── GCMT_event_NORTHWESTERN_BALKAN_REGION_Mag_5.9_1980-5-18-20-2/
    │       └── ITERATION_1/

