__author__ = 'marrabld'
import sys

sys.path.append("../..")

import os

print(os.getcwd())
import unittest
import dimitripy.ingest
import dimitripy.base
import dimitripy.post_processing_tool
import scipy


class TestTimeSeriesIntercomparison(unittest.TestCase):
    def setUp(self):
        directory = '/home/marrabld/projects/DIMITRI_2.0/Output/DomeC_20130417_REF_MERIS_3rd_Reprocessing'
        filename = 'ED_DomeC_MERIS_3rd_Reprocessing_PARASOL_Calibration_1.csv'
        tmp_dict = dimitripy.ingest.DimitriFiles.read_dimitri_intercomparison_file(os.path.join(directory, filename))

        self.reference_dimitri_object = dimitripy.base.DimitriObject(tmp_dict[0])
        self.comparison_dimitri_object = dimitripy.base.DimitriObject(tmp_dict[1])
        self.ts_comp = dimitripy.post_processing_tool.TimeSeriesIntercomparison(self.reference_dimitri_object,
                                                                                self.comparison_dimitri_object)

    def test_plot_temporal_ratio(self):
        #self.ts_comp.plot_temporal_ratio('reflectance', 0)
        self.ts_comp.plot_temporal_ratio('reflectance', scipy.asarray([[4, 6, 12], [2, 3, 6]]).T)

    def test_plot_temporal_parameter(self):
        self.ts_comp.plot_temporal_parameter('reflectance', 0, dimitri_object='reference')
        self.ts_comp.plot_temporal_parameter('reflectance', 0, dimitri_object='comparison')

