__author__ = 'marrabld'

import scipy
import sys
import logger as log
import libdimitripy.base
import scipy.linalg

DTYPE = libdimitripy.base.GLOBALS.DTYPE
DEBUG_LEVEL = libdimitripy.base.GLOBALS.DEBUG_LEVEL
lg = log.logger
lg.setLevel(DEBUG_LEVEL)
sys.path.append("../..")


class RoujeanBRDF():
    """
    Class for calculating the Roujean BRDF coefficients.
    """

    def __init__(self):
        pass

    def calc_kernel_f1(self, sun_zenith, sensor_zenith, relative_azimuth):
        """

        @param sun_zenith:
        @param sensor_zenith:
        @param relative_azimuth:
        @return:
        """

        # Just a bit of syntax candy
        # Do it in here so it goes out of scope after the method call
        cos = scipy.cos
        sin = scipy.sin
        tan = scipy.tan
        acos = scipy.arccos

        delta = scipy.sqrt(
            tan(sun_zenith) ** 2 + tan(sensor_zenith) ** 2 - 2 * tan(sensor_zenith) * tan(sun_zenith) * cos(
                relative_azimuth))

        kernel_f1 = 1 / (2.0 * scipy.pi) * ((
                                                (scipy.pi - relative_azimuth) * cos(relative_azimuth) + sin(
                                                    relative_azimuth)) * tan(sun_zenith) * tan(
            sensor_zenith))

        kernel_f1 -= (1 / scipy.pi) * (tan(sun_zenith) + tan(sensor_zenith) + delta)

        return kernel_f1

    def calc_kernel_f2(self, sun_zenith, sensor_zenith, relative_azimuth):
        """

        @param sun_zenith:
        @param sensor_zenith:
        @param relative_azimuth:
        @return:
        """

        # Just a bit of syntax candy
        # Do it in here so it goes out of scope after the method call
        cos = scipy.cos
        sin = scipy.sin
        tan = scipy.tan
        acos = scipy.arccos

        scatt_angle = acos(
            cos(sun_zenith) * cos(sensor_zenith) + sin(sun_zenith) * sin(sensor_zenith) * cos(relative_azimuth))
        kernel_f2 = (4 / (3 * scipy.pi)) * (1 / (cos(sun_zenith) + cos(sensor_zenith)))
        kernel_f2 *= ((scipy.pi / 2 - scatt_angle) * cos(scatt_angle) + sin(scatt_angle))
        kernel_f2 -= (1.0 / 3.0)

        return kernel_f2

    def calc_roujean_coeffs(self, sun_zenith, sensor_zenith, relative_azimuth, reflectance):
        """

        @param sun_zenith:
        @param sensor_zenith:
        @param relative_azimuth:
        @param reflectance:
        @return:
        """

        # Remove any values that have -999 for the reflectance.
        idx = reflectance != -999

        lg.debug('Calculating kernel functions')
        f_matrix = scipy.ones((reflectance[idx].shape[0], 3))  # There are 3 k_coeffs
        f_matrix[:, 1] = self.calc_kernel_f1(sun_zenith[idx], sensor_zenith[idx], relative_azimuth[idx])
        f_matrix[:, 2] = self.calc_kernel_f2(sun_zenith[idx], sensor_zenith[idx], relative_azimuth[idx])

        lg.debug('Inverting for K coeffs')
        try:
            #k_coeff = scipy.dot(f_matrix.T, f_matrix)
            #k_coeff = scipy.linalg.inv(k_coeff)
            #k_coeff = scipy.dot(k_coeff, f_matrix.T)
            #k_coeff = scipy.dot(k_coeff, reflectance.T)

            k_coeff, residual, rank, singular_values = scipy.linalg.lstsq(f_matrix, reflectance[idx].T)
        except:
            lg.exception("Couldn't find k_coeff setting to -999")
            k_coeff = scipy.asarray([-999, -999, -999])  # Right thing to do?
            residual = rank = singular_values = scipy.asarray([-999, -999, -999])

        return k_coeff.T, residual, rank, singular_values

    def model_brdf(self, sun_zenith, sensor_zenith, relative_azimuth, k_coeff):
        """

        @param sun_zenith:
        @param sensor_zenith:
        @param relative_azimuth:
        @param k_coeff:
        @return:
        """

        lg.debug('Calculating Roujean BRDF')
        brdf = k_coeff[0] + k_coeff[1] * self.calc_kernel_f1(sun_zenith, sensor_zenith, relative_azimuth) + \
               k_coeff[2] * self.calc_kernel_f2(sun_zenith, sensor_zenith, relative_azimuth)

        return brdf

    def model_brdf_timeseries(self, sun_zenith, sensor_zenith, relative_azimuth, reflectance, decimal_year, start_date,
                              end_date,
                              bin_days=20):
        """

        @param sun_zenith:
        @param sensor_zenith:
        @param relative_azimuth:
        @param reflectance:
        @param decimal_year:
        @param start_date:
        @param end_date:
        @param bin_days:
        @return:
        """

        #  TODO:  sort out resampling of and averaging of data here.

        if start_date < decimal_year[0]:
            start_date = decimal_year[0]
            lg.warning('Start date is before beginning of time series, setting to :: ' + str(start_date))

        if end_date > decimal_year[-1]:
            end_date = decimal_year[-1]
            lg.warning('End date is after end of the time series, setting to :: ' + str(end_date))

        bin_days /= 365.0  # now we are on decimal years.

        num_days = scipy.absolute((end_date - start_date))  # * 365.0)
        num_aquired = scipy.ceil(num_days / (bin_days))

        #  preallocate the arrays.
        k_coeff = scipy.zeros((num_aquired, 3))
        brdf = scipy.zeros(1)
        brdf_uncertainty_r = scipy.zeros(num_aquired)
        brdf_uncertainty_s = scipy.zeros(num_aquired)
        brdf_std = scipy.zeros(num_aquired)
        resampled_time = scipy.zeros(num_aquired)

        for i_iter in range(0, int(num_aquired)):
            #  Set the bound with in the bin period
            bin_start = start_date + (i_iter * bin_days)
            bin_stop = bin_start + bin_days
            bin_idx = ((bin_start < decimal_year) & (bin_stop > decimal_year))
            k_coeff[i_iter, :], residual, rank, singular_values = self.calc_roujean_coeffs(sun_zenith[bin_idx],
                                                                                           sensor_zenith[bin_idx],
                                                                                           relative_azimuth[bin_idx],
                                                                                           reflectance[bin_idx])
            #for j_iter in range(0, count(bin_idx)):
            temp = self.model_brdf(sun_zenith[bin_idx], sensor_zenith[bin_idx],
                                                       relative_azimuth[bin_idx],
                                                       k_coeff[i_iter, :])
            brdf = scipy.hstack((brdf, temp))
            #brdf[int(i_iter * bin_days):int(sun_zenith[bin_idx].shape[0])] = temp

            roujean_reflectance = scipy.mean(brdf)

            #  Calculate the error statistics
            #  Doing this the same as DIMITRIv2 for consistency
            roujean_diff = reflectance - roujean_reflectance
            brdf_std[i_iter] = scipy.std(roujean_diff)
            rmse = scipy.sqrt(scipy.sum(roujean_diff ** 2) / roujean_diff.shape[0])
            brdf_uncertainty_r[i_iter] = 3 * rmse
            brdf_uncertainty_s[i_iter] = rmse / scipy.sqrt(roujean_diff.shape[0])
            time = decimal_year[bin_idx]
            #mid_time = time[round(time.shape[0] / 2)]  # hopefully this grabs the middle value.
            mid_time = scipy.mean(time)  # TODO this in nonsense, fix tlater
            resampled_time[i_iter] = mid_time

        return k_coeff, resampled_time, brdf,  brdf_std, brdf_uncertainty_r, brdf_uncertainty_s


    def normalise_reflectance(self, sun_zenith, relative_azimuth, k_coeffs):
        """
        Normalises the reflectance to nadir given the roujean coefficients.

        @param reflectance:
        @param k_coeffs:
        @return:
        """

        sensor_zenith = scipy.zeros(sun_zenith.shape)

        return self.model_brdf(sun_zenith, sensor_zenith, relative_azimuth, k_coeffs)


    def save_coeffs(self, filename, k_coeff):
        """

        @param filename:
        @return:
        """
        lg.info('Writing k_coeffs to file :: ' + filename)
        scipy.savetxt(filename, k_coeff, delimiter=",")


    def calc_rho(self):
        pass