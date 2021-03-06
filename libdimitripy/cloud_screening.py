from scipy.optimize import optimize

__author__ = 'marrabld'

import scipy
import scipy.linalg
import scipy.signal
import os
import sys
import logger as log
import libdimitripy.base
import scipy.ndimage
import ConfigParser
import pickle
import libdimitripy.brdf

DTYPE = libdimitripy.base.GLOBALS.DTYPE
DEBUG_LEVEL = libdimitripy.base.GLOBALS.DEBUG_LEVEL
lg = log.logger
lg.setLevel(DEBUG_LEVEL)
config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'configuration.conf')
config = ConfigParser.ConfigParser()
config.read(config_file)

sys.path.append("../..")


class CKMethod():
    """
    This class implements the Chis Kent (<date>) method of checking for cloud cover in an image.

    Training stage:

    Firstly a training set of images is selected such that images can be classified into three groups and defined as:
    clear-sky, part-cloud or full-cloud.  A curve of how mean and standard deviation change with increasing resolution
    is produced for all of the training images.  This procedure is defined below.

    A low resolution is defined defined that is 2 x 2 pixels.  The scene is interpolated to the new resolution and
    average and standard deviation of the TOA value over those pixels is calculated.  The resolution size is increased
    until the averaging window is the same resolution as the scene.  The mean and standard deviation is calculated for
    each resolution as shown below.

    (m,n,)= 1(m  n)j=1ni=1mi,j()

    (m,n,)=1(n  m)j=1ni=1mi,j()- (m,n,)2

    {mZ | 1 < m  window length}
    {n Z | 1 < n  window width}

    A power law approximation for the changing variability is computed and the gradient of the slope compared against a
    set of defined thresholds.

    (m,n,)Ax()k

    Where A is the linear scaling factor and k is the slope factor.  Both A and k will be found using least-square
    regression.

    """

    def __init__(self):
        """

        """
        self.clear_images = ''
        self.partly_cloudy_images = ''
        self.cloudy_images = ''


    def define_training_images(self, clear_images, partly_cloudy_images, cloudy_images):
        """
        Can be used instead of the constructor.  Essentially does the same thing.  API candy

        :param clear_images: 3D array of clear sky images
        :param partly_cloudy_images: 3D array of partly cloudy images
        :param cloudy_images: 3D array of cloudy images
        :return:
        """

        self.clear_images = scipy.asarray(clear_images)
        self.partly_cloudy_images = scipy.asarray(partly_cloudy_images)
        self.cloudy_images = scipy.asarray(cloudy_images)

    def train_model(self, update_cache=True):
        """

        Model is A*x**b) where model [A, b]

        :return:
        """

        clear_model = scipy.zeros((1, 2), dtype=DTYPE)  # initialise an empty vector
        partly_cloudy_model = scipy.zeros((1, 2), dtype=DTYPE)
        cloudy_model = scipy.zeros((1, 2), dtype=DTYPE)

        models = [clear_model, partly_cloudy_model, cloudy_model]
        images = [self.clear_images, self.partly_cloudy_images, self.cloudy_images]

        ##########
        #  interpolate the image to a 2x2 image and calculate stats
        #  repeat while increasing the interpolation size up to the original size.
        ##########

        for i_iter, model in enumerate(models):
            #for image in images:
            mean, std, window = self.process_image(images[i_iter])
            tmp_model = self.fit_model(window, std)
            model = scipy.vstack([model, tmp_model])

            ##########
            #  model should be a vstacked pair of values.
            #  average through them and use the average value as the trained value
            ##########

            if i_iter == 0:
                clear_model = scipy.mean(model, axis=0)
            elif i_iter == 1:
                partly_cloudy_model = scipy.mean(model, axis=0)
            elif i_iter == 2:
                cloudy_model = scipy.mean(model, axis=0)
            else:
                lg.error('Error training model, model enumeration > 3')

        if update_cache:
            config.set('cloud_screening_ckmethod', 'a_clear_model', clear_model[0])
            config.set('cloud_screening_ckmethod', 'b_clear_model', clear_model[1])
            config.set('cloud_screening_ckmethod', 'a_partly_cloudy_model', partly_cloudy_model[0])
            config.set('cloud_screening_ckmethod', 'b_partly_cloudy_model', partly_cloudy_model[1])
            config.set('cloud_screening_ckmethod', 'a_cloudy_model', cloudy_model[0])
            config.set('cloud_screening_ckmethod', 'b_cloudy_model', cloudy_model[1])
            lg.debug(config.write(sys.stdout))
            pickle_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'cache/ck_cloud.p')
            print(pickle_file)
            pickle.dump([clear_model, partly_cloudy_model, cloudy_model],
                        open(pickle_file, "wb"))
            #config.write()

        return [clear_model, partly_cloudy_model, cloudy_model]


    def process_image(self, image):
        """


        :rtype : object
        :param image:
        :return:
        """
        image_size = image.shape
        image_mean = scipy.zeros(1, dtype=DTYPE)
        image_std = scipy.zeros(1, dtype=DTYPE)

        ##########
        #  resample the image to a 2x2 image and calculate stats
        #  repeat while increasing the interpolation size up to the original size.
        ##########

        for i_iter in range(1, image_size[0]):  # this will likely only work for square images for now.  TODO fix
            zoom_factor = float(i_iter) / float(image_size[0])  # square only
            interp_image = scipy.ndimage.zoom(image, zoom_factor)
            image_mean = scipy.hstack((image_mean, scipy.mean(interp_image)))
            image_std = scipy.hstack((image_std, scipy.std(interp_image)))

        window_size = scipy.linspace(0, image_size[0] - 2, image_size[0] - 2)

        ## work around, trim the starting zero from the beginning.
        image_mean = image_mean[2:]
        image_std = image_std[2:]


        # zero scale the vectors
        image_mean = image_mean - min(image_mean)
        image_std = image_std - min(image_std)
        image_mean = scipy.signal.medfilt(image_mean, 3)
        image_std = scipy.signal.medfilt(image_std, 3)

        #!!!! for testing
        import pylab

        pylab.plot(window_size, image_std)
        pylab.show()

        return image_mean, image_std, window_size

    def fit_model(self, std, window_size):
        """

        TODO kwargs the initial guesses

        :return:
        """
        lg.debug('Fitting curve, CKMethod')
        x = window_size
        y = std

        fitfunc = lambda p, x: p[0] * x ** p[1]  # Target function
        errfunc = lambda p, x, y: scipy.absolute(fitfunc(p, x) - y)  # Distance to the target function
        p0 = [1, 1]  # Initial guess for the parameters
        p1, success = scipy.optimize.leastsq(errfunc, p0[:], args=(x, y))
        lg.info('Fit success = ' + str(success))
        lg.debug('[A, b] : ' + str(p1))
        if success == 5:
            lg.error('Fit not found!!')

        return p1


    def score_image(self, image):
        """
        This finds whether the image is cloudy or not.

        :param image:
        :return:
        """

        pickle_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'cache/ck_cloud.p')

        # Load the cloud thresholds
        [cloudy_model, partly_cloudy_model, clear_model] = pickle.load(open(pickle_file, "rb"))

        mean, std, window_size = self.process_image(image)
        p = self.fit_model(window_size, std)
        #p = self.fit_model(window_size, mean)

        # rebuild the functions of the window range,
        # find the residual vector and then the euclidean norm.
        # the one with the smallest should be the model.

        fitfunc = lambda p, x: p[0] * x ** p[1]

        clear_residual = scipy.absolute(fitfunc(p, window_size) - fitfunc(clear_model, window_size))
        pc_residual = scipy.absolute(fitfunc(p, window_size) - fitfunc(partly_cloudy_model, window_size))
        cloudy_residual = scipy.absolute(fitfunc(p, window_size) - fitfunc(cloudy_model, window_size))

        clear_residual[scipy.isinf(clear_residual)] = 0.0
        clear_residual[scipy.isnan(clear_residual)] = 0.0
        pc_residual[scipy.isinf(pc_residual)] = 0.0
        pc_residual[scipy.isnan(pc_residual)] = 0.0
        cloudy_residual[scipy.isinf(cloudy_residual)] = 0.0
        cloudy_residual[scipy.isnan(cloudy_residual)] = 0.0

        clear_norm = scipy.linalg.norm(clear_residual)
        pc_norm = scipy.linalg.norm(pc_residual)
        cloudy_norm = scipy.linalg.norm(cloudy_residual)

        smallest_val = [clear_norm, pc_norm, cloudy_norm].index(min([clear_norm, pc_norm, cloudy_norm]))
        lg.debug('score :: ' + str(smallest_val))

        return smallest_val


    def find_nearest(self, a, a0):
        idx = scipy.abs(a - a0).argmin()
        return a.flat[idx]


class BRDFMethod():
    def __init__(self):
        #self.clear_image_object = ''  # list of Dimitiri objects that are clear sky.
        self.brdf = libdimitripy.brdf.RoujeanBRDF()


    def train_model(self, image_object, update_cache=True):
        """
        Calculates the Roujean k coefficients for the BRDF model based on the clear sky images.
        Saves the k coeffs to the cache for later use

        @return:
        """
        lg.debug('Training model for BRDFMethod of cloud screening')

        k_coeffs, residual, rank, singular_values = self.brdf.calc_roujean_coeffs(image_object.sun_zenith,
                                                                                  image_object.sensor_zenith,
                                                                                  image_object.relative_azimuth(),
                                                                                  image_object.reflectance)

        if update_cache:
            pickle_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'cache/brdf_cloud.p')
            pickle.dump(k_coeffs, open(pickle_file, "wb"))

        return k_coeffs

    def calc_brdf_modelled_reflectance(self, image_object, k_coeffs):
        """
        For the list of images, calculate the modelled reflectance using the Roujean coefficients

        @param image_object:
        :param k_coeffs:
        @return:
        """
        lg.debug('Calculating modelled reflectance')

        brdf_ref = self.brdf.model_brdf(image_object.sun_zenith, image_object.sensor_zenith,
                                        image_object.relative_azimuth(), k_coeffs)

        return brdf_ref

    def score_images(self, reflectance, modelled_reflectance, threshold=0.1):
        """
        Compare the modelled reflectance with the measured reflectance.  score them as cloudy or not
        based on the threshold

        @param reflectance:
        @param modelled_reflectance:
        @param threshold:
        @return idx:
        """

        diff = reflectance - modelled_reflectance
        idx = (diff <= (threshold * -1.0)) | (diff >= threshold)

        return idx
