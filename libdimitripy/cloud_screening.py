from scipy.optimize import optimize

__author__ = 'marrabld'

import scipy
import os
import sys
import logger as log
import libdimitripy.base
import scipy.ndimage
import ConfigParser

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

        @param clear_images: 3D array of clear sky images
        @param partly_cloudy_images: 3D array of partly cloudy images
        @param cloudy_images: 3D array of cloudy images
        @return:
        """

        self.clear_images = scipy.asarray(clear_images)
        self.partly_cloudy_images = scipy.asarray(partly_cloudy_images)
        self.cloudy_images = scipy.asarray(cloudy_images)

    def train_model(self, update_config=True):
        """

        Model is A*exp(b) where model [A, b]

        @return:
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

        if update_config:
            config.set('cloud_screening_ckmethod', 'a_clear_model', cloudy_model[0])
            config.set('cloud_screening_ckmethod', 'b_clear_model', cloudy_model[1])
            config.set('cloud_screening_ckmethod', 'a_partly_cloudy_model', partly_cloudy_model[0])
            config.set('cloud_screening_ckmethod', 'b_partly_cloudy_model', partly_cloudy_model[1])
            config.set('cloud_screening_ckmethod', 'a_cloudy_model', cloudy_model[0])
            config.set('cloud_screening_ckmethod', 'b_cloudy_model', cloudy_model[1])
            lg.debug(config.write(sys.stdout))
            config.write()

        return [clear_model, partly_cloudy_model, cloudy_model]


    def process_image(self, image):
        """


        @rtype : object
        @param image:
        @return:
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

        window_size = scipy.linspace(0, image_size[0], image_size[0])
        return image_mean, image_std, window_size

    def fit_model(self, std, window_size):
        """

        TODO kwargs the initial guesses

        @return:
        """
        lg.debug('Fitting curve, CKMethod')
        x = window_size
        y = std

        fitfunc = lambda p, x: p[0] * x ** p[1]  # Target function
        errfunc = lambda p, x, y: fitfunc(p, x) - y  # Distance to the target function
        p0 = [10, 1]  # Initial guess for the parameters
        p1, success = scipy.optimize.leastsq(errfunc, p0[:], args=(x, y))
        lg.info('Fit success = ' + str(success))
        if success == 5:
            lg.error('Fit not found!!')

        return p1


    def score_image(self, image):
        pass

