__author__ = 'marrabld'

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

#self.test_dir = '/home/marrabld/projects/dimitripy/scripts/data/LUTS/demo_mc50'
hyper_lut_dir = '/home/marrabld/projects/dimitripy/scripts/data/LUTS/hs386_mc50'
dim_lut_dir= '/home/marrabld/projects/dimitripy/scripts/data/LUTS/DIMITRI'

rsr_dir = '/home/marrabld/projects/DIMITRI_2.0/AUX_DATA/spectral_response/MERIS'
#test_file = 'demo_PP_V_MC50_BO_10000_func.txt'
#test_file_2 = 'demo_tdown_PP_V_MC50_R010_100000_mean.txt'
#test_file_3 = 'demo_tup_PP_V_MC50_R010_100000_mean.txt'
#test_file_4 = 'demo_aot_PP_V_MC50.txt'
#hyper_lut_file = 'hs386_PP_V_MC50_BO_10000_func.txt'
#test_file = 'hs386_PP_V_MC50_BO_10000_mean.txt'

#hyper_lut_file = 'hs386_tup_PP_V_MC50_R010_100000_mean.txt'
hyper_lut_file = 'hs386_aot_PP_V_MC50.txt'
dim_lut_file = 'TAUA_MERIS_MAR-50.txt'

#test_file_3 = 'hs386_tup_PP_V_MC50_R010_100000_mean.txt'
#test_file_4 = 'hs386_aot_PP_V_MC50.txt'

hyper_lut_file = os.path.join(hyper_lut_dir, hyper_lut_file)
dim_lut_file = os.path.join(dim_lut_dir, dim_lut_file)

lut = libdimitripy.lut_tool.Lut()

hyper_lut, hyper_lut_lables = lut.read_lut(hyper_lut_file)
rsr_list = lut.read_rsr_from_directory(rsr_dir)
dimitri_lut = lut.convolve_rsr_lut(rsr_list, hyper_lut, hyper_lut_lables)

##########
#  Waves for the DIMITRI LUT
##########
waves = scipy.asarray(
    [412.5, 442.5, 490.0, 510.0, 560.0, 620.0, 665.0, 681.25, 708.75, 753.75, 761.875, 778.75, 865.0, 885.0,
     900.0])
hyper_lut_lables['lambda'] = waves
header_string = "# MERIS rayleigh reflectance \n# Lines are for all bands, thetas, thetav, deltaphi and wind speed given by:\n"

lut.write_aot_lut_to_file(dimitri_lut, hyper_lut_lables, dim_lut_file, header_txt=header_string)
