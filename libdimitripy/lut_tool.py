__author__ = 'marrabld'

import scipy
import libdimitripy
import sys
import logger as log

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
        header_data = f.readline() # Skipt the first few lines
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
                elif tmp_line[1] == 'data,':

                    ##########
                    #  The order of the loop is important, so grab the label order
                    #  from the # data, <labels> line
                    ##########

                    self.lut_data = scipy.zeros(self.labels['dimensions'])

                    #  Start looping through the data
                    for i_iter, power_term in enumerate(self.labels['power_term']):
                        for j_iter, wind in enumerate(self.labels['wind']):
                            for k_iter, delta_phi in enumerate(self.labels['delta_phi']):
                                for l_iter, theta_v in enumerate(self.labels['theta_v']):
                                    for m_iter, theta_s in enumerate(self.labels['theta_s']):
                                        tmp_data = f.readline().rstrip('\n')
                                        # Check to see if it is a blank line
                                        if tmp_data.strip() == "":
                                            tmp_data = f.readline()  # ignore and read the next line
                                        tmp_data = scipy.fromstring(tmp_data, DTYPE, sep=' ')
                                        for n_iter, wavelength in enumerate(self.labels['lambda']):
                                            #self.lut_data[i_iter][j_iter][k_iter][l_iter][m_iter][n_iter] = \
                                            #    tmp_data[n_iter]
                                            self.lut_data[n_iter][m_iter][l_iter][k_iter][j_iter][i_iter]
                    done = True

        return self.lut_data


    def get_value(self, power_term, wind, delta_phi, theta_v, theta_s, wavelength):

        # These are indexes.
        return self.lut_data[power_term][wind][delta_phi][theta_v][theta_s][wavelength]










