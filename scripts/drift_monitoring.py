__author__ = 'marrabld'
import sys

sys.path.append("../..")

import os

print(os.getcwd())

import libdimitripy.ingest
import libdimitripy.base
import libdimitripy.post_processing_tool
import scipy
from Tkinter import Tk
from tkFileDialog import askdirectory

#directory = '/home/marrabld/projects/DIMITRI_2.0/Output/DomeC_20130417_REF_MERIS_3rd_Reprocessing'
#filename = 'ED_DomeC_MERIS_3rd_Reprocessing_PARASOL_Calibration_1.csv'

meris_bands = [4, 6, 12]
aatsr_bands = [0, 1, 2]
modisa_bands = [16, 20, 21]
parasol_bands = [2, 3, 6]
vgt_bands = [0, 1, 2]


Tk().withdraw()
directory = askdirectory()


#tmp_dict = libdimitripy.ingest.DimitriFiles.read_dimitri_intercomparison_file(os.path.join(directory, filename))
#

filenames = os.listdir(directory)

for filename in filenames:
    if 'ED_' in filename:
        print(filename)
        if 'PARASOL' in filename:
            comparison_bands = parasol_bands
        if 'AATSR' in filename or 'ATSR2' in filename:
            comparison_bands = aatsr_bands
        if 'MODISA' in filename:
            comparison_bands = modisa_bands
        if 'VEGETATION' in filename:
            comparison_bands = vgt_bands
        # process file and save the plot
        tmp_dict = libdimitripy.ingest.DimitriFiles.read_dimitri_intercomparison_file(os.path.join(directory, filename))

        reference_dimitri_object = libdimitripy.base.DimitriObject(tmp_dict[0])
        comparison_dimitri_object = libdimitripy.base.DimitriObject(tmp_dict[1])
        ts_comp = libdimitripy.post_processing_tool.TimeSeriesIntercomparison(reference_dimitri_object,
                                                                                comparison_dimitri_object)
        f, a = ts_comp.plot_temporal_ratio('reflectance', scipy.asarray([meris_bands, comparison_bands]).T, show=False)
        f.set_size_inches(15, 12)
        f.savefig(filename + '.png', dpi=200)