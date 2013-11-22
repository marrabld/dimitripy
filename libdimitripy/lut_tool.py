__author__ = 'marrabld'

import scipy
import libdimitripy
import sys
import logger as log
import os
import csv
import glob
import scipy.interpolate

DTYPE = libdimitripy.base.GLOBALS.DTYPE
DEBUG_LEVEL = libdimitripy.base.GLOBALS.DEBUG_LEVEL
lg = log.logger
lg.setLevel(DEBUG_LEVEL)
sys.path.append("../..")


class Lut():
    def __init__(self):
        self.labels = {}
        self.lut_data = None

    def read_lut(self, filename):

        ##########
        #  Read the header information and save to class properties
        ##########
        done = False

        f = open(filename, 'rb')
        header_data = f.readline()  # Skip the first few lines
        header_data = f.readline()
        header_data = f.readline()

        while not done:


            header_data = f.readline()
            if header_data[0] == '#':  # Then we have a comment
                tmp_line = header_data.split(' ')
                if tmp_line[1] != 'data,':  # If it's not data then it must be header ?
                    tmp_label = tmp_line[1].rstrip('\n')
                    tmp_data = f.readline()
                    try:
                        #tmp_data = map(float, tmp_data)
                        tmp_float = scipy.fromstring(tmp_data, DTYPE, sep=' ')
                        self.labels[tmp_label] = scipy.asarray(tmp_float)
                    except:
                        lg.exception("Couldn't read LUT file label :: " + str(tmp_data) + ' in ' + filename)

                elif (tmp_line[1] == 'data,') and (not '_aot_' in filename):

                    ##########
                    #  The order of the loop is important, so grab the label order
                    #  from the # data, <labels> line
                    ##########

                    self.lut_data = scipy.zeros(self.labels['dimensions'])

                    #  Start looping through the data
                    if 'BO' in filename:
                        aerosol_label = 'power_term'
                    else:
                        aerosol_label = 'tau550'

                    for i_iter, power_term in enumerate(self.labels[aerosol_label]):  # May be tau550 or powerterm
                        for j_iter, wind in enumerate(self.labels['wind']):
                            for k_iter, delta_phi in enumerate(self.labels['delta_phi']):
                                for l_iter, theta_v in enumerate(self.labels['theta_v']):
                                    for m_iter, theta_s in enumerate(self.labels['theta_s']):
                                        tmp_data = f.readline().rstrip('\n')
                                        # Check to see if it is a blank line
                                        while tmp_data.strip() == "":
                                            tmp_data = f.readline()  # ignore and read the next line
                                        tmp_data = scipy.fromstring(tmp_data, DTYPE, sep=' ')
                                        for n_iter, wavelength in enumerate(self.labels['lambda']):
                                            self.lut_data[n_iter][m_iter][l_iter][k_iter][j_iter][i_iter] = \
                                                tmp_data[n_iter]

                    done = True
                elif (tmp_line[1] == 'data,') and ('_aot_' in filename):
                    self.lut_data = scipy.zeros(self.labels['dimensions'])
                    for i_iter, tau550 in enumerate(self.labels['tau550']):
                        tmp_data = f.readline().rstrip('\n')
                        # Check to see if it is a blank line
                        while tmp_data.strip() == "":
                            tmp_data = f.readline()  # ignore and read the next line
                        tmp_data = scipy.fromstring(tmp_data, DTYPE, sep=' ')
                        for j_iter, wavelength in enumerate(self.labels['lambda']):
                            self.lut_data[j_iter][i_iter] = tmp_data[j_iter]
                    done = True

        return self.lut_data, self.labels

    def read_rsr_from_directory(self, directory):
        # for files in directory read them in.  build a 3D array and return for convolving

        rsr_files = glob.glob(directory + '/*.txt')
        rsr_list = []

        for rsr_file in rsr_files:
            # get the number of lines in the file and preallocate an array
            num_lines = self.file_len(rsr_file)
            rsr_2d = scipy.zeros((num_lines - 1, 2))  # -1 because of the header

            rsr_file = open(rsr_file) # now we make it a file object
            rsr_reader = csv.reader(rsr_file, delimiter=';')
            for row_num, row in enumerate(rsr_reader):
                if row_num == 0:
                    pass
                else:
                    for col_num, col in enumerate(row):
                        rsr_2d[row_num - 1][col_num] = col

            rsr_list.append(rsr_2d)

        return rsr_list

    def convolve_rsr_lut(self, rsr_list, lut, lut_labels):

        # Figure out wave lengths belong to which list.
        band_min = []
        band_max = []
        function_handle_list = []

        for rsr in rsr_list:
            band_min.append(scipy.min(rsr[:, 0]))
            band_max.append(scipy.max(rsr[:, 0]))

        dimitri_lut_data = scipy.zeros(lut_labels['dimensions'])

        if 'power_term' in lut_labels.keys():
            aerosol_label = 'power_term'
        elif 'tau550' in lut_labels.keys():
            aerosol_label = 'tau550'

        for i_iter, power_term in enumerate(lut_labels[aerosol_label]):  # May be tau550 or powerterm
            for j_iter, wind in enumerate(lut_labels['wind']):
                for k_iter, delta_phi in enumerate(lut_labels['delta_phi']):
                    for l_iter, theta_v in enumerate(lut_labels['theta_v']):
                        for m_iter, theta_s in enumerate(lut_labels['theta_s']):
                            # interpolate a function handle for the RSRs
                            for i_iter, rsr_func in enumerate(rsr_list):
                                ##########
                                #  for all the RSRs we generate an interpolation function
                                ##########
                                f = scipy.interpolate.interp1d(rsr_list[i_iter][:, 0], rsr_list[i_iter][:, 1])
                                function_handle_list.append(f)

                            for n_iter, wavelength in enumerate(lut_labels['lambda']):
                                #dimitri_lut_data[n_iter][m_iter][l_iter][k_iter][j_iter][i_iter] = 0
                                pass  #  TODO all below.
                                ##########
                                #  For each wavelength, figure out which interpolation function to call
                                #  find the wavelength in a band find the RSR weight
                                #  The centre band is the [sum weight x LUT] / [sum weights]
                                #  convolve the functions.
                                ##########

                                ##########
                                # Write the centre band value to the new LUT
                                # write the new lut_label as well.
                                ##########
        pass



    def file_len(self, fname):
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
        return i + 1

    def get_value(self, power_term, wind, delta_phi, theta_v, theta_s, wavelength):

        # These are indexes.
        return self.lut_data[power_term][wind][delta_phi][theta_v][theta_s][wavelength]










