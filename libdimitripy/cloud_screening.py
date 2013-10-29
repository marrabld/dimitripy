__author__ = 'marrabld'

import scipy
import scipy.stats
import sys
import logger as log
import libdimitripy.base
import scipy.ndimage

DTYPE = libdimitripy.base.GLOBALS.DTYPE
DEBUG_LEVEL = libdimitripy.base.GLOBALS.DEBUG_LEVEL
lg = log.logger
lg.setLevel(DEBUG_LEVEL)
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

    def __init__(self, clear_images, partly_cloudy_images, cloudy_images):
        """
        Optional constructor


        @param clear_images: 3D array of clear sky images
        @param partly_cloudy_images: 3D array of partly cloudy images
        @param cloudy_images: 3D array of cloudy images
        @return:
        """
        pass

    def define_training_images(self, clear_images, partly_cloudy_images, cloudy_images):
        """
        Can be used instead of the constructor.  Essentially does the same thing.  API candy

        @param clear_images: 3D array of clear sky images
        @param partly_cloudy_images: 3D array of partly cloudy images
        @param cloudy_images: 3D array of cloudy images
        @return:
        """

    def train_model(self):
        """

        Model is A*exp(b) where model [A, b]

        @return:
        """

        clear_model = scipy.zeros(1, 1)  # initialise an empty vector
        partly_cloudy_model = scipy.zeros(1, 1)
        cloudy_model = scipy.zeros(1, 1)

        models = [clear_model, partly_cloudy_model, cloudy_model]
        images = [self.clear_images, self.partly_cloudy_images, self.cloudy_images]

        ##########
        #  interpolate the image to a 2x2 image and calculate stats
        #  repeat while increasing the interpolation size up to the original size.
        ##########

        for model in models:
            for image in images:
                model = scipy.hstack([model, self.process_image(image)])


    def process_image(self, image):
        """

        @param image:
        @return:
        """
        image_size = image.shape
        image_mean = scipy.zeros(1)
        image_std = scipy.zeros(1)

        ##########
        #  resample the image to a 2x2 image and calculate stats
        #  repeat while increasing the interpolation size up to the original size.
        ##########

        for i_iter in range(0, image_size[0] - 1):  # this will likely only work for square images for now.  TODO fix
            zoom_factor = 1 / (image_size[0] - i_iter)  # square only
            interp_image = scipy.ndimage.zoom(image, zoom_factor)
            image_mean = scipy.hstack(image_mean, scipy.mean(interp_image))
            image_std = scipy.hstack(image_std, scipy.std(interp_image))

        return image_mean, image_std


    def score_image(self, image):
        pass

