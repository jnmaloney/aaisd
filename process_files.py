import gzip
from datetime import datetime


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

temp_map = {} # To be used for generating statistics
wind_map = {}
temp_map_allyears = {} # To compare individual points
def add_data(year, mday, data, store, actual_store):

    # convert type of mday from string to datetime
    mday = datetime(day=int(mday[2:4]), month=int(mday[0:2]), year=2000) # ?
    actual_day = datetime(day=int(mday[2:4]), month=int(mday[0:2]), year=year)

    if not store.has_key(mday):
        store[mday] = []
    data_int = int(data)
    if not data_int == 9999:
        store[mday].append((int(year), data_int))

        if actual_store:
            if not actual_store.has_key(actual_day):
                actual_store[actual_day] = []
            actual_store[actual_day].append(data_int)

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
        if len(year_arr) == 0: #year_arr = [9999]
            temp_list_mean[i] = None
        else:
            temp_list_mean[i] = numpy.mean(year_arr)

    # remove values
    temp_list_mean = filter(lambda a: a != None, temp_list_mean)



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
# for i in range(len(n_events_year)):
#     year = 1950 + i
#     n = n_events_year[i]
#     print "%s: %s" % (year, n)


# Bokeh displays
from bokeh.plotting import figure, output_file, show

output_file("lines.html")

y = temp_avg.values()
xs = temp_avg.keys()
#x = ["%s/%s/2000" % (i[2:4], i[0:2]) for i in xs]
#x = [datetime(day=int(i[2:4]), month=int(i[0:2]), year=2000) for i in xs]
x = xs

# Sort the lists
x, y = (list(i) for i in zip(*sorted(zip(x, y), key=lambda pair: pair[0])))

y_mean = y#temp_avg.values()

# Variance / std
y_upper = []
y_lower = []
for i in temp_avg.keys():
    y_upper.append( temp_avg[i] + temp_std[i] )
    y_lower.append( temp_avg[i] - temp_std[i] )

x, y_upper = (list(i) for i in zip(*sorted(zip(temp_avg.keys(), y_upper), key=lambda pair: pair[0])))
x, y_lower = (list(i) for i in zip(*sorted(zip(temp_avg.keys(), y_lower), key=lambda pair: pair[0])))


# all values
x_all = []
y_all = []
y_var_index = []
for k, v in temp_map.iteritems():
    for i in v:
        x_all.append(k)
        y_all.append(i)

        # stats for this k
        std = temp_std[k]
        avg = temp_avg[k]
        ind = int(abs(i - avg) / std)
        y_var_index.append(ind)

# Find the year that high-index points are occuring


# value colour index
colour_value = ['#0000ff', '#000088', '#0000ff', '#000088', 'orange', 'red', 'purple']
y_colour = []
for i in y_var_index:
    y_colour.append(colour_value[i])

# Figure
p = figure(title="Temperature statistics",
x_axis_label='day of year',
x_axis_type='datetime',
y_axis_label='Temperature (C)')

#p.circle(x, y, legend="Temperature (C)") # Individual data points
p.circle(x_all, y_all, legend="Temperature (C)", color=y_colour) # Individual data points
p.line(x, y_mean, legend="mean", color='#121212', line_width=2) # mean
p.line(x, y_upper, legend="upper", color='#898989', line_width=2) # upper var
p.line(x, y_lower, legend="lower", color='#898989', line_width=2) # lower var

show(p)
