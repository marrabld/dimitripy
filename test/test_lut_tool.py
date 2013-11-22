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


class TestLutTool(unittest.TestCase):
    def setUp(self):
        self.test_dir = '/home/marrabld/projects/dimitripy/scripts/data/LUTS/demo_mc50'
        self.rsr_dir = '/home/marrabld/projects/DIMITRI_2.0/AUX_DATA/spectral_response/MERIS'
        test_file = 'demo_PP_V_MC50_BO_10000_func.txt'
        test_file_2 = 'demo_tdown_PP_V_MC50_R010_100000_mean.txt'
        test_file_3 = 'demo_tup_PP_V_MC50_R010_100000_mean.txt'
        test_file_4 = 'demo_aot_PP_V_MC50.txt'

        self.test_file_1 = os.path.join(self.test_dir, test_file)
        self.test_file_2 = os.path.join(self.test_dir, test_file_2)
        self.test_file_3 = os.path.join(self.test_dir, test_file_3)
        self.test_file_4 = os.path.join(self.test_dir, test_file_4)
        self.lut = libdimitripy.lut_tool.Lut()

    def test_read_lut(self):

        lut = self.lut.read_lut(self.test_file_1)
        self.assertIsInstance(lut, scipy.ndarray)

        lut = self.lut.read_lut(self.test_file_2)
        self.assertIsInstance(lut, scipy.ndarray)

        lut = self.lut.read_lut(self.test_file_3)
        self.assertIsInstance(lut, scipy.ndarray)

        lut = self.lut.read_lut(self.test_file_4)
        self.assertIsInstance(lut, scipy.ndarray)

    def test_read_rsr_from_directory(self):

        rsr_list = self.lut.read_rsr_from_directory(self.rsr_dir)
        self.assertIsInstance(rsr_list, list)