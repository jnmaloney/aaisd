from bokeh.plotting import figure, show, save, output_file
from bokeh.models.tickers import *
from bokeh.models.axes import *
from bokeh.palettes import brewer
from os import listdir
from os.path import isfile, join

# Open outliers files

years = {
'temp': [],
'dewp': [],
't_min': [],
't_max': [],
'precip': [],
'snow_d': [],
'wind_max': [],
}
values_high = {
'temp': [],
'dewp': [],
't_min': [],
't_max': [],
'precip': [],
'snow_d': [],
'wind_max': [],
}
values_low = {
'temp': [],
'dewp': [],
't_min': [],
't_max': [],
'precip': [],
'snow_d': [],
'wind_max': [],
}

onlyfiles = [f for f in listdir('locs') if isfile(join('locs', f))]
for fname in onlyfiles:
    f = open(join('locs', fname), "r") #"locs/833780-99999-outliers.txt", "r")
    #f = open("locs/833780-99999-outliers.txt", "r")
    for line in f.readlines():
        s = line.split()
        year = int(s[1])
        value = s[0]
        r = int(s[2])
        u = int(s[3])
        l = int(s[4])

        years[value].append(year)
        values_high[value].append((100.0*u) / r)
        values_low[value].append((100.0*l) / r)

# x = []
# for i in range(len(l)):
#     x.append( (100.0*(l[i]+u[i])) / r[i] )

colors = brewer['Spectral'][4]
colorsMap = {
'temp': colors[0],
'dewp': colors[1],
't_min': colors[2],
't_max': colors[3],
'precip': 'lightblue',
'snow_d': 'lightgrey',
'wind_max': 'lightsteelblue',
}

# Do figures seperately
# for value in [
# 'temp',
# 'dewp',
# 't_min',
# 't_max',
# 'precip',
# 'snow_d',
# 'wind_max']:
#     p = figure(
#     title=None,
#     x_axis_label='year', #'Month-Day',
#     y_axis_label='%',
#     background_fill_color="#EFE8E2",
#     plot_width=1200, plot_height=600,
#     )
#     p.xaxis[0].ticker = SingleIntervalTicker(interval=10, num_minor_ticks=0)
#
#     poly1 = range(1920, 2021)
#     poly2 = values_low[value]
#     print len(poly1), len(poly2)
#     poly1.insert(0, 1920)
#     poly2.insert(0, 0)
#     poly1.append(2020)
#     poly2.append(0)
#
#     p.patch(poly1, poly2,
#     #fill_color=colorsMap[value],
#     line_color=colorsMap[value])
#     #fill_alpha=0.5)
#
#     output_file("outlier_count_value_low_%s.html" % value)
#
#     show(p)
#     save(p)
#     y
#     p = figure(
#     title=None,
#     x_axis_label='year', #'Month-Day',
#     y_axis_label='%',
#     background_fill_color="#EFE8E2",
#     plot_width=1200, plot_height=600,
#     )
#     p.xaxis[0].ticker = SingleIntervalTicker(interval=10, num_minor_ticks=0)
#
#     p.patch(poly1, poly2,
#     #fill_color=colorsMap[value],
#     line_color=colorsMap[value])
#     #fill_alpha=0.75)
#
#     output_file("outlier_count_value_high_%s.html" % value)
#
#     show(p)
#     save(p)

def sub(y, x, z, value):
    p = figure(
    title=None,
    x_axis_label='year', #'Month-Day',
    y_axis_label='%',
    background_fill_color="#EFE8E2",
    plot_width=1200, plot_height=600,
    )
    p.xaxis[0].ticker = SingleIntervalTicker(interval=10, num_minor_ticks=0)

    p.patch(y, x,
    fill_color=colorsMap[value],
    line_color=colorsMap[value],
    line_width=2,
    fill_alpha=0.5)

    output_file("outlier_count_value_low_%s.html" % value)

    show(p)
    save(p)
    y
    p = figure(
    title=None,
    x_axis_label='year', #'Month-Day',
    y_axis_label='%',
    background_fill_color="#EFE8E2",
    plot_width=1200, plot_height=600,
    )
    p.xaxis[0].ticker = SingleIntervalTicker(interval=10, num_minor_ticks=0)

    p.patch(y, z,
    fill_color=colorsMap[value],
    line_color=colorsMap[value],
    line_width=2,
    fill_alpha=0.75)

    output_file("outlier_count_value_high_%s.html" % value)

    show(p)
    save(p)

# All poly

p = figure(
title=None,
x_axis_label='year', #'Month-Day',
y_axis_label='%',
background_fill_color="#EFE8E2",
plot_width=1200, plot_height=600,
)
p.xaxis[0].ticker = SingleIntervalTicker(interval=10, num_minor_ticks=0)

# # Plot 1
# for v in ['temp', 'dewp', 't_min', 't_max', 'precip', 'snow_d', 'wind_max']:
#     p.line(years[v], values_low[v])
#     p.line(years[v], values_high[v])

# Plot 2
v_store = {}

polys1 = {
'temp': [],
'dewp': [],
't_min': [],
't_max': [],
'precip': [],
'snow_d': [],
'wind_max': [],
}
polys2 = {
'temp': [],
'dewp': [],
't_min': [],
't_max': [],
'precip': [],
'snow_d': [],
'wind_max': [],
}
polysM1 = {
'temp': [],
'dewp': [],
't_min': [],
't_max': [],
'precip': [],
'snow_d': [],
'wind_max': [],
}
polysM2 = {
'temp': [],
'dewp': [],
't_min': [],
't_max': [],
'precip': [],
'snow_d': [],
'wind_max': [],
}
tracko = [0 for i in range(1920, 2021)]
y = []

for i in range(1920, 2021, 1):
    y.append(i)
for i in range(2020, 1920, -1):
    y.append(i)

for v in ['temp', 'dewp', 't_min', 't_max', 'precip', 'snow_d', 'wind_max']:
    x = []
    z = []

    for year in range(1920, 2021, 1):
        value_low = 0
        value_high = 0
        for year2 in range(1):
            try:
                i = years[v].index(year+year2)
                value_low = values_low[v][i]
                value_high = values_high[v][i]
            except Exception as e:
                pass
        x.append(value_low)
        z.append(value_high)

    sub(y, x, z, v)

    for i in range(len(x)):
        polys1[v].append(tracko[i])

        polys2[v].append(tracko[i] + x[i])


    for i in range(len(x)-1, 0, -1):
        polys1[v].append(tracko[i] + x[i])

        polys2[v].append(tracko[i] + x[i] + z[i])


    # for i in range(len(x)):
    #
    #     polys1[v].append(x[i])
    #     polys2[v].append(z[i])
    #
    #     polysM1[v].append(tracko[i] + x[i] * 0.5)
    #     polysM2[v].append(tracko[i] + x[i] + z[i] * 0.5)

        tracko[i] += x[i] + z[i]

    #p.patch(y, polys1[v])
    #p.line(y, polys1[v])

colors = brewer['Spectral'][4]
p.patch(y, polys2['temp'], fill_color=colors[0], fill_alpha=0.75)
p.patch(y, polys1['temp'], fill_color=colors[0], fill_alpha=0.5)
p.patch(y, polys2['dewp'], fill_color=colors[1], fill_alpha=0.75)
p.patch(y, polys1['dewp'], fill_color=colors[1], fill_alpha=0.5)
p.patch(y, polys2['t_min'], fill_color=colors[2], fill_alpha=0.75)
p.patch(y, polys1['t_min'], fill_color=colors[2], fill_alpha=0.5)
p.patch(y, polys2['t_max'], fill_color=colors[3], fill_alpha=0.75)
p.patch(y, polys1['t_max'], fill_color=colors[3], fill_alpha=0.5)
p.patch(y, polys2['precip'], fill_color='lightblue', fill_alpha=0.75)
p.patch(y, polys1['precip'], fill_color='lightblue', fill_alpha=0.5)
p.patch(y, polys2['snow_d'], fill_color='lightgrey', fill_alpha=0.75)
p.patch(y, polys1['snow_d'], fill_color='lightgrey', fill_alpha=0.5)
p.patch(y, polys2['wind_max'], fill_color='lightsteelblue', fill_alpha=0.75)
p.patch(y, polys1['wind_max'], fill_color='lightsteelblue', fill_alpha=0.5)
# p.rect(y, polysM2['wind_max'], 9, polys2['wind_max'],fill_color='lightsteelblue', fill_alpha=0.75, line_color="black", legend="wind_max +")
# p.rect(y, polysM1['wind_max'], 9,polys1['wind_max'],fill_color='lightsteelblue', fill_alpha=0.5, line_color="black", legend="wind_max -")
# p.rect(y, polysM2['snow_d'],   9, polys2['snow_d'],fill_color='lightgrey', fill_alpha=0.75, line_color="black", legend="snow_d +")
# p.rect(y, polysM1['snow_d'],   9, polys1['snow_d'],fill_color='lightgrey', fill_alpha=0.5, line_color="black", legend="snow_d -")
# p.rect(y, polysM2['precip'],   9, polys2['precip'],fill_color='lightblue', fill_alpha=0.75, line_color="black", legend="precip +")
# p.rect(y, polysM1['precip'],   9, polys1['precip'],fill_color='lightblue', fill_alpha=0.5, line_color="black", legend="precip -")
# p.rect(y,  polysM2['t_max'],   9, polys2['t_max'],  fill_color=colors[3], fill_alpha=0.75, line_color="black", legend="t_max +")
# p.rect(y, polysM1['t_max'],    9, polys1['t_max'],  fill_color=colors[3], fill_alpha=0.5, line_color="black", legend="t_max -")
# p.rect(y, polysM2['t_min'],    9, polys2['t_min'],  fill_color=colors[2], fill_alpha=0.75, line_color="black", legend="t_min +")
# p.rect(y, polysM1['t_min'],    9, polys1['t_min'],  fill_color=colors[2], fill_alpha=0.5, line_color="black", legend="t_min -")
#
# p.rect(y, polysM2['dewp'],     9, polys2['dewp'], fill_color=colors[1], fill_alpha=0.75, line_color="black", legend="dewp +")
# p.rect(y, polysM1['dewp'],     9, polys1['dewp'], fill_color=colors[1], fill_alpha=0.5, line_color="black", legend="dewp -")
# p.rect(y, polysM2['temp'],     9, polys2['temp'], fill_color=colors[0], fill_alpha=0.75, line_color="black", legend="temp +")
# p.rect(y, polysM1['temp'],     9,  polys1['temp'], fill_color=colors[0], fill_alpha=0.5, line_color="black", legend="temp -")




    #for year, value_low, value_high in years[v], values_low[v], values_high[v]:
    # for i in range(len(years[v])):
    #     year = years[v][i]
    #     value_low = values_low[v][i]
    #     value_high = values_high[v][i]
    #     x.append(year)
    #     if not v_store.has_key(year):
    #         v_store[year] = 0
    #     v_store[year] += value_low
    #     y.append(v_store[year])
    #     v_store[year] += value_high
    #     z.append(v_store[year])

    # x.append(x[-1])
    # y.append(0)
    # z.append(0)
    #
    # for year in range(1920, 2021):
    #     value_low = 0
    #     value_high = 0
    #     try:
    #         i = years[v].index(year)
    #         value_low = values_low[v][i]
    #         value_high = values_high[v][i]
    #     except Exception as e:
    #         pass
    #
    #     y.append(year)
    #     x.append(value_low)
    #     z.append(value_high)
    #
    #
    #
    # #p.rect(x, [0.5*i for i in y], 1, y, fill_color="lightgrey")
    # #p.rect(x, [0.5*i for i in z], 1, z, fill_color="steelblue")
    #
    # xx = []
    # for i in y:
    #     xx.append(i)
    # y.reverse()
    # for i in y:
    #     xx.append(i)
    #
    # yy = []
    # for i in x:
    #     yy.append(i)
    # z.reverse()
    # for i in z:
    #     yy.append(i)
    #
    # p.line(xx, yy)

    # p.line(x, y)
    # p.line(x, z)

output_file("outlier_count_master.html")

show(p)
#save(p)
