import sys
import ftplib
import os


if len(sys.argv) == 1:
    raise RuntimeError("Not enough arguments")

weather_station_code = sys.argv[1]

print "Accessing historical data for station code %s" % (weather_station_code)

# FTP login
user = 'anonymous'
pw = 'joshua.maloney@uqconnect.edu.au'
ftp = ftplib.FTP('ftp.ncdc.noaa.gov', user, pw)
ftp.cwd('/pub/data/gsod/')
ftp.sendcmd("TYPE i")    # Switch to Binary mode


# Scrape from 1901 - 2017 inclusive
year_begin = 1901
year_end = 2017
year_range = range(year_begin, year_end + 1)

save_directory = "gsod"
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

print "Saving data to %s/%s" % (os.getcwd(), save_directory)

for year in year_range:

    ftp.cwd("%s" % year)

    file_to_get = "%s-%s.op.gz" % (weather_station_code, year)
    file_to_save = "%s/%s" % (save_directory, file_to_get)

    try:
        with open(file_to_save, "wb") as f:
            ftp.retrbinary("RETR %s" % file_to_get, f.write)
    except Exception as e:
        print e
        os.remove(file_to_save)

    ftp.cwd("..")
