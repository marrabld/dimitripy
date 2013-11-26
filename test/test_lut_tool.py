__author__ = 'marrabld'

import sys

sys.path.append("../..")

import unittest
import scipy
import libdimitripy.ingest
import libdimitripy.base
import libdimitripy.brdf
import libdimitripy.lut_tool
import os
import pylab


class TestLutTool(unittest.TestCase):
    def setUp(self):
        #self.test_dir = '/home/marrabld/projects/dimitripy/scripts/data/LUTS/demo_mc50'
        self.test_dir = '/home/marrabld/projects/dimitripy/scripts/data/LUTS/hs386_mc50'

        self.rsr_dir = '/home/marrabld/projects/DIMITRI_2.0/AUX_DATA/spectral_response/MERIS'
        #test_file = 'demo_PP_V_MC50_BO_10000_func.txt'
        #test_file_2 = 'demo_tdown_PP_V_MC50_R010_100000_mean.txt'
        #test_file_3 = 'demo_tup_PP_V_MC50_R010_100000_mean.txt'
        #test_file_4 = 'demo_aot_PP_V_MC50.txt'
        test_file = 'hs386_PP_V_MC50_BO_10000_func.txt'
        test_file_2 = 'hs386_tdown_PP_V_MC50_R010_100000_mean.txt'
        test_file_3 = 'hs386_tup_PP_V_MC50_R010_100000_mean.txt'
        test_file_4 = 'hs386_aot_PP_V_MC50.txt'

        self.test_file_1 = os.path.join(self.test_dir, test_file)
        self.test_file_2 = os.path.join(self.test_dir, test_file_2)
        self.test_file_3 = os.path.join(self.test_dir, test_file_3)
        self.test_file_4 = os.path.join(self.test_dir, test_file_4)
        self.lut = libdimitripy.lut_tool.Lut()

    #def test_read_lut(self):
    #    lut, lut_label = self.lut.read_lut(self.test_file_1)
    #    self.assertIsInstance(lut, scipy.ndarray)
    #
    #    lut, lut_label = self.lut.read_lut(self.test_file_2)
    #    self.assertIsInstance(lut, scipy.ndarray)
    #
    #    lut, lut_label = self.lut.read_lut(self.test_file_3)
    #    self.assertIsInstance(lut, scipy.ndarray)
    #
    #    lut, lut_label = self.lut.read_lut(self.test_file_4)
    #    self.assertIsInstance(lut, scipy.ndarray)
    #
    #def test_read_rsr_from_directory(self):
    #    rsr_list = self.lut.read_rsr_from_directory(self.rsr_dir)
    #    self.assertIsInstance(rsr_list, list)
    #
    def test_convolve_rsr_lut(self):
        lut, lut_lables = self.lut.read_lut(self.test_file_3)
        rsr_list = self.lut.read_rsr_from_directory(self.rsr_dir)
        dimitri_lut = self.lut.convolve_rsr_lut(rsr_list, lut, lut_lables)
        self.assertIsInstance(dimitri_lut, scipy.ndarray)
        #pylab.plot(dimitri_lut[0, 0, 0, 0, 0, 0])
        #pylab.show()
#
    def test_write_trans_lut_to_file(self):
        lut, lut_lables = self.lut.read_lut(self.test_file_3)
        print(lut.shape)
        rsr_list = self.lut.read_rsr_from_directory(self.rsr_dir)
        dimitri_lut = self.lut.convolve_rsr_lut(rsr_list, lut, lut_lables)
        print(dimitri_lut.shape)
        waves = scipy.asarray(
            [412.5, 442.5, 490.0, 510.0, 560.0, 620.0, 665.0, 681.25, 708.75, 753.75, 761.875, 778.75, 865.0, 885.0,
             900.0])
        lut_lables['lambda'] = waves
        header_string = "# MERIS total upward transmittance (direct+diffuse, Rayleigh+aerosol) for aerosol model MAR-50 \n\
# Columns gives t_up for 7 aerosol optical thickness (total, i.e. all layers) given in file taua_1.txt \n\
# (first optical thickness is zero hence gives Rayleigh transmittance) \n\
# Lines are for all bands, thetas, thetav, deltaphi and wind speed given by:\n"

        self.lut.write_trans_lut_to_file(dimitri_lut, lut_lables, 't_up_lut_test.txt', header_txt=header_string)


    def test_lut_nums(self):
        lut, lut_lables = self.lut.read_lut(self.test_file_3)
        idx_wave = lut_lables['lambda'] == 412
        print(lut[idx_wave, 0, 0, 0, 0, :])


