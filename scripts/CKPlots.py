import pickle

__author__ = 'marrabld'
import sys

sys.path.append("../..")

import libdimitripy.ingest
import libdimitripy.base
import libdimitripy.cloud_screening

import os
import Image
import scipy
import pylab

#image_path = '/home/marrabld/projects/dimitripy/test/data/cloud_screening/cloudy-blue-sky.jpg'
#test_image = Image.open(image_path).convert('L')
#test_image = scipy.asarray(test_image)  # This should be np array

cloudy_image = '/home/marrabld/projects/dimitripy/test/data/cloud_screening/cloudy-sky.jpg'
cloudy_image = Image.open(cloudy_image).convert('L')
cloudy_image = scipy.asarray(cloudy_image)

partly_cloudy_image = '/home/marrabld/projects/dimitripy/test/data/cloud_screening/cloudy-blue-sky.jpg'
partly_cloudy_image = Image.open(partly_cloudy_image).convert('L')
partly_cloudy_image = scipy.asarray(partly_cloudy_image)

clear_image = '/home/marrabld/projects/dimitripy/test/data/cloud_screening/clear-blue-sky.jpg'
clear_image = Image.open(clear_image).convert('L')
clear_image = scipy.asarray(clear_image)

ck_method = libdimitripy.cloud_screening.CKMethod()

m, s, w = ck_method.process_image(partly_cloudy_image)
pylab.plot(w, s)
p = ck_method.fit_model(w, s)

fitfunc = lambda p, x: p[0] * x ** p[1]

y = fitfunc(p, w)

#pylab.plot(w, y)

pickle_file = '/home/marrabld/projects/dimitripy/libdimitripy/cache/ck_cloud.p'
[cloudy_model, partly_cloudy_model, clear_model] = pickle.load(open(pickle_file, "rb"))

cm = fitfunc(clear_model, w)
pc = fitfunc(partly_cloudy_model, w)
cl = fitfunc(cloudy_model, w)

pylab.plot(w, cm)
pylab.plot(w, pc)
pylab.plot(w, cl)
pylab.legend(['clear','partly','cloudy'])

pylab.show()



