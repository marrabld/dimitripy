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

A full IDL license is NOT required for DIMITRI V2.0; the freely available IDL Virtual Machine
(available at http://www.ittvis.com/ProductsServices/IDL/IDLModules/IDLVirtualMachine.aspx) will
allow use of the pre-compiled DIMITRI package and use of the full functionalities accessible from the
HMI.

DIMITRI has been developed to be compatible on both Linux and Windows based systems; however,
MAC compatibility cannot be guaranteed. DIMITRI has been developed for use with IDL 7.1 or
higher; the minimum requirements required for IDL 7.1 are therefore the minimum requirements for
running DIMITRI.

A full IDL license (http://www.ittvis.com) will allow command line usage, modification of routines
and recompilation of the software package.

How to use DIMITRI
------------------

Following extraction, DIMITRI is now ready to be utilised, this can be achieved by:
* On Windows: Double clicking the “DIMITRI_V2.0.sav” file, or running IDL runtime and
selecting the file
* On Linux: Typing “idl –vm=DIMITRI_V2.0.sav”

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

.. automodule:: dimitripy.libdimitripy.ingest
    :members:



