from matplotlib.ticker import FormatStrFormatter

__author__ = 'marrabld'

import sys
import matplotlib.pyplot as plt
import logger as log

lg = log.logger
sys.path.append("..")


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

    def plot_temporal_ratio(self, parameter, band, show=True, time='all'):
        """
        Produces plots of the desired parameter by comparing a comparison dimitri object
        with a reference object.  The band input parameter must be an int or a 2D Numpy array
        where the rows are the band numbers to compare and the columns are the reference and comparison bands
        respectively.  If more than one row are parsed, they will be subplotted on the same figure window.

        :param parameter: <string> DimitriObject parameter to compare (currently only reflectance is tested)
        :param band: <Numpy int> or <2D Numpy array> Numpy array with the bands to compare asarray([[reference], [comparison]])
        :param show: <bool> if set to true figure will be displayed on the screen TODO add save as option
        :param time: not used atm
        :return figure_handle, axes_handle: <matplotlib>  Can be used to change the plot parameters.
        """

        decimal_year = self.reference_object['decimal_year']
        fig_handle, ax_handle = plt.subplots()

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
            lg.info('Found Band pairs')
            start = 0
            end = len(decimal_year)

            for b_iter in range(0, band.shape[0]):
                sub_num = int(str(band.shape[0]) + '1' + str(b_iter + 1))
                ax_handle = plt.subplot(sub_num)
                toa_ratio = self.comparison_object[parameter][band[b_iter, 1], start:end] / self.reference_object[
                                                                                                parameter][
                                                                                            band[b_iter, 0], start:end]
                ##########
                # draw the middle line around 1.
                ##########
                y = [1, 1]
                x = [decimal_year[0], decimal_year[-1]]
                plt.plot(x, y, 'r--')

                ##########
                # Set the default plot parameters
                ##########
                plt.title(self.reference_object.bands[band[b_iter, 0]] + ' nm')
                plt.ylabel(r'$\frac{R}{R_{ref}}$')
                ax_handle.plot(decimal_year, toa_ratio, '*')
                ax_handle.xaxis.set_major_formatter(FormatStrFormatter('%1.1f'))

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
