import scipy.io
from scipy.io import netcdf

__author__ = 'marrabld'

"""
This package holds methods for reading in data files.
"""

# Module global.  Used as default values in the constructors.
BANDS = {'PARASOL': [443, 490, 565, 670, 754, 760, 865, 910, 1020],
          'MERIS': [412, 443, 490, 510, 560, 620, 665, 681, 708, 753, 761, 778, 865, 885, 900],
          'VIIRS': [412, 445, 488, 555, 672, 746, 865, 1240, 1378, 1610, 2250]}


class DimitriFiles():
    """
    Class for reading in Dimitriv2 generated files
    """

    def __init__(self):
        pass

    @staticmethod
    def read_dimitri_sav_file(file_name, sensor_name, bands=BANDS):
        """
        Reads the DIMITRIv2.sav files in the native IDL format.

        @param file_name: <String> The name of the file to read.
        @param sensor_name: <String> The name of the sensor
        @param bands: <dictionary>[<string>:<list>] The name/wavelength pair
        @return: <dictionary> A python dictionary of the metadata
        """
        meta_data = {}
        tmp_array = scipy.io.readsav(file_name, python_dict=True)['sensor_l1b_ref']
        meta_data['sensor_name'] = sensor_name
        meta_data['bands'] = bands[sensor_name]
        meta_data['num_bands'] = len(meta_data['bands'])  # TODO need to get the number of bands
        meta_data['decimal_year'] = tmp_array[:, 0]
        meta_data['sensor_zenith'] = tmp_array[:, 1]
        meta_data['sensor_azimuth'] = tmp_array[:, 2]
        meta_data['sun_zenith'] = tmp_array[:, 3]
        meta_data['sun_azimuth'] = tmp_array[:, 4]
        meta_data['ozone'] = tmp_array[:, 5]
        meta_data['pressure'] = tmp_array[:, 6]
        meta_data['relative_humidity'] = tmp_array[:, 7]
        meta_data['wind_zonal'] = tmp_array[:, 8]
        meta_data['wind_merid'] = tmp_array[:, 9]
        meta_data['wvap'] = tmp_array[:, 10]
        meta_data['reflectance'] = tmp_array[:, 17:17 + len(bands)]
        meta_data['reflectance_std'] = tmp_array[:, 17 + len(bands):, ]

        return meta_data

    @staticmethod
    def read_dimitri_netcdf_file(file_name):
        f = netcdf.netcdf_file(file_name, 'r')

        return f


class RawFiles():
    """
    Methods for reading 'raw' satellite files.
    """

    def __init__(self):
        pass

