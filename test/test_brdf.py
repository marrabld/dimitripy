__author__ = 'marrabld'

__author__ = 'marrabld'
import sys
import scipy

sys.path.append("../..")

import unittest
import libdimitripy.ingest
import libdimitripy.base
import libdimitripy.brdf
import pylab
import os


class TestBrdf(unittest.TestCase):
    def setUp(self):
        self.test_file = '/home/marrabld/projects/DIMITRI_2.0/Input/Site_Libya4/MERIS/Proc_3rd_Reprocessing/MERIS_TOA_REF.dat'
        tmp_dict = libdimitripy.ingest.DimitriFiles.read_dimitri_sav_file(self.test_file, 'MERIS')

        # Test that we can use the dictionary to make a DimitriObject
        self.test_object = libdimitripy.base.DimitriObject(tmp_dict)
        self.test_band = 4
        self.brdf = libdimitripy.brdf.RoujeanBRDF()

        self.relative_azimuth = scipy.deg2rad(scipy.linspace(-90, 90, 180))
        self.sensor_zenith = scipy.deg2rad(30)
        #self.sensor_zenith = scipy.ones(180) * self.sensor_zenith

    def test_calc_kernel_f1(self):
        f1 = self.brdf.calc_kernel_f1(scipy.deg2rad(self.test_object.sun_zenith),
                                      scipy.deg2rad(self.test_object.sensor_zenith),
                                      scipy.deg2rad(self.test_object.relative_azimuth()))
        self.assertIsInstance(f1, scipy.ndarray)

    def test_calc_kernel_f1_plot(self):
        f1 = self.brdf.calc_kernel_f1(scipy.deg2rad(45), self.sensor_zenith, self.relative_azimuth)
        pylab.plot(f1)
        f1 = self.brdf.calc_kernel_f1(scipy.deg2rad(30), self.sensor_zenith, self.relative_azimuth)
        pylab.plot(self.relative_azimuth, f1)
        f1 = self.brdf.calc_kernel_f1(scipy.deg2rad(60), self.sensor_zenith, self.relative_azimuth)
        pylab.plot(self.relative_azimuth, f1)
        pylab.show()

    def test_calc_kernel_f2(self):
        f2 = self.brdf.calc_kernel_f1(self.test_object.sun_zenith, self.test_object.sun_azimuth,
                                      self.test_object.relative_azimuth())
        self.assertIsInstance(f2, scipy.ndarray)

    def test_calc_kernel_f2_plot(self):
        f2 = self.brdf.calc_kernel_f2(scipy.deg2rad(45), self.sensor_zenith, self.relative_azimuth)
        pylab.plot(self.relative_azimuth, f2)
        f2 = self.brdf.calc_kernel_f2(scipy.deg2rad(30), self.sensor_zenith, self.relative_azimuth)
        pylab.plot(self.relative_azimuth, f2)
        f2 = self.brdf.calc_kernel_f2(scipy.deg2rad(60), self.sensor_zenith, self.relative_azimuth)
        pylab.plot(self.relative_azimuth, f2)
        pylab.show()

    def test_calc_roujean_coeffs(self):
        k_coeff, residual, rank, singular_values = self.brdf.calc_roujean_coeffs(self.test_object.sun_zenith,
                                                                                 self.test_object.sun_azimuth,
                                                                                 self.test_object.relative_azimuth(),
                                                                                 self.test_object.reflectance[:,
                                                                                 self.test_band])
        #self.assertIsInstance(k_coeff, scipy.ndarray)
        #print(k_coeff)

    def test_model_brdf_timeseries(self):
        k_coeff, resampled_time, brdf, brdf_std, brdf_uncertainty_r, brdf_uncertainty_s = self.brdf.model_brdf_timeseries(
            self.test_object.sun_zenith,
            self.test_object.sensor_zenith,
            self.test_object.relative_azimuth(),
            self.test_object.reflectance[:, self.test_band],
            self.test_object.decimal_year,
            2002.0,
            2012.0)
        self.brdf.save_coeffs('k_coeff.csv', k_coeff)
        self.brdf.save_coeffs('ref.csv', self.test_object.reflectance)
        #pylab.plot(resampled_time, k_coeff[:, 0])
        #pylab.plot(resampled_time, k_coeff[:, 1])
        #pylab.plot(resampled_time, k_coeff[:, 2])

        #pylab.figure()

        decimal = scipy.asarray(self.test_object.decimal_year, dtype=scipy.float64)

        # Make these the same size and get rid of the -999s
        small_reflectance = self.test_object.reflectance[0:brdf.shape[0], self.test_band]
        idx = small_reflectance != -999

        pylab.plot(small_reflectance[idx], brdf[idx], '*')
        pylab.show()


       # idx = scipy.equal(decimal, resampled_time)

        #brdf = self.brdf.normalise_reflectance(self.test_object.sun_zenith[idx],
        #                                       self.test_object.relative_azimuth()[idx],
        #                                       k_coeff)

        #pylab.plot(resampled_time, brdf)
        #pylab.show()








