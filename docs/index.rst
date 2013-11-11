.. dimitripy documentation master file, created by
   sphinx-quickstart on Wed Oct  9 12:44:57 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to dimitripy's documentation!
=====================================

DIMITRI
=======

Database for Imaging Mulit-spectral Instruments and Tools for Radiometric Intercomparison

Overview
--------

DIMITRIPY is a python implimentation of DIMITRI

The DIMITRI software package contains a suite of IDL routines for the intercomparison of Top Of
Atmosphere (TOA) radiance and reflectance values within the 400nm - 4μm wavelength range; this
is generally known as Level 1b Earth Observation (EO) satellite data. The package includes product
reader and data extraction routines, and allows comparison of satellite data based on User defined
cloud screening parameters as well as temporal, spatial and geometric matching. DIMITRI is a
database containing the so-called remote sensing TOA reflectance values from 2002 until the
present day for ATSR2 (ESA), AATSR (ESA), MERIS (ESA), MODIS-Aqua (NASA), PARASOL POLDER-3
(CNES), and VEGETATION (CNES) over eight predetermined validation sites (see Table 1).
DIMITRI is supplied with all L1b data pre-loaded, giving instant access to time series of data which
totals more than 5 terabytes. Additional data for other validation sites, or more recent acquisitions,
can be ingested into DIMITRI to allow even greater temporal and spatial analysis.

System Requirements
-------------------

DIMITRIPY is a reimplimentation of DIMITRI which was originally
Python and Scipy.



How to use DIMITRI
------------------

Easy

DIMITRI Team
------------------
- Kathryn Barker (ARGANS)
- Dan Marrable (ARGANS)
- Marc Bouvet (ESA)

Contents:

.. toctree::
   :maxdepth: 2


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. automodule:: dimitripy.libdimitripy
    :members:

.. automodule:: dimitripy.libdimitripy.base
    :members:

.. automodule:: dimitripy.libdimitripy.post_processing_tool
    :members:

.. automodule:: dimitripy.libdimitripy.brdf
    :members:

.. automodule:: dimitripy.libdimitripy.cloud_screening
    :members:

.. automodule:: dimitripy.libdimitripy.ingest
    :members:

.. automodule:: dimitripy.libdimitripy.helper_functions
    :members:

