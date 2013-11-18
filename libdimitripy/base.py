__author__ = 'marrabld'

"""
This package holds the classes used for storing and accessing satellite data from 'dimitri objects'
"""

import scipy


class GLOBALS():
    """
    # Module global.  Used as default values, change with caution.
    # don't change here.  Changing in settings file.  TODO load at startup from settings
    """
    BANDS = {'PARASOL': [443, 490, 565, 670, 754, 760, 865, 910, 1020],
             'MERIS': [412, 443, 490, 510, 560, 620, 665, 681, 708, 753, 761, 778, 865, 885, 900],
             'VIIRS': [412, 445, 488, 555, 672, 746, 865, 1240, 1378, 1610, 2250],
             'AATSR': [555, 660, 865, 1610, 3700, 10850, 12000],
             'ATSR2': [555, 660, 865, 1610, 3700, 10850, 12000],
             'MODISA': [412, 443, 487, 530, 547, 666, 666, 677, 677, 746, 866, 904, 936, 935, 1383, 566, 554, 1242,
                        1629, 2114, 646, 856],
             'VEGETATION': [450, 645, 835, 1665]
    }  # The position in the list is the band number.
    DTYPE = scipy.float64
    DEBUG_LEVEL = 'DEBUG'


class DimitriObject:
    """
    Holds the data for a single scene
    """

    def __init__(self):
        """

        @rtype : object
        """
        self.decimal_year = None
        self.sensor_zenith = None
        self.sensor_azimuth = None
        self.sun_zenith = None
        self.sun_azimuth = None
        self.ozone = None
        self.pressure = None
        self.relative_humidity = None
        self.wind_zonal = None
        self.wind_merid = None
        self.wvap = None
        self.bands = None
        self.sensor_name = None
        self.reflectance = None
        self.reflectance_std = None
        self.shape = None

    def __init__(self, meta_data):
        """
        Optional constructor method to define fields from a dictionary.  Required fields are
        decimal_year
        sensor_zenith
        sensor_zenith
        sun_zenith
        sun_azimuth
        ozone
        pressure
        relative_humidity
        wind_zonal
        wind_merid
        wvap
        bands
        sensor_name
        reflectance
        reflectance_std

        :param meta_data: A dictionary holding the metadata.
        """
        self.decimal_year = meta_data['decimal_year']
        self.sensor_zenith = meta_data['sensor_zenith']
        self.sensor_azimuth = meta_data['sensor_zenith']
        self.sun_zenith = meta_data['sun_zenith']
        self.sun_azimuth = meta_data['sun_azimuth']
        self.ozone = meta_data['ozone']
        self.pressure = meta_data['pressure']
        self.relative_humidity = meta_data['relative_humidity']
        self.wind_zonal = meta_data['wind_zonal']
        self.wind_merid = meta_data['wind_merid']
        self.wvap = meta_data['wvap']
        self.bands = meta_data['bands']
        self.sensor_name = meta_data['sensor_name']
        self.reflectance = meta_data['reflectance']
        self.reflectance_std = meta_data['reflectance_std']
        self.shape = meta_data['reflectance'].shape


    def __str__(self):
        return 'decimal_year,' \
               ' sensor_zenith,' \
               ' sensor_zenith,' \
               ' sun_zenith,' \
               ' sun_azimuth,' \
               ' ozone, pressure,' \
               ' relative_humidity,' \
               ' wind_zonal,' \
               ' wind_merid,' \
               ' wvap, bands,' \
               ' sensor_name,' \
               ' reflectance,' \
               ' reflectance_std,' \
               ' shape'

    def __getitem__(self, key):
        if key == 'reflectance':
            return self.reflectance
        elif key == 'decimal_year':
            return self.decimal_year
        elif key == 'sun_zenith':
            return self.sun_zenith
        elif key == 'sensor_name':
            return self.sensor_name
        else:
            raise KeyError(key)

    def relative_azimuth(self):
        """
        Returns the relative azimuth angle between the sun and sensor.  Checks the angles are sane.
        TODO write a unit test for this.
        """
        raa = scipy.absolute(self.sun_azimuth, self.sensor_azimuth)
        idx = raa > 180.0
        raa[idx] = 360.0 - raa[idx]

        return raa



class SatelliteObject(DimitriObject):
    """

    """

    def __init__(self):
        DimitriObject.__init__(self)

    def dummy(self):
        pass