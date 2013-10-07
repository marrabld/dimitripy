__author__ = 'marrabld'

import sys
import pylab

sys.path.append("..")
import scipy

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

    def plot_temporal_ratio(self, parameter, band, show=True, time='all'):
        """

        @param parameter:
        @param band:
        @param time:
        @return:
        """
        decimal_year = self.reference_object['decimal_year']

        start = 0
        end = len(decimal_year)

        toa_ratio = self.comparison_object[parameter][band, start:end] / self.reference_object[parameter][band, start:end]
        pylab.plot(decimal_year, toa_ratio, '*')
        if show:
            pylab.show()

        # TODO return figure handle

    def plot_temporal_parameter(self, parameter, band, dimitri_object='reference',  show=True, time='all'):
        """

        @param parmeter:
        @param band:
        @param time:
        @return:
        """

        if dimitri_object == 'reference':
            pylab.plot(self.reference_object.decimal_year, self.reference_object[parameter][band, :], '*')
        elif dimitri_object == 'comparison':
            pylab.plot(self.comparison_object.decimal_year, self.comparison_object[parameter][band, :], '*')
        else:
            raise KeyError(parameter)

        if show:
            pylab.show()




