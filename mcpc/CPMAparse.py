import os
import matplotlib.pyplot as plt
import numpy as np
import smps
import datetime as dt
import math as mt


filepath = os.path.join(os.getcwd(), "SMPS*project/OPCtest9_21000.cpma")

meta = dict()
data = dict()
counterRAW = 1
counterOTHER = 0
datalist = []

with open(filepath) as f:
    for i, line in enumerate(f):
        # parse the meta data
        _line = line.split('\t')

        if i <= 5:
            if i == 0:
                _line = _line[1:]

            for j in range(0, len(_line), 2):

                meta[_line[j][:-1]] = _line[j+1].strip()

        elif _line[0] == 'SCAN':
            #Marks beginning of data chunk, logs current chunk (statistics) into dictionary

            data['OTHER'+str(counterOTHER)] = datalist
            counterOTHER = counterOTHER + 1
            datalist = []

        elif _line[0] == 'END OF SCAN':
            #Marks end of important data chunk (number concentrations, mass concentrations, etc.),
            #logs data into dictionary with key of RAW + scan number
            data['RAW'+str(counterRAW)] = datalist
            counterRAW = counterRAW + 1
            datalist = []

        else :
            #Creates chunks of data
            #For the RAW entries this includes column titles and data
            #For other entries includes a mess of stats in property:\t value
            datalist.append( _line )


        #f.split('\t')
        #if line.startswith("SCAN"):
        #    print ("New Scan at line {}".format(i))

#Getting the information we want out of the dictionary
arrcount = 0
numbins = len(data['RAW1'])

#Create empty array for the 3 properties we want, time of scan size bin, and dndlogdp value
timesizecount = np.empty([counterRAW*numbins,3])

for key in data:
    #loop through each entry

    if key[0] == 'O':
        #skip OTHER entries
        pass

    else :
        #for raw entries, it is 2D list, the first dimension contains each line
        list2D = data[key]

        for x in list2D:
            #going through each recorded line and getting out data we want

            if x[0] == 'Datum#':
                #skip column headers (might use later for neater data)

                pass

            else:
                #Have to turn time field into a numerical value (converted to hours)
                time = x[1]
                _time = time.split(':')
                numtime = float(_time[0]) + float(_time[1])/60 +float(_time[2])/3600

                #put data in a simple array with each every size bin for each scan lumped together
                timesizecount[arrcount][0] = numtime
                timesizecount[arrcount][1] = float(x[4])
                timesizecount[arrcount][2] = float(x[5])
                arrcount += 1


### The rest of this file is more like a method for comparing SPMS and CPC data. Not sure it's very valuable

smps0921 = smps.io.load_file("/Users/jrowe31/Documents/20170921_AAAR.txt", column = False)

#PUTTING IT ALL TOGETHER!

#Start for each scan in CMPA data, create empty array to store data. Will contain 4 columns, first
#contains CMPA dNdlogdp, second SMPS dNdlogdp, third is counting efficiency, third is percent difference

comparr = np.empty([counterRAW*numbins,1])
compcounter = 0

#Gets each scan from CPMA parsed file
for scan in timesizecount :
    bincounter = -1
    timecounter = -1

    #Have to correct for when scans go to zero, simply make everything NaN
    if scan[2] == 0:
        comparr[compcounter][:] = np.nan

    else :
        #Goes through scan times from smps and find index of time that is just under scan time of CMPA scan time
        for scantime in smps0921.raw.index:
            numerictime = scantime.time().hour + scantime.time().minute/60 + scantime.time().second/3600
            if numerictime < scan[0]:
                timecounter += 1

        #Goes through SMPS size bins and finds size range that corresponds to size measure by CMPA
        for x in smps0921.bins:
            if x[0]*1000 < scan[1] :
                bincounter += 1

        #Getting the actual value out of the data frame and doing math
        smpscount = smps0921.dndlogdp.iloc[timecounter, bincounter]
        #comparr[compcounter][0] = scan[2]
        #comparr[compcounter][1] = smpscount
        comparr[compcounter]= scan[2]/smpscount
        #comparr[compcounter][3] = (scan[2] - smpscount)/smpscount

        #Finally, increase compcounter by one
        compcounter += 1

#Voila!


new = np.resize(comparr,(230, 10))
final = new[:60][:]
averages = np.average(final, axis = 0)
averages[9] = 3000
plt.plot(timesizecount[:10,1], averages)
