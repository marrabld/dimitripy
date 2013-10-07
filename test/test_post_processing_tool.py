__author__ = 'marrabld'
import sys

sys.path.append("../..")

import os
print(os.getcwd())
import unittest
import dimitripy.ingest
import dimitripy.base
import dimitripy.post_processing_tool


class TestTimeSeriesIntercomparison(unittest.TestCase):
    def setUp(self):
        filename = '/home/marrabld/projects/DIMITRI_2.0/Output/DomeC_20130822_REF_MERIS_3rd_Reprocessing/RCAL_DomeC_VEGETATION_Calibration_1_REF_MERIS_3rd_Reprocessing.csv'
        tmp_dict = dimitripy.ingest.DimitriFiles.read_dimitri_intercomparison_file(filename)

        self.reference_dimitri_object = dimitripy.base.DimitriObject(tmp_dict[0])
        self.comparison_dimitri_object = dimitripy.base.DimitriObject(tmp_dict[1])

    def test_plot_temporal_ratio(self):
        dimitripy.post_processing_tool.plot_temporal_ratio(self.reference_dimitri_object,
                                                           self.comparison_dimitri_object)
