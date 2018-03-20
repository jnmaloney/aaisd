import gzip


additional_data_code = {
    'AA1': 2,
    'AA2': 4,
    'AA3': 1,
    'AA4': 1,
    'AB1': 7,
    'AC1': 3,
    'AD1': 20,
    'AE1': 12,
    'AG1': 4,
    'AH1': 3,
    'AH2': 4,
    'AH3': 1,
    'AH4': 6,
    'AH5': 6,
    'AH6': 1,

}

temp_map = {}
wind_map = {}
def add_data(year, mday, data, store):
    if not store.has_key(mday):
        store[mday] = []
    data_int = int(data)
    if not data_int == 9999:
        store[mday].append((int(year), data_int))

def read_archive(archivename):
    with gzip.open(archivename, 'rb') as f:
        for line in f.readlines():
            #print line,

            # Data
            date_string = line[16-1:23]
            time_string = line[24-1:27]
            windspeed_string = line[66-1:69] # x10 m/s
            temp_string = line[88-1:92]

            #date = dateutil.parser.parse(date_string)
            year_string = date_string[0:4]
            mday_string = date_string[4:8]
            add_data(year_string, mday_string, windspeed_string, wind_map)
            add_data(year_string, mday_string, temp_string, temp_map)

            # Additional data
            # if line[106-1:108] != 'ADD': continue
            #
            # additional_data = line[109-1:]
            #
            # data_code = additional_data[0:3]
            # data_length = 10
            # data = additional_data[3-1:]
            #
            # add_id = line[109-1:111]


            #print date_string, time_string, windspeed_string, temp_string


# Read each year's archive
for year in range(1950, 2017+1):
    archivename = 'dl/600600-99999-%s.gz' % year
    read_archive(archivename)


# Summarise results
# Generate statistics per day-of-year
import numpy
temp_avg = {}
temp_std = {}
for mday in temp_map.keys():

    # For each day, collect all measurements to a single mean value

    temp_list = temp_map[mday]

    # collect multiple readings into lists per day-of-year
    temp_list_collected = [[] for i in range(1950, 2017+1)]
    for i in temp_list:
        year_index = i[0] - 1950
        value = i[1]
        temp_list_collected[year_index].append(value)

    # reduce lists to single mean values
    temp_list_mean = [9999 for i in range(1950, 2017+1)]
    for i in range(len(temp_list_mean)):
        year_arr = numpy.array(temp_list_collected[i])

        # Some values missing???
        if len(year_arr) == 0: year_arr = [9999]

        temp_list_mean[i] = numpy.mean(year_arr)

    # remove values
    filter(lambda a: a == 9999, temp_list_mean)


    # Calculate stats with numpy

    temp_arr = numpy.array(temp_list_mean)
    temp_avg[mday] = numpy.mean(temp_arr)
    temp_std[mday] = numpy.std(temp_arr)

    # Overwrite data!
    temp_map[mday] = temp_list_mean


    #print "%s: %i (%i)" % (mday, temp_avg[mday], temp_std[mday]),

# Check data for extreme events
n_events_year = [0 for i in range(1950, 2017+1)]
for mday in temp_map.keys():

    temp_mday_avg = temp_avg[mday]
    temp_mday_std = temp_std[mday]
    temp_list = temp_map[mday]
    n = 2 # deviations away from average

    #for i in temp_list:
    for i in range(len(temp_list)):
        t = temp_list[i]
        if t < temp_mday_avg - n * temp_mday_std:
            #print "%s: %s (%s)" % (mday, i, temp_mday_avg)
            n_events_year[i] += 1
        elif t > temp_mday_avg + n * temp_mday_std:
            #print "%s: %s (%s)" % (mday, i, temp_mday_avg)
            n_events_year[i] += 1

# Display event count per year
for i in range(len(n_events_year)):
    year = 1950 + i
    n = n_events_year[i]
    print "%s: %s" % (year, n)
