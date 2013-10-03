__author__ = 'marrabld'
import sys
import scipy

sys.path.append("../..")

import unittest
import dimitripy.ingest


class TestDimitriIngestDimitriFiles(unittest.TestCase):
    def setUp(self):
        self.test_file = '/home/marrabld/projects/DIMITRI_2.0/Input/Site_DomeC/PARASOL/Proc_Calibration_1/PARASOL_TOA_REF.dat'

    def test_read_dimitri_sav_file(self):
        tmp_dict = dimitripy.ingest.DimitriFiles.read_dimitri_sav_file(self.test_file, 'PARASOL')
        assert isinstance(tmp_dict, dict), True

    def test_read_dimitri_netcdf_file(self):
        tmp_dict = dimitripy.ingest.DimitriFiles.read_dimitri_netcdf_file('/home/marrabld/projects/DIMITRI_2.0/Input/Site_DomeC/PARASOL/Proc_Calibration_1/DomeC_PARASOL_Proc_Calibration_1.nc')
        assert isinstance(tmp_dict, scipy.io.netcdf_file), True


if __name__ == '__main__':
    unittest.main()