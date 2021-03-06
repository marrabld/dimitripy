__author__ = 'marrabld'

import scipy
import libdimitripy
import sys
import logger as log
import os
import csv
import glob
import scipy.interpolate
import libdimitripy.helper_functions

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
                    if 'BO' in filename and 'func' in filename:
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
        rsr_files = libdimitripy.helper_functions.Sort.natural_sort(rsr_files)
        rsr_list = []

        for rsr_file in rsr_files:
            # get the number of lines in the file and preallocate an array
            num_lines = self.file_len(rsr_file)
            rsr_2d = scipy.zeros((num_lines - 1, 2))  # -1 because of the header

            rsr_file = open(rsr_file)  # now we make it a file object
            rsr_reader = csv.reader(rsr_file, delimiter=';')
            for row_num, row in enumerate(rsr_reader):
                if row_num == 0:
                    pass
                else:
                    for col_num, col in enumerate(row):
                        rsr_2d[row_num - 1][col_num] = col

            #rsr_2d = scipy.trim_zeros(rsr_2d)  # Some of the csv files have trailing lines
            #tmp_0 = scipy.trim_zeros(rsr_2d[:, 0])
            #tmp_1 = scipy.trim_zeros(rsr_2d[:, 1])
            tmp_0 = rsr_2d[:, 0]
            tmp_1 = rsr_2d[:, 1]
            rsr_2d = scipy.vstack((tmp_0.T, tmp_1.T)).T
            rsr_list.append(rsr_2d)

        return rsr_list

    def convolve_rsr_lut(self, rsr_list, lut, lut_labels):

        #  Todo, check the min and max values in the RSRs, if the are greater than the LUT then drop them from the list

        # Figure out wave lengths belong to which list.
        band_min = []
        band_max = []
        function_handle_list = []

        for rsr in rsr_list:
            band_min.append(rsr[:, 0].min())
            band_max.append(rsr[:, 0].max())

        ##########
        #  The dimitri dimensions is the same as lut but with less waves
        ##########
        dimitri_lut_data_dim = lut_labels['dimensions']
        dimitri_lut_data_dim[0] = len(rsr_list)
        dimitri_lut_data = scipy.zeros(dimitri_lut_data_dim)
        dimitri_lut_data[:] = scipy.NAN

        if 'power_term' in lut_labels.keys():
            aerosol_label = 'power_term'
        elif 'tau550' in lut_labels.keys():
            aerosol_label = 'tau550'

        if 'theta_s' in lut_labels:  # We must be a big LUT
            for i_iter, power_term in enumerate(lut_labels[aerosol_label]):  # May be tau550 or powerterm
                for j_iter, wind in enumerate(lut_labels['wind']):
                    for k_iter, delta_phi in enumerate(lut_labels['delta_phi']):
                        for l_iter, theta_v in enumerate(lut_labels['theta_v']):
                            for m_iter, theta_s in enumerate(lut_labels['theta_s']):
                                # interpolate a function handle for the RSRs
                                for n_iter, rsr_func in enumerate(rsr_list):
                                    ##########
                                    #  for all the RSRs we generate an interpolation function
                                    ##########
                                    f = scipy.interpolate.interp1d(rsr_list[n_iter][:, 0], rsr_list[n_iter][:, 1])

                                    ##########
                                    #  Grab all the waves from the lut in our band
                                    ##########
                                    idx_wave_min = lut_labels['lambda'] >= band_min[n_iter]
                                    idx_wave_max = lut_labels['lambda'] <= band_max[n_iter]
                                    idx_wave = idx_wave_min & idx_wave_max

                                    waves = lut_labels['lambda'][idx_wave]
                                    lut_vals = lut[idx_wave, m_iter, l_iter, k_iter, j_iter, i_iter]
                                    band_weights = 0
                                    band_ref = 0

                                    ##########
                                    #  convolve the LUT and RSR
                                    ##########

                                    for wave_iter, wave in enumerate(waves):
                                        try:
                                            band_ref += f(wave) * lut_vals[wave_iter]
                                            band_weights += f(wave)  # Sum all of the weights in the band
                                        except:
                                            print wave
                                            lg.exception(str(wave))


                                    ##########
                                    #  All of the waves are condensed down to one value which is the centre band
                                    #  of the RSR
                                    ##########

                                    ##########
                                    #  Need to figure out where to put the wavelength dim.
                                    #  As they are unlinkely go be parsed in order
                                    ##########
                                    sorted_band_max = scipy.sort(band_max)
                                    pos = scipy.linspace(0, len(band_max), len(band_max) + 1)
                                    pos = pos[sorted_band_max == band_max[n_iter]]
                                    if len(pos) > 1:
                                        #lg.warning('Duplicate band found in RSR')  # Spams the screen.
                                        pos = pos[0]

                                    wave_pos = int(pos)  # Adding [0] fixes bug where there are multiple bands with the same value

                                    if band_ref == 0 or band_weights == 0:
                                        lg.warning('no data for this band :: ' + str(wave) + ' making -999')
                                        dimitri_lut_data[wave_pos, m_iter, l_iter, k_iter, j_iter,
                                                         i_iter] = -999  # for now
                                    else:
                                        #dimitri_lut_data[wave_pos, m_iter, l_iter, k_iter, j_iter,
                                        #                 i_iter] = band_ref / band_weights
                                        dimitri_lut_data[n_iter, m_iter, l_iter, k_iter, j_iter,
                                                         i_iter] = band_ref / band_weights

        else:  # We are the small LUT
            for i_iter, power_term in enumerate(lut_labels['tau550']):
                for j_iter, rsr_func in enumerate(rsr_list):
                    ##########
                    #  for all the RSRs we generate an interpolation function
                    ##########
                    f = scipy.interpolate.interp1d(rsr_list[j_iter][:, 0], rsr_list[j_iter][:, 1])

                    ##########
                    #  Grab all the waves from the lut in our band
                    ##########
                    idx_wave_min = lut_labels['lambda'] >= band_min[j_iter]
                    idx_wave_max = lut_labels['lambda'] <= band_max[j_iter]
                    idx_wave = idx_wave_min & idx_wave_max

                    waves = lut_labels['lambda'][idx_wave]
                    lut_vals = lut[idx_wave, i_iter]
                    band_weights = 0
                    band_ref = 0

                    for wave_iter, wave in enumerate(waves):
                        band_ref += f(wave) * lut_vals[wave_iter]
                        band_weights += f(wave)  # Sum all of the weights in the band

                    ##########
                    #  All of the waves are condensed down to one value which is the centre band
                    #  of the RSR
                    ##########

                    ##########
                    #  Need to figure out where to put the wavelength dim.
                    #  As they are unlikely go be parsed in order
                    ##########
                    sorted_band_max = scipy.sort(band_max)
                    pos = scipy.linspace(0, len(band_max), len(band_max) + 1)
                    wave_pos = int(pos[sorted_band_max == band_max[j_iter]][0])  # Adding [0] fixes bug where there are multiple bands with the same value

                    #dimitri_lut_data[wave_pos, i_iter] = band_ref / band_weights
                    dimitri_lut_data[j_iter, i_iter] = band_ref / band_weights


        return dimitri_lut_data


    def file_len(self, fname):
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
        return i + 1

    def get_value(self, power_term, wind, delta_phi, theta_v, theta_s, wavelength):

        # These are indexes.
        return self.lut_data[power_term][wind][delta_phi][theta_v][theta_s][wavelength]


    def write_trans_lut_to_file(self, lut, lut_labels, filename='lut.txt', header_txt='#'):

        f = open(filename, 'wb')
        writer = csv.writer(f, delimiter=' ')

        ##########
        #  Write header information
        #  which we grab from lut_label
        ##########

        f.write(header_txt)
        f.write('# lambda: ')
        writer.writerow(lut_labels['lambda'])
        if lut_labels['theta_s'].shape[0] > 1:
            f.write('# thetas: ')
            writer.writerow(lut_labels['theta_s'])
        if lut_labels['theta_v'].shape[0] > 1:
            f.write('# thetav: ')
            writer.writerow(lut_labels['theta_v'])
            #f.write('# deltaphi: ')
        #writer.writerow(lut_labels['delta_phi'])
        if lut_labels['theta_v'].shape[0] > 1:
            f.write('# Inner loop is on thetav, then on bands \n')
        else:
            f.write('# Inner loop is on thetas, then on bands \n')
        dim = str(lut_labels['dimensions'])
        dim = dim.replace('1.', '').replace('[', '').replace(']', '').replace('.', '').strip()
        dim = ' '.join(dim.split())  # get rid of repeating spaces replace them with only one.
        f.write('# Dimensions: ' + dim + '\n')
        for wave_iter, wavelength in enumerate(lut_labels['lambda']):
            for i_iter, theta_s in enumerate(lut_labels['theta_s']):
                for j_iter, theta_v in enumerate(lut_labels['theta_v']):
                    for k_iter, delta_phi in enumerate(lut_labels['delta_phi']):
                        for l_iter, wind in enumerate(lut_labels['wind']):
                            val = lut[wave_iter, i_iter, j_iter, k_iter, l_iter, :]
                            writer.writerow(val)

    def write_aot_lut_to_file(self, lut, lut_labels, filename='aot_lut.txt', header_txt='#'):

        f = open(filename, 'wb')
        writer = csv.writer(f, delimiter=' ')

        ##########
        #  Write header information
        #  which we grab from lut_label
        ##########

        f.write(header_txt)
        f.write('# lambda: ')
        writer.writerow(lut_labels['lambda'])
        # Have to add 1 on to the final dimension to allow for tau = 0
        dim = lut_labels['dimensions']
        dim[-1] += 1
        dim = str(dim)
        dim = dim.replace('1.', '').replace('[', '').replace(']', '').replace('.', '').strip()
        dim = ' '.join(dim.split())  # get rid of repeating spaces replace them with only one.
        f.write('# Dimensions: ' + dim + '\n')
        for wave_iter, wavelength in enumerate(lut_labels['lambda']):
            val = lut[wave_iter, :]
            f.write('0.0 ')
            writer.writerow(val)

    def write_rayleigh_lut_to_file(self, lut, lut_labels, filename='R_lut.txt', header_txt='#'):
        f = open(filename, 'wb')
        writer = csv.writer(f, delimiter=' ')

        ##########
        #  Write header information
        #  which we grab from lut_label
        ##########

        f.write(header_txt)
        f.write('# lambda: ')
        writer.writerow(lut_labels['lambda'])
        f.write('# thetas: ')
        writer.writerow(lut_labels['theta_s'])
        f.write('# thetav: ')
        writer.writerow(lut_labels['theta_v'])
        f.write('# deltaphi: ')
        writer.writerow(lut_labels['delta_phi'])
        f.write('# wind: ')
        writer.writerow(lut_labels['wind'])
        f.write('# Inner loop is on wind, then deltaphi, thetav, thetas and bands\n')
        dim = str(lut_labels['dimensions'])
        dim = dim.replace('1.', '').replace('[', '').replace(']', '').replace('.', '').strip()
        dim = ' '.join(dim.split())  # get rid of repeating spaces replace them with only one.
        f.write('# Dimensions: ' + dim[:-1] + '\n')
        for wave_iter, wavelength in enumerate(lut_labels['lambda']):
            for i_iter, theta_s in enumerate(lut_labels['theta_s']):
                for j_iter, theta_v in enumerate(lut_labels['theta_v']):
                    for k_iter, delta_phi in enumerate(lut_labels['delta_phi']):
                        for l_iter, wind in enumerate(lut_labels['wind']):
                            val = lut[wave_iter, i_iter, j_iter, k_iter, l_iter, 0]
                            writer.writerow([val])


    def write_func_lut_to_file(self, lut, lut_labels, filename='func_lut.txt', header_txt='#'):
        f = open(filename, 'wb')
        writer = csv.writer(f, delimiter=' ')

        ##########
        #  Write header information
        #  which we grab from lut_label
        ##########

        f.write(header_txt)
        f.write('# lambda: ')
        writer.writerow(lut_labels['lambda'])
        f.write('# thetas: ')
        writer.writerow(lut_labels['theta_s'])
        f.write('# thetav: ')
        writer.writerow(lut_labels['theta_v'])
        f.write('# deltaphi: ')
        writer.writerow(lut_labels['delta_phi'])
        f.write('# wind: ')
        writer.writerow(lut_labels['wind'])
        dim = str(lut_labels['dimensions'])
        dim = dim.replace('1.', '').replace('[', '').replace(']', '').replace('.', '').strip()
        dim = ' '.join(dim.split())  # get rid of repeating spaces replace them with only one.
        f.write('# Dimensions: ' + dim + '\n')
        for wave_iter, wavelength in enumerate(lut_labels['lambda']):
            for i_iter, theta_s in enumerate(lut_labels['theta_s']):
                for j_iter, theta_v in enumerate(lut_labels['theta_v']):
                    for k_iter, delta_phi in enumerate(lut_labels['delta_phi']):
                        for l_iter, wind in enumerate(lut_labels['wind']):
                            val = lut[wave_iter, i_iter, j_iter, k_iter, l_iter, :]
                            writer.writerow(val)












