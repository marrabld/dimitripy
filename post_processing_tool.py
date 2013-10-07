__author__ = 'marrabld'

import sys
import pylab

sys.path.append("..")

import dimitripy.base


class TimeSeriesIntercomparison():
    """
    USed for Intercomparing simulated reflectances with actual reflectances
    """
    def __init__(self):
        self.reference_object = None
        self.comparison_object = None

    def __init__(self, reference_dimitri_object, comparison_dimitri_object):
        self.reference_object = reference_dimitri_object
        self.comparison_object = comparison_dimitri_object

    def plot_temporal_ratio(self, parameter, band, time='all'):
        """

        @param parameter:
        @param band:
        @param time:
        @return:
        """

        #if parameter == 'reflectance':
        toa_ratio = self.comparison_object[parameter][band, :] / self.reference_object[parameter][band, :]
        pylab.plot(toa_ratio, self.reference_object['decimal_time'])
        pylab.show()



