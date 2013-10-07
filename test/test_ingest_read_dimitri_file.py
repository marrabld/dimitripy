__author__ = 'marrabld'
import sys
import scipy

sys.path.append("../..")

import unittest
import dimitripy.ingest
import dimitripy.base


class TestDimitriIngestDimitriFiles(unittest.TestCase):
    def setUp(self):
        self.test_file = '/home/marrabld/projects/DIMITRI_2.0/Input/Site_DomeC/PARASOL/Proc_Calibration_1/PARASOL_TOA_REF.dat'

    def test_read_dimitri_sav_file(self):
        tmp_dict = dimitripy.ingest.DimitriFiles.read_dimitri_sav_file(self.test_file, 'PARASOL')

        # Test that we can use the dictionary to make a DimitriObject
        test_object = dimitripy.base.DimitriObject(tmp_dict)
        assert isinstance(test_object, dimitripy.base.DimitriObject)

        assert isinstance(tmp_dict, dict), True

    def test_read_dimitri_netcdf_file(self):
        tmp_dict = dimitripy.ingest.DimitriFiles.read_dimitri_netcdf_file(
            '/home/marrabld/projects/DIMITRI_2.0/Input/Site_DomeC/PARASOL/Proc_Calibration_1/DomeC_PARASOL_Proc_Calibration_1.nc')
        assert isinstance(tmp_dict, scipy.io.netcdf_file), True

    def test_read_dimitri_intercomparison_file(self):
        filename = '/home/marrabld/projects/DIMITRI_2.0/Output/DomeC_20130822_REF_MERIS_3rd_Reprocessing/RCAL_DomeC_VEGETATION_Calibration_1_REF_MERIS_3rd_Reprocessing.csv'
        tmp_dict = dimitripy.ingest.DimitriFiles.read_dimitri_intercomparison_file(filename)
        assert isinstance(tmp_dict[0], dict), True
        assert isinstance(tmp_dict[1], dict), True

        # Test that we can use the dictionary to make a DimitriObject
        test_object = dimitripy.base.DimitriObject(tmp_dict[0])
        test_object_2 = dimitripy.base.DimitriObject(tmp_dict[1])

        assert isinstance(test_object, dimitripy.base.DimitriObject)
        assert isinstance(test_object_2, dimitripy.base.DimitriObject)


if __name__ == '__main__':
    unittest.main()