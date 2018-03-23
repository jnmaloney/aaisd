import gzip
from datetime import datetime
import os

import numpy as np
import pandas as pd

from bokeh.plotting import figure, show, output_file
from bokeh.models.tickers import *
from bokeh.models.axes import *




# Data containers
moda_values = {
't_max': {},
't_min': {},
'wind_max': {},
'precip': {},
'snow_d': {},
}

# Conversion
def FStoC(f_string): return (float(f_string) - 32.0) * 5.0 / 9.0

# Read from a single archive
def read_archive(archivename):

    if not os.path.isfile(archivename): return

    with gzip.open(archivename, 'rb') as f:
        for line in f.readlines():
            process_linedata(line)

# Process a line from the data file
def process_linedata(line):

    # Ignore first line
    if line[0:6] == "STN---": return

    # Read data points
    line_data = line.split()
    yearmoda = line_data[2]
    wind_max = line_data[15]
    t_max_f = line[103:108]
    t_min_f = line[111:116]
    precip = line_data[19]
    snowd = line_data[20]

    # Add to collection for Mo-Da
    # Store data for Year-Mo-Da
    add_values(yearmoda, wind_max, 'wind_max')
    add_values(yearmoda, FStoC(t_max_f), 't_max')
    add_values(yearmoda, FStoC(t_min_f), 't_min')
    add_values(yearmoda, precip, 'precip')
    add_values(yearmoda, snowd, 'snow_d')


def add_values(yearmoda, value, label):

    if value > 500: return # 999

    store = moda_values[label]

    year = yearmoda[0:4]
    moda = yearmoda[4:]

    if not store.has_key(moda):
        store[moda] = []

    store[moda].append((value, year))

# Read each year's archive
for year in range(1901, 2017+1):
    archivename = 'gsod/600600-99999-%s.op.gz' % year
    read_archive(archivename)

# Process total statistics

# Box plot demo
values = moda_values['t_max']

modas = []
xx = []

for k, v in values.iteritems():
    for i in v:
        modas.append(k)
        xx.append(i[0])

df = pd.DataFrame(dict(score=xx, group=modas))

select_modas = ['0101', '0201', '0301', '0401', '0501', '0601', '0701', '0801', '0901', '1001','1101', '1201']
#select_modas = ['0101', '0301', '0701', '1001']
#select_modas = ['0301']
all_modas = sorted(values.keys())

# find the quartiles and IQR for each category
groups = df.groupby('group')
q1 = groups.quantile(q=0.25)
q2 = groups.quantile(q=0.5)
q3 = groups.quantile(q=0.75)
iqr = q3 - q1
upper = q3 + 1.5*iqr
lower = q1 - 1.5*iqr

# ?
#print lower.score['0301']

# find the outliers for each category
def outliers(group):
    cat = group.name
    return group[(group.score > upper.loc[cat]['score']) | (group.score < lower.loc[cat]['score'])]['score']
out = groups.apply(outliers).dropna()

# prepare outlier data for plotting, we need coordinates for every outlier.
if not out.empty:
    outx = []
    outy = []
    for cat in all_modas:
        # only add outliers if they exist
        if not out.loc[cat].empty:
            for value in out[cat]:
                outx.append(cat)
                outy.append(value)

#p = figure(tools="save", background_fill_color="#EFE8E2", title="", x_range=all_modas)
p = figure(
title="Outlying Temperature Events",
x_axis_label=None, #'Month-Day',
y_axis_label='Daily High Temperature from 1950 - 2017',
background_fill_color="#EFE8E2",
x_minor_ticks=0,
x_range=all_modas)

# ticker = SingleIntervalTicker(interval=5, num_minor_ticks=10)
# xaxis = LinearAxis(ticker=ticker)
# plot.add_layout(xaxis, 'below')

ticker = FixedTicker()
ticker.ticks = [0101, 0201, 0301, 0401]
xaxis = LinearAxis(ticker=ticker)
p.add_layout(xaxis, 'below')

# if no outliers, shrink lengths of stems to be no longer than the minimums or maximums
qmin = groups.quantile(q=0.00)
qmax = groups.quantile(q=1.00)
upper.score = [min([x,y]) for (x,y) in zip(list(qmax.loc[:,'score']),upper.score)]
lower.score = [max([x,y]) for (x,y) in zip(list(qmin.loc[:,'score']),lower.score)]

# # stems
# p.segment(select_modas, upper.score, select_modas, q3.score, line_color="black")
# p.segment(select_modas, lower.score, select_modas, q1.score, line_color="black")
#
# # boxes
# p.vbar(select_modas, 0.7, q2.score, q3.score, fill_color="#E08E79", line_color="black")
# p.vbar(select_modas, 0.7, q1.score, q2.score, fill_color="#3B8686", line_color="black")

# whiskers (almost-0 height rects simpler than segments)
# p.rect(select_modas, lower.score[select_modas[0]], 0.2, 0.01, line_color="black")
# p.rect(select_modas, upper.score[select_modas[0]], 0.2, 0.01, line_color="black")

# Corrected whisker plots
# for moda in select_modas:
#
#     # stems
#     p.segment([moda], upper.score[moda], [moda], q3.score[moda], line_color="black")
#     p.segment([moda], lower.score[moda], [moda], q1.score[moda], line_color="black")
#
#     # boxes
#     p.vbar([moda], 0.7, q2.score[moda], q3.score[moda], fill_color="#E08E79", line_color="black")
#     p.vbar([moda], 0.7, q1.score[moda], q2.score[moda], fill_color="#3B8686", line_color="black")
#
#     # whiskers (almost-0 height rects simpler than segments)
#     p.rect([moda], lower.score[moda], 0.2, 0.01, line_color="black")
#     p.rect([moda], upper.score[moda], 0.2, 0.01, line_color="black")

# All values continuous box plot
#for moda in moda_values
# for moda in all_modas:
#
#     # boxes
#     p.vbar([moda], 0.7, q2.score[moda], q3.score[moda], fill_color="#E08E79", line_color="black")
#     p.vbar([moda], 0.7, q1.score[moda], q2.score[moda], fill_color="#3B8686", line_color="black")
#
#     # whiskers (almost-0 height rects simpler than segments)
#     p.rect([moda], lower.score[moda], 0.2, 0.01, line_color="black")
#     p.rect([moda], upper.score[moda], 0.2, 0.01, line_color="black")


q1s = [q1.score[i] for i in all_modas]
q2s = [q2.score[i] for i in all_modas]
q3s = [q3.score[i] for i in all_modas]
#p.line(all_modas, q3s, line_color='#E08E79')
#p.line(all_modas, q2s, line_color='black')
#p.line(all_modas, q1s, line_color='#3B8686')
p.patch(all_modas + all_modas[::-1], q3s + q2s[::-1], color='#E08E79')
p.patch(all_modas + all_modas[::-1], q2s + q1s[::-1], color='#3B8686')
#p.line(all_modas, q2s, line_color='black')

lowers = [lower.score[i] for i in all_modas]
uppers = [upper.score[i] for i in all_modas]
#p.line(all_modas, uppers, line_color='black')
#p.line(all_modas, lowers, line_color='black')
p.patch(all_modas + all_modas[::-1], uppers + q3s[::-1], color='white')
p.patch(all_modas + all_modas[::-1], q1s + lowers[::-1], color='white')


# outliers
if not out.empty:
    p.circle(outx, outy, size=6, color="#F38630", fill_alpha=0.6)

p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = "white"
p.grid.grid_line_width = 2
p.xaxis.major_label_text_font_size="12pt"

output_file("boxplot.html", title="boxplot.py example")

show(p)
