Waveform Data
-------------
Every inversion needs real data to be able to quantify misfits. The waveform
data for all events are stored in the ``DATA`` subfolder. The data for each
single event will be stored in a subfolder of the ``DATA`` folder with the
**same name as the QuakeML file minus the .xml**.

These folder are automatically created and updated each time a **LASIF**
command is executed. If you followed the tutorial, your directory structure
should resemble the following::

    Tutorial
    ├── ADJOINT_SOURCES_AND_WINDOWS
    │   ├── ADJOINT_SOURCES
    │   └── WINDOWS
    ├── CACHE
    ├── DATA
    │   ├── GCMT_event_NORTHERN_ITALY_Mag_4.9_2000-8-21-17-14
    │   ├── GCMT_event_NORTHWESTERN_BALKAN_REGION_Mag_5.9_1980-5-18-20-2
    ├── EVENTS
    │   ├── GCMT_event_NORTHERN_ITALY_Mag_4.9_2000-8-21-17-14.xml
    │   └── GCMT_event_NORTHWESTERN_BALKAN_REGION_Mag_5.9_1980-5-18-20-2.xml
    ├── ITERATIONS
    ├── KERNELS
    ├── LOGS
    ├── MODELS
    ├── OUTPUT
    ├── STATIONS
    │   ├── RESP
    │   ├── SEED
    │   └── StationXML
    ├── SYNTHETICS
    │   ├── GCMT_event_NORTHERN_ITALY_Mag_4.9_2000-8-21-17-14
    │   ├── GCMT_event_NORTHWESTERN_BALKAN_REGION_Mag_5.9_1980-5-18-20-2
    ├── WAVEFIELDS
    └── config.xml


All data in the ``DATA`` subfolder has to be processed or unprocessed actual
data. The data is further structured by assigning a tag to every data set. A
tag is assigned by simply placing a folder in ``ROOT/DATA/EVENT_NAME`` and
putting all data in there. The special tag ``raw`` is reserved for the raw
waveforms straight from the datacenters or some other source. Other tags should
describe the filtering and processing applied to the data (LASIF's built-in
processing capabilities actually enforce certain tag names - this will be
covered in more detail later on). The same is true for synthetic waveform data,
except that in that case, the data resides in the ``SYNTHETICS`` folder and
the tags have to coincide with the iteration names. More on this later on.

After a while, the structure might look like this::

    TutorialAnatolia
    |-- DATA
    │   ├── GCMT_event_NORTHERN_ITALY_Mag_4.9_2000-8-21-17-14
            |-- raw
            |-- preprocessed_hp_0.01000_lp_0.12500_npts_4000_dt_0.130000
        |...
    |-- SYNTHETICS
    │   ├── GCMT_event_NORTHERN_ITALY_Mag_4.9_2000-8-21-17-14
            |-- INVERSION_1
            |-- INVERSION_2
            |...
        |...
    |...

**The user is responsible** for adhering to that structure. Otherwise other
parts of LASIF cannot operate properly. Many commands shipping with LASIF ease
that process.

**LASIF** is able to deal with waveform data in essentially every common
format thanks to being built on top of ObsPy. We recommend to use the
MiniSEED format as that is the one actually shipped by effectively all data
centers.

Tutorial Data
^^^^^^^^^^^^^

Download the data for the tutorial
`here <https://raw.githubusercontent.com/wiki/krischer/LASIF/data/data.tar.bz2>`_
and place the contents in the ``DATA`` folder of the project. The ``raw``
subfolder should already be clear to you, the ``preprocessed_*`` folders will
be explained in the course of this tutorial.
