__author__ = 'marrabld'
import sys

sys.path.append("../..")

import unittest
import libdimitripy.ingest
import libdimitripy.base
import libdimitripy.cloud_screening

import os
import Image
import scipy
import pylab


class TestCKMethod(unittest.TestCase):
    def setUp(self):
        image_path = '/home/marrabld/projects/dimitripy/test/data/cloud_screening/cloudy-blue-sky.jpg'
        self.test_image = Image.open(image_path).convert('L')
        self.test_image = scipy.asarray(self.test_image)  # This should be np array

        cloudy_image = '/home/marrabld/projects/dimitripy/test/data/cloud_screening/cloudy-sky.jpg'
        self.cloudy_image = Image.open(cloudy_image).convert('L')
        self.cloudy_image = scipy.asarray(self.cloudy_image)

        partly_cloudy_image = '/home/marrabld/projects/dimitripy/test/data/cloud_screening/cloudy-blue-sky.jpg'
        self.partly_cloudy_image = Image.open(partly_cloudy_image).convert('L')
        self.partly_cloudy_image = scipy.asarray(self.partly_cloudy_image)

        clear_image = '/home/marrabld/projects/dimitripy/test/data/cloud_screening/clear-blue-sky.jpg'
        self.clear_image = Image.open(clear_image).convert('L')
        self.clear_image = scipy.asarray(self.clear_image)

        self.ck_method = libdimitripy.cloud_screening.CKMethod()


    def test_define_training_images(self):
        self.ck_method.define_training_images(self.clear_image, self.partly_cloudy_image, self.cloudy_image)

    def test_train_model(self):
        self.ck_method.define_training_images(self.clear_image, self.partly_cloudy_image, self.cloudy_image)
        [a, b, c] = self.ck_method.train_model()

    #def test_process_image(self):
    #    m, s, w = self.ck_method.process_image(self.test_image)
    #    p = self.ck_method.fit_model(w, s)

    #    print(p)

    def test_score_image(self):
        score = self.ck_method.score_image(self.clear_image)
        self.assertEquals(score, 0)
        score = self.ck_method.score_image(self.partly_cloudy_image)
        self.assertEquals(score, 1)
        score = self.ck_method.score_image(self.cloudy_image)
        self.assertEquals(score, 2)


