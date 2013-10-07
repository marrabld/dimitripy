import sys
sys.path.append("../..")

import scipy.io
from scipy.io import netcdf
import csv
import re
import dimitripy.base

DTYPE = dimitripy.base.GLOBALS.DTYPE

__author__ = 'marrabld'

"""
This package holds methods for reading in data files.
"""




class DimitriFiles():
    """
    Class for reading in Dimitriv2 generated files
    """

    def __init__(self):
        pass

    @staticmethod
    def read_dimitri_sav_file(filename, sensor_name, bands=dimitripy.base.GLOBALS.BANDS):
        """
        Reads the DIMITRIv2.sav files in the native IDL format.

        @param filename: <String> The name of the file to read.
        @param sensor_name: <String> The name of the sensor
        @param bands: <dictionary>[<string>:<list>] The name:wavelength pair
        @return: <dictionary> A python dictionary of the metadata
        """
        meta_data = {}
        tmp_array = scipy.io.readsav(filename, python_dict=True)['sensor_l1b_ref']
        meta_data['sensor_name'] = sensor_name
        meta_data['bands'] = bands[sensor_name]
        meta_data['num_bands'] = len(meta_data['bands'])
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

    #noinspection PyNoneFunctionAssignment
    @staticmethod
    def read_dimitri_intercomparison_file(filename):
        """
        Reads the DIMITRIv2 generated intercomparison .csv files.  Creates two
        dictionaries where the key is the parameters in the file for both sensors.

        @param filename: <String> The name of the file to read.
        @return: <list><dictionary> A python list of 2 dictionaries of the metadata

        """

        meta_data = {'bands': []}  # Use this later to build the DimitriObject.

        with open(filename, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            for r_index, row in enumerate(csv_reader):
                if r_index == 0:
                    # Skip the first row, its a header
                    tmp = row  # we don't need it.
                    del tmp
                else:
                    if r_index == 1:
                        # grab the sensor name only once
                        meta_data['sensor_name'] = row[1]

                    if r_index > 1 and meta_data['sensor_name'] != row[
                        1]:  # we have moved through the file and on to the second sensor
                        r1_meta_data = meta_data
                        del meta_data
                        meta_data = {'bands': []}
                        meta_data['sensor_name'] = row[1]

                    # The first few rows, will be all the metadata we need so we use them as the keys
                    # for the dictionary.  As long as it doesn't start with TOA*
                    if 'TOA' in row[3] and 'REF' in row[3]:
                        wave = re.findall(r'\d+', row[3])
                        meta_data['bands'].append(wave[0])  # Pulls the numbers out of the string
                        # Find the element in the list that the wave is and add the TOA
                        wave_index = meta_data['bands'].index(wave[0])
                        # Check if 'reflectance' exists, if not create it here cos we now know the size.
                        if meta_data.has_key('reflectance'):
                            tmp = scipy.empty((1, len(row[
                                                      4:])))  # Make it 2 dimensions, not the best way I am usre.  TODO check better way edit, can use squeeze
                            tmp = scipy.asarray(row[4:], dtype=DTYPE)
                            meta_data['reflectance'] = scipy.vstack((meta_data['reflectance'], tmp))
                        else:
                            meta_data['reflectance'] = scipy.empty((1, len(row[4:])))
                            meta_data['reflectance'][wave_index, :] = scipy.asarray(row[4:],
                                                                                    dtype=DTYPE)  # wave_index should be 0

                    elif 'TOA' in row[3] and 'STD' in row[3]:
                        wave = re.findall(r'\d+', row[3])
                        meta_data['bands'].append(wave[0])  # Pulls the numbers out of the string
                        # Find the element in the list that the wave is and add the TOA
                        wave_index = meta_data['bands'].index(wave[0])
                        if meta_data.has_key('reflectance_std'):
                            tmp = scipy.empty((1, len(
                                row[4:])))  # Make it 2 dimensions, not the best way I am usre.  TODO check better way
                            tmp = scipy.asarray(row[4:], dtype=DTYPE)
                            meta_data['reflectance_std'] = scipy.vstack((meta_data['reflectance_std'], tmp))
                        else:
                            meta_data['reflectance_std'] = scipy.empty((1, len(row[4:])))
                            meta_data['reflectance_std'][wave_index, :] = scipy.asarray(row[4:],
                                                                                        dtype=DTYPE)  # wave_index should be 0
                    else:
                        #  Need to translate the dialect so that the fields are the same as the keys

                        if row[3] == 'VZA':
                            key = 'sensor_zenith'
                        elif row[3] == 'VAA':
                            key = 'sensor_azimuth'
                        elif row[3] == 'SZA':
                            key = 'sun_zenith'
                        elif row[3] == 'SAA':
                            key = 'sun_azimuth'
                        elif row[3] == 'TIME':
                            key = 'decimal_year'
                        elif row[3] == 'OZONE_MU':
                            key = 'ozone'
                        elif row[3] == 'PRESSURE_MU':
                            key = 'pressure'
                        elif row[3] == 'HUMIDITY_MU':
                            key = 'relative_humidity'
                        elif row[3] == 'WIND_ZONAL_MU':
                            key = 'wind_zonal'
                        elif row[3] == 'WIND_MERID_MU':
                            key = 'wind_merid'
                        elif row[3] == 'WVAP_MU':
                            key = 'wvap'
                        else:
                            key = row[3]

                        meta_data[key] = row[4:]

        return [r1_meta_data, meta_data]


class RawFiles():
    """
    Methods for reading 'raw' satellite files.
    """

    def __init__(self):
        pass

