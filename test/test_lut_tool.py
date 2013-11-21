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
        test_dir = '/home/marrabld/projects/dimitripy/scripts/data/LUTS/demo_mc50'
        test_file = 'demo_PP_V_MC50_BO_10000_func.txt'
        self.test_file = os.path.join(test_dir, test_file)
        self.lut = libdimitripy.lut_tool.Lut()

    def test_read_lut(self):

        lut = self.lut.read_lut(self.test_file)
        self.assertIsInstance(lut, scipy.ndarray)
