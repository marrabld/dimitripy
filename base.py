__author__ = 'marrabld'

"""
This package holds the classes used for storing and accessing satellite data from 'dimitri objects'
"""


class DimitriObject:
    """
    Holds the data for a single scene
    """

    def __init__(self):
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

    def __init__(self, meta_data):
        """
        Optional constructor method to define fields from a dictionary.  Required fields are
        decimal_year
        sensor_zenith
        sensor_azimuth
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

        @param meta_data: A dictionary holding the metadata.
        """
        self.decimal_year = meta_data['decimal_year']
        self.sensor_zenith = meta_data['sensor_zenith']
        self.sensor_azimuth = meta_data['sensor_azimuth']
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



class SatelliteObject(DimitriObject):
    """

    """

    def __init__(self):
        DimitriObject.__init__(self)

    def dummy(self):
        pass