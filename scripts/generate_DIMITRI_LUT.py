__author__ = 'marrabld'

import sys

sys.path.append("../..")

import scipy
import libdimitripy.ingest
import libdimitripy.base
import libdimitripy.brdf
import libdimitripy.lut_tool
import os

SATELLITE = 'MERIS'
SAT_WAVES = scipy.asarray(
    [412.5, 442.5, 490.0, 510.0, 560.0, 620.0, 665.0, 681.25, 708.75, 753.75, 761.875, 778.75, 865.0, 885.0,
     900.0])

#hyper_lut_dir = '/home/marrabld/projects/dimitripy/scripts/data/LUTS/demo_mc50'
hyper_lut_dir = '/home/marrabld/projects/dimitripy/scripts/data/LUTS/hs386_mc50'
dim_lut_dir = '/home/marrabld/projects/dimitripy/scripts/data/LUTS/DIMITRI'
rsr_dir = '/home/marrabld/projects/DIMITRI_2.0/AUX_DATA/spectral_response/' + SATELLITE

##########
#  Trans up
##########
# Files to read in.  Hyper and Dimitri
hyper_lut_file = 'hs386_tup_PP_V_MC50_R010_100000_mean.txt'
dim_lut_file = 'TRA_UP_MERIS_MAR-50.txt'
hyper_lut_file = os.path.join(hyper_lut_dir, hyper_lut_file)
dim_lut_file = os.path.join(dim_lut_dir, dim_lut_file)

# LUT object from dimitripy
lut = libdimitripy.lut_tool.Lut()

# Grab the hyper lut and metadata
hyper_lut, hyper_lut_lables = lut.read_lut(hyper_lut_file)

# Convolve the spectral response functions
rsr_list = lut.read_rsr_from_directory(rsr_dir)
dimitri_lut = lut.convolve_rsr_lut(rsr_list, hyper_lut, hyper_lut_lables)

header_string = '# MERIS total upward transmittance (direct+diffuse, Rayleigh+aerosol) for aerosol model MAR-50\n# Columns gives t_up for 7 aerosol optical thickness (total, i.e. all layers) given in file taua_9.txt\n# (first optical thickness is zero hence gives Rayleigh transmittance)\n'
hyper_lut_lables['lambda'] = SAT_WAVES  # spoofing the vals here so we know which ones to convolve to.
lut.write_trans_lut_to_file(dimitri_lut, hyper_lut_lables, dim_lut_file, header_txt=header_string)

##########
#  Trans down
##########
# Files to read in.  Hyper and Dimitri
hyper_lut_file = 'hs386_tdown_PP_V_MC50_R010_100000_mean.txt'
dim_lut_file = 'TRA_DOWN_MERIS_MAR-50.txt'
hyper_lut_file = os.path.join(hyper_lut_dir, hyper_lut_file)
dim_lut_file = os.path.join(dim_lut_dir, dim_lut_file)

# LUT object from dimitripy
lut = libdimitripy.lut_tool.Lut()

# Grab the hyper lut and metadata
hyper_lut, hyper_lut_lables = lut.read_lut(hyper_lut_file)

# Convolve the spectral response functions
rsr_list = lut.read_rsr_from_directory(rsr_dir)
dimitri_lut = lut.convolve_rsr_lut(rsr_list, hyper_lut, hyper_lut_lables)

header_string = '# MERIS total upward transmittance (direct+diffuse, Rayleigh+aerosol) for aerosol model MAR-50\n# Columns gives t_up for 7 aerosol optical thickness (total, i.e. all layers) given in file taua_9.txt\n# (first optical thickness is zero hence gives Rayleigh transmittance)\n'
hyper_lut_lables['lambda'] = SAT_WAVES  # spoofing the vals here so we know which ones to convolve to.
lut.write_trans_lut_to_file(dimitri_lut, hyper_lut_lables, dim_lut_file, header_txt=header_string)

##########
#  AOT LUT
##########
# Files to read in.  Hyper and Dimitri
hyper_lut_file = 'hs386_aot_PP_V_MC50.txt'
dim_lut_file = 'TAUA_MERIS_MAR-50.txt'
hyper_lut_file = os.path.join(hyper_lut_dir, hyper_lut_file)
dim_lut_file = os.path.join(dim_lut_dir, dim_lut_file)

# LUT object from dimitripy
lut = libdimitripy.lut_tool.Lut()

# Grab the hyper lut and metadata
hyper_lut, hyper_lut_lables = lut.read_lut(hyper_lut_file)

# Convolve the spectral response functions
rsr_list = lut.read_rsr_from_directory(rsr_dir)
dimitri_lut = lut.convolve_rsr_lut(rsr_list, hyper_lut, hyper_lut_lables)

header_string = '# MERIS aerosol optical thickness for aerosol MAR-50\n# Columns gives tau_a corresponding to 7 reference optical thickness at 550 nm, see MERIS Reference Model Document\n# (first optical thickness is zero)\n'
hyper_lut_lables['lambda'] = SAT_WAVES  # spoofing the vals here so we know which ones to convolve to.
lut.write_aot_lut_to_file(dimitri_lut, hyper_lut_lables, dim_lut_file, header_txt=header_string)

##########
#  func LUT
##########

# Files to read in.  Hyper and Dimitri
hyper_lut_file = 'hs386_PP_V_MC50_BO_10000_func.txt'
dim_lut_file = 'XC_MERIS_MAR-50.txt'
hyper_lut_file = os.path.join(hyper_lut_dir, hyper_lut_file)
dim_lut_file = os.path.join(dim_lut_dir, dim_lut_file)

# LUT object from dimitripy
lut = libdimitripy.lut_tool.Lut()

# Grab the hyper lut and metadata
hyper_lut, hyper_lut_lables = lut.read_lut(hyper_lut_file)

# Convolve the spectral response functions
rsr_list = lut.read_rsr_from_directory(rsr_dir)
dimitri_lut = lut.convolve_rsr_lut(rsr_list, hyper_lut, hyper_lut_lables)

header_string = '# MERIS XC coefficients of rhopath/rhoR fit against optical thickness for aerosol model MAR-50\n# Columns gives the 3 XC coefficients\n# (first optical thickness is zero hence gives Rayleigh reflectance)\n'
hyper_lut_lables['lambda'] = SAT_WAVES  # spoofing the vals here so we know which ones to convolve to.
lut.write_func_lut_to_file(dimitri_lut, hyper_lut_lables, dim_lut_file, header_txt=header_string)

##########
#  Rayleigh LUT
##########

# Files to read in.  Hyper and Dimitri
hyper_lut_file = 'hs386_PP_V_MC50_BO_10000_mean.txt'
dim_lut_file = 'RHOR_MERIS.txt'
hyper_lut_file = os.path.join(hyper_lut_dir, hyper_lut_file)
dim_lut_file = os.path.join(dim_lut_dir, dim_lut_file)

# LUT object from dimitripy
lut = libdimitripy.lut_tool.Lut()

# Grab the hyper lut and metadata
hyper_lut, hyper_lut_lables = lut.read_lut(hyper_lut_file)

# Convolve the spectral response functions
rsr_list = lut.read_rsr_from_directory(rsr_dir)
dimitri_lut = lut.convolve_rsr_lut(rsr_list, hyper_lut, hyper_lut_lables)

header_string = '# MERIS rayleigh reflectance-2\n'
hyper_lut_lables['lambda'] = SAT_WAVES  # spoofing the vals here so we know which ones to convolve to.
lut.write_rayleigh_lut_to_file(dimitri_lut, hyper_lut_lables, dim_lut_file, header_txt=header_string)

##########
# Plot the two rayleigh LUTs
##########

#import pylab
#for i_iter, wave in enumerate(SAT_WAVES):
#    pylab.plot(dimitri_lut[i_iter, 0, 0, 0, 0])
#    #print(i_iter)
#
###########
##  Read in the MERIS LUT
###########
#import csv
#meris_lut = scipy.zeros((1, 8))
#meris_iter = 0
#meris_thetav = scipy.asarray(
#    [0.000000, 2.840910, 6.521060, 10.222950, 13.929760, 17.638420, 21.347980, 25.058050, 28.768431, 32.479012,
#     36.189732, 39.900551, 43.611439])
#
#f = open('/home/marrabld/projects/dimitripy/scripts/data/LUTS/MERIS/TRA_UP_MERIS_MAR-50.txt')
#csv_reader = csv.reader(f, delimiter=' ')
#for row in csv_reader:
#    if '#' in row:
#        pass
#    else:
#        meris_lut = scipy.vstack((meris_lut, scipy.asarray(row)))  # psuedo lut
#
#
#for i in range(0, SAT_WAVES.shape[0]):
#
#    pylab.plot(meris_lut[meris_iter:meris_iter + meris_thetav.shape[0], 0])
#    meris_iter += meris_thetav.shape[0]
#
#
##pylab.legend(lut_lables['lambda'])
#pylab.show()


