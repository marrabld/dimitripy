import copy

__author__ = 'marrabld'
import sys

sys.path.append("../")

import libdimitripy.ingest
import libdimitripy.base
import libdimitripy.brdf
import libdimitripy.post_processing_tool
import libdimitripy.helper_functions
import pylab
import scipy

#toa_file = '/home/marrabld/projects/DIMITRI_2.0/Input/Site_Libya4/MERIS/Proc_3rd_Reprocessing/MERIS_TOA_REF.dat'
#toa_file = '/home/marrabld/projects/DIMITRI_2.0/Input/Site_DomeC/MERIS/Proc_2nd_Reprocessing/MERIS_TOA_REF.dat'
#toa_file = '/home/marrabld/projects/DIMITRI_2.0/Input/Site_Amazon/MERIS/Proc_3rd_Reprocessing/MERIS_TOA_REF.dat'
#toa_file = '/home/marrabld/projects/DIMITRI_2.0/Input/Site_Uyuni/MERIS/Proc_3rd_Reprocessing/MERIS_TOA_REF.dat'
toa_file = '/home/marrabld/projects/DIMITRI_2.0/Input/Site_TuzGolu/MERIS/Proc_3rd_Reprocessing/MERIS_TOA_REF.dat'
filename = 'spoof'

#meris_bands = [4, 6, 12]
meris_bands = [0, 1, 2]
aatsr_bands = [0, 1, 2]
modisa_bands = [16, 20, 21]
parasol_bands = [2, 3, 6]
vgt_bands = [0, 1, 2]

comparison_bands = meris_bands

start_date = 2002.0
end_date = 2012.0
bin_days = 12
toa_band = meris_bands[2]

#plot_type = '1to1'
plot_type = 'time'

if plot_type == '1to1':
    tmp_dict = libdimitripy.ingest.DimitriFiles.read_dimitri_sav_file(toa_file, 'MERIS')

    # Test that we can use the dictionary to make a DimitriObject
    toa_object = libdimitripy.base.DimitriObject(tmp_dict)
    brdf = libdimitripy.brdf.RoujeanBRDF()

    k_coeff, resampled_time, brdf, brdf_std, brdf_uncertainty_r, brdf_uncertainty_s = brdf.model_brdf_timeseries(
        toa_object.sun_zenith,
        toa_object.sensor_zenith,
        toa_object.relative_azimuth(),
        toa_object.reflectance[:, toa_band],
        toa_object.decimal_year,
        start_date,
        end_date,
        bin_days)

    small_reflectance = toa_object.reflectance[0:brdf.shape[0], toa_band]
    idx = small_reflectance != -999

    fig_handle, ax_handle = pylab.subplots()
    pylab.plot(small_reflectance[idx], brdf[idx], '*', alpha=0.7)
    pylab.plot([0, 1], [0, 1], 'k--')
    pylab.xlabel('measured reflectance')
    pylab.ylabel('modelled reflectance')
    pylab.title('MERIS 865 nm')
    textstr = 'BRDF bin size :: ' + str(bin_days) + ' days'

    # these are matplotlib.patch.Patch properties
    #props = dict(boxstyle='round', facecolor='wheat', alpha=0.75)

    # place a text box in upper left in axes coords
    #ax_handle.text(0.05, 0.95, textstr, transform=ax_handle.transAxes, fontsize=14,
    #               verticalalignment='top', bbox=props)

    #pylab.show()
else:
    dimitri_dict = libdimitripy.ingest.DimitriFiles.read_dimitri_sav_file(toa_file, 'MERIS')
    comparison_dimitri_object = libdimitripy.base.DimitriObject(dimitri_dict)

    #reference_dimitri_object = libdimitripy.base.DimitriObject(dimitri_dict)  # going to spoof this to be brdf
    reference_dimitri_object = copy.deepcopy(comparison_dimitri_object)

    brdf = libdimitripy.brdf.RoujeanBRDF()

    idx = reference_dimitri_object.reflectance[:, toa_band] != -999
    tmp_size = reference_dimitri_object.decimal_year[idx].shape[0]

    #shape = reference_dimitri_object.reflectance.shape
    modelled_brdf = scipy.zeros(tmp_size)
    tmp_brdf = scipy.zeros(tmp_size)

    for i_iter in range(0, reference_dimitri_object.reflectance.shape[1]):
        k_coeff, resampled_time, tmp_brdf, brdf_std, brdf_uncertainty_r, brdf_uncertainty_s = brdf.model_brdf_timeseries(
            reference_dimitri_object.sun_zenith,
            reference_dimitri_object.sensor_zenith,
            reference_dimitri_object.relative_azimuth(),
            reference_dimitri_object.reflectance[:, toa_band],
            reference_dimitri_object.decimal_year,
            start_date,
            end_date)

        #print(modelled_brdf.shape)
        idx = reference_dimitri_object.reflectance[:, toa_band] != -999
        reference_dimitri_object.reflectance[:, i_iter][idx] = tmp_brdf

    #    modelled_brdf = scipy.vstack((modelled_brdf, tmp_brdf))

    #  first get the coincident decimal_dates


    reference_dimitri_object.decimal_year = reference_dimitri_object.decimal_year[idx]
    reference_dimitri_object.sun_zenith = reference_dimitri_object.sun_zenith[idx]
    reference_dimitri_object.sensor_zenith = reference_dimitri_object.sensor_zenith[idx]
    reference_dimitri_object.bands = ['560', '665', '865']

    reference_dimitri_object.reflectance = reference_dimitri_object.reflectance.T
    comparison_dimitri_object.reflectance = comparison_dimitri_object.reflectance.T

    ts_comp = libdimitripy.post_processing_tool.TimeSeriesIntercomparison(reference_dimitri_object,
                                                                          comparison_dimitri_object)

    f, a = ts_comp.plot_temporal_ratio('reflectance', scipy.asarray([meris_bands, comparison_bands]).T, show=False)
    f.set_size_inches(15, 12)
    f.savefig(filename + '.png', dpi=200)




