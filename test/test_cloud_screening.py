__author__ = 'marrabld'

sys.path.append("../..")

import unittest
import libdimitripy.ingest
import libdimitripy.base
import libdimitripy.cloud_screening

import os
import Image
import scipy


class TestCKMethod(unittest.TestCase):
    def setUp(self):
        image_path = '../data/cloud_screening/cloudy-blue-sky.png'
        self.test_image = Image.open(image_path).convert('L')
        self.test_image = scipy.asarray(self.test_image)  # This should be np array
        self.ck_method = ####  Got to here!

    def test_define_training_images(self):
        pass

    def test_train_model(self):
        pass

    def test_process_image(self):
        pass