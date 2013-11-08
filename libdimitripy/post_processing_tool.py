__author__ = 'marrabld'

import scipy
import scipy.stats
from matplotlib.ticker import FormatStrFormatter
import sys
import matplotlib.pyplot as plt
import logger as log
import libdimitripy.base

DTYPE = libdimitripy.base.GLOBALS.DTYPE
DEBUG_LEVEL = libdimitripy.base.GLOBALS.DEBUG_LEVEL
lg = log.logger
lg.setLevel(DEBUG_LEVEL)
sys.path.append("../..")


class TimeSeriesIntercomparison():
    """
    USed for Intercomparing simulated reflectances with actual reflectances.  Class requires 2 DimitriObjects.  Once refered to as the reference object and
    one referred to as the comparison object.  These should be passed through the constructor (reference, comparison).  The reference sensor is always used
    as the first in any list.
    """

    def __init__(self):
        self.reference_object = None
        self.comparison_object = None

    def __init__(self, reference_dimitri_object, comparison_dimitri_object):
        self.reference_object = reference_dimitri_object
        self.comparison_object = comparison_dimitri_object

    def plot_temporal_ratio(self, parameter, band, show=True, outlier_filter=2, sza_filter=65, time='all',
                            ylim=[-20, 20], **kwargs):
        """
        Produces plots of the desired parameter by comparing a comparison dimitri object
        with a reference object.  The band input parameter must be an int or a 2D Numpy array
        where the rows are the band numbers to compare and the columns are the reference and comparison bands
        respectively.  If more than one row are parsed, they will be subplotted on the same figure window.

        :param parameter: <string> DimitriObject parameter to compare (currently only reflectance is tested)
        :param band: <Numpy int> or <2D Numpy array> Numpy array with the bands to compare asarray([[reference], [comparison]])
        :param show: <bool> if set to true figure will be displayed on the screen TODO add save as option
        :param outlier_filter: <float> The number of standard deviations to filter out of the TOA ratio
        :param sza_filter: <float> Any data points greater than this angle will be filtered out.
        :param time: not used atm
        :return figure_handle, axes_handle: <matplotlib>  Can be used to change the plot parameters.
        """

        decimal_year = scipy.asarray(self.reference_object['decimal_year'], dtype=DTYPE)
        reference_sza = scipy.asarray(self.reference_object['sun_zenith'], dtype=DTYPE)
        fig_handle, ax_handle = plt.subplots()

        ##########
        # get kwargs and set defaults
        ##########
        ylim = ylim

        ##########
        # If only 1D, compare same band numbers
        ##########
        if band.ndim < 2:
            lg.info('One band found, using for both')
            start = 0
            end = len(decimal_year)

            toa_ratio = self.comparison_object[parameter][band, start:end] / self.reference_object[parameter][band,
                                                                             start:end]
            ax_handle.plot(decimal_year, toa_ratio, '*')

            ##########
            # draw the middle line around 1.
            ##########
            y = [1, 1]
            x = [decimal_year[0], decimal_year[-1]]
            plt.plot(x, y, 'r--')

            ##########
            # Set the default plot parameters
            ##########
            plt.xlabel('Decimal Year')
            plt.ylabel(r'$\frac{R}{R_{ref}}$')
            plt.title(self.reference_object.bands[band] + ' nm')

        ##########
        # If 2D, compare one band column with the corresponding column
        ##########
        elif band.ndim > 1:
            lg.debug('Found Band pairs')
            start = 0
            end = len(decimal_year)

            for b_iter in range(0, band.shape[0]):
                sub_num = int(str(band.shape[0]) + '1' + str(b_iter + 1))
                ax_handle = plt.subplot(sub_num)
                toa_ratio = (self.comparison_object[parameter][band[b_iter, 1], start:end] - self.reference_object[
                                                                                                 parameter][
                                                                                             band[b_iter, 0],
                                                                                             start:end]) / \
                            self.reference_object[parameter][band[b_iter, 0], start:end]
                toa_ratio[scipy.isinf(toa_ratio)] = 0
                toa_ratio *= 100  # Make it percentage

                ##########
                # draw the middle line around 1.
                ##########
                #y = [1, 1]
                #x = [decimal_year[0], decimal_year[-1]]
                #plt.plot(x, y, 'k--')

                ##########
                # Find the mean and standard deviation of the toa_ratio and add it to he legend
                ##########
                lg.debug('finding stats of TOA')
                mean_toa_ratio = scipy.mean(toa_ratio)
                std_toa_ratio = scipy.std(toa_ratio)

                #########
                #  Filter out any outliers that deviate more or less than defined by the method input parameter
                #########
                lg.debug(
                    'Filtering data based on filter parameters :: <sigma>, <sza> :: ' + str(
                        outlier_filter) + ', ' + str(
                        sza_filter))
                lg.debug(
                    'Of Band pair <reference>, <comparison>:: ' + str(band[b_iter, 0]) + ', ' + str(band[b_iter, 1]))
                filter_index = (toa_ratio > (mean_toa_ratio - std_toa_ratio * outlier_filter)) & (toa_ratio < (
                    mean_toa_ratio + std_toa_ratio * outlier_filter))

                filtered_decimal_year = decimal_year[filter_index]
                toa_ratio = toa_ratio[filter_index]
                filtered_reference_sza = reference_sza[filter_index]  # Keep these the same size

                #########
                #  Filter out any data points that lie outside the sza_filter value.
                #########
                filter_index = (filtered_reference_sza < sza_filter)
                filtered_decimal_year = filtered_decimal_year[filter_index]
                toa_ratio = toa_ratio[filter_index]
                filtered_reference_sza = filtered_reference_sza[filter_index]

                ##########
                # Fit a curve (linear fit)
                ##########
                slope, intercept, r_value, p_value, std_error = scipy.stats.linregress(filtered_decimal_year, toa_ratio)

                textstr = 'Yearly drift = %.2f %% $\mathrm{year^{-1} \pm}$ %.2f %% $\mathrm{ \,  year^{-1}}$ (%.0f$\sigma$) \n Mean difference = %.2f %% (%.0f$\sigma$ = %.2f %%)' % (
                    slope, std_error, outlier_filter, mean_toa_ratio, outlier_filter, std_toa_ratio)

                # these are matplotlib.patch.Patch properties
                props = dict(boxstyle='round', facecolor='wheat', alpha=0.75)

                # place a text box in upper left in axes coords
                ax_handle.text(0.05, 0.95, textstr, transform=ax_handle.transAxes, fontsize=14,
                               verticalalignment='top', bbox=props)

                ##########
                # Set the default plot parameters
                ##########
                plt.title(str(self.reference_object.bands[band[b_iter, 0]]) + ' nm')
                #plt.ylabel(r'$\frac{' + self.comparison_object['sensor_name'] + '-' + self.reference_object[
                #    'sensor_name'] + '}{' + self.reference_object['sensor_name'] + '}$' + '% of TOA reflectance')
                plt.ylabel(r'$\frac{' + self.comparison_object['sensor_name'] + '-' + 'BRDF' + '}{' + 'BRDF' + '}$' + '% of TOA reflectance')
                ax_handle.plot(filtered_decimal_year, toa_ratio, '*')
                ax_handle.xaxis.set_major_formatter(FormatStrFormatter('%1.1f'))
                #ax_handle.set_ylim(ylim)

            plt.xlabel('Decimal Year')

        else:
            lg.exception("couldn't find useable Band information")
            raise

        if show:
            plt.show()

        return fig_handle, ax_handle

    def plot_temporal_parameter(self, parameter, band, dimitri_object='reference', show=True, time='all'):
        """
        Produces plots of the desired parameter over the time series of DimitriObject  TODO, Add ability to subplot with
        more bands.

        :param parmeter: <string> DimitriObject parameter to compare (currently only reflectance is tested)
        :param band: <int> The band number to plot
        :param dimitri_object: <string> The object to plot.  Either reference or comparison.  This is because the class holds both
        :param time: <string> Not used
        :return fig_handle: <matplotlib>  Can be used to change the plot parameters.
        """

        ##########
        # Check which DimitriObject to plot
        ##########
        if dimitri_object == 'reference':
            fig_handle = plt.plot(self.reference_object.decimal_year, self.reference_object[parameter][band, :], '*')
        elif dimitri_object == 'comparison':
            fig_handle = plt.plot(self.comparison_object.decimal_year, self.comparison_object[parameter][band, :], '*')
        else:
            lg.exception('KeyError :: Expect \'reference or comparison\' ')
            raise KeyError(parameter)

        ##########
        # Set the default plot parameters
        ##########
        plt.xlabel('Decimal Year')
        plt.ylabel('$TOA \, Reflectance \, sr^{-1}$')
        plt.title(self.reference_object.bands[band] + ' nm')

        if show:
            plt.show()

        return fig_handle
