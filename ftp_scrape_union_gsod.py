import sys, getopt
import ftplib
import os

pw = ''
union_file = ""
if len(sys.argv) == 3:
    pw = sys.argv[1]
    union_file = sys.argv[2]


weather_station_code = ""


# Open union file
f = open(union_file, "r")
to_read = {}
for line in f.readlines():
    station_code = line[0:12]
    to_read[station_code] = True

# FTP login
user = 'anonymous'
ftp = ftplib.FTP('ftp.ncdc.noaa.gov', user, pw)
ftp.cwd('/pub/data/gsod/')
ftp.sendcmd("TYPE i")    # Switch to Binary mode


# Scrape from 1929 - 2018 inclusive
year_begin = 2009
year_end = 2018
year_range = range(year_begin, year_end + 1)

master_save_directory = "gsod"
if not os.path.exists(master_save_directory):
    os.makedirs(master_save_directory)

#print "Saving data to %s/%s" % (os.getcwd(), master_save_directory)

for year in year_range:

    print year,
    count_success = 0
    count_error = 0
    count_skipped = 0

    # Go to ftp directory for year
    ftp.cwd("%s" % year)

    # Get file list
    files = []
    try:
        files = ftp.nlst()
    except Exception as e:
        print e
        continue

    print "%s files found" % len(files)

    for fname in files:

        #print "%s: %s \r" % (count_error + count_success, fname)
        sys.stdout.write("\r{0}: {1}>".format(count_error + count_success + count_skipped, fname))
        sys.stdout.flush()

        fdata = [i.split('-') for i in fname.split('.')]
        if len(fdata) == 0: continue
        if len(fdata[0]) < 3: continue
        station_code_A = fdata[0][0]
        station_code_B = fdata[0][1]

        weather_station_code = "%s-%s" % (station_code_A, station_code_B)

        if not to_read.has_key(weather_station_code): continue

        save_directory = "%s/%s" % (master_save_directory, weather_station_code)
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        file_to_save = "%s/%s" % (save_directory, fname)

        if os.path.isfile(file_to_save):
            count_skipped += 1
            continue;

        try:
            with open(file_to_save, "wb") as f:
                ftp.retrbinary("RETR %s" % fname, f.write)
            count_success += 1
        except Exception as e:
            #print e
            os.remove(file_to_save)
            count_error += 1

    sys.stdout.write("\r")
    sys.stdout.flush()

    if count_error: print "%s saved, %s skipped, %s errors" % (count_success, count_skipped, count_error)
    else: print "%s saved, %s skipped," % (count_success, count_skipped)

    ftp.cwd("..")
