__author__ = 'marrabld'
import pandas as pd
import csv
import os
import scipy
import datetime
from datetime import datetime as dt
import time
import pylab

from matplotlib.ticker import FormatStrFormatter, MultipleLocator

def toYearFraction(date):
    def sinceEpoch(date):  # returns seconds since epoch
        return time.mktime(date.timetuple())

    s = sinceEpoch

    year = date.year
    startOfThisYear = dt(year=year, month=1, day=1)
    startOfNextYear = dt(year=year + 1, month=1, day=1)

    yearElapsed = s(date) - s(startOfThisYear)
    yearDuration = s(startOfNextYear) - s(startOfThisYear)
    fraction = yearElapsed / yearDuration

    return date.year + fraction

csv_dir = "/home/marrabld/projects/DIMITRI_2.0/Bin"
csv_file = "__DIMITRI_DATABASE.CSV"
csv_file = os.path.join(csv_dir, csv_file)
count = 0

sites = ['Amazon', 'BOUSSOLE', 'DomeC', 'Libya4', 'SIO', 'SPG', 'TuzGolu', 'Uyuni']
date_list = []
date_dict = {}
sensors = ['AATSR',
           'ATSR2',
           'MERIS',
           'MODISA',
           'PARASOL',
           'VEGETATION']

for site in sites:
    print('==================')
    print(site)
    print('==================')
    for sensor in sensors:
        #print(sensor)
        count = 0
        date_list = []
        date_dict = {}
        cloud_flag_list = []

        #--------------------------------------------------#
        # Plot stuff
        #--------------------------------------------------#
        fig, ax = pylab.subplots()
        bar_width = 0.0035
        opacity = 0.4
        majorFormatter = FormatStrFormatter('%d')

        with open(csv_file, 'r') as csvfile:
            date_dict.clear()
            csvreader = csv.reader(csvfile, delimiter=';')
            for row in csvreader:
                if (row[1] == site) and (row[2] == sensor):  #and ((float(row[12]) > 0.0) and (float(row[13]) >= 0.0)):
                    date = datetime.datetime(int(row[4]), int(row[5]), int(row[6]))
                    #d_key = str(date.strftime("%Y"))
                    d_key = toYearFraction(date)
                    d_key = round(d_key, 2)
                    if not d_key in date_dict and int(row[13]) >= 0:
                        date_dict[d_key] = 1
                    elif d_key in date_dict and int(row[13]) >= 0:
                        date_dict[d_key] = date_dict[d_key] + 1

                    count += 1
                    cloud_flag_list.append(int(row[13]))
                    #print(str(row[12]) + ' :: ' + str(row[13]))

            ax.bar(scipy.float32(date_dict.keys()), scipy.float32(date_dict.values()), bar_width, alpha=opacity, color='b')
            ax.xaxis.set_major_formatter(majorFormatter)
            #ax.vlines(scipy.float32(date_dict.keys()), scipy.float32(date_dict.values()), bar_width, alpha=opacity)
            pylab.title(sensor + ' :: ' + site)
            pylab.xlabel('Decimal Year')
            pylab.ylabel('Number of manually cloud-screened images')
            pylab.grid()

            #pylab.show()
            pylab.savefig('./Cloudscreening_images/' + sensor + '--' + site + '.png')
            #pylab.clf()
            del (date_dict)
            del (date_list)
            print('--------------------')
            print(sensor)
            print('--------------------')
            print('Total :: ' + str(count))
            print('Not manually screened ' + str(cloud_flag_list.count(-1)))
            print('flag == 0 ' + str(cloud_flag_list.count(0)))
            print('flag == 1 ' + str(cloud_flag_list.count(1)))
            print('flag == 2 ' + str(cloud_flag_list.count(2)))
            print('Total manually screened ' + str(cloud_flag_list.count(0) + cloud_flag_list.count(1) + cloud_flag_list.count(2)))
            try:
                print('Percentage manually screened % :: ' + str(
                    ((float(cloud_flag_list.count(0)) + float(cloud_flag_list.count(1))) / float(count)) * 100.0))
            except:
                print('Percentage manually screened % :: 0')
            print('')

            #--------------------------------------------------#
            # Reset all of the values for each site and sensor
            #--------------------------------------------------#