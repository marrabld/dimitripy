__author__ = 'marrabld'

import sys

sys.path.append("../..")

import unittest
import libdimitripy.ingest
import libdimitripy.base
import libdimitripy.cloud_screening

import os
import pickle
import scipy
import pylab


class TestBRDFMethod(unittest.TestCase):
    def setUp(self):
        self.test_file = '/home/marrabld/projects/DIMITRI_2.0/Input/Site_Libya4/MERIS/Proc_3rd_Reprocessing/MERIS_TOA_REF.dat'
        tmp_dict = libdimitripy.ingest.DimitriFiles.read_dimitri_sav_file(self.test_file, 'MERIS')

        self.test_object = libdimitripy.base.DimitriObject(tmp_dict)
        self.brdf_method = libdimitripy.cloud_screening.BRDFMethod()
        self.test_band = 4
        self.test_object.reflectance = self.test_object.reflectance[:, self.test_band]

    def test_train_model(self):
        k_coeffs = self.brdf_method.train_model(self.test_object)
        self.assertIsInstance(k_coeffs, scipy.ndarray)

    def test_calc_brdf_modelled_reflectance(self):
        k_coeffs = pickle.load(open('../libdimitripy/cache/brdf_cloud.p'))
        brdf_ref = self.brdf_method.calc_brdf_modelled_reflectance(self.test_object, k_coeffs)
        self.assertIsInstance(k_coeffs, scipy.ndarray)
        self.assertIsInstance(brdf_ref, scipy.ndarray)

    def test_score_images(self):
        k_coeffs = pickle.load(open('../libdimitripy/cache/brdf_cloud.p'))
        brdf_ref = self.brdf_method.calc_brdf_modelled_reflectance(self.test_object, k_coeffs)
        idx = self.brdf_method.score_images(self.test_object.reflectance, brdf_ref)
        # for i in idx:
        #    print(i)

        #print(type(idx[0]))
        self.assertIsInstance(idx, scipy.ndarray)
        #self.assertIsInstance(idx[0], numpy.bool_)