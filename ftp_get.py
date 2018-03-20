import ftplib

user = 'anonymous'
pw = 'joshua.maloney@uqconnect.edu.au'
ftp = ftplib.FTP('ftp.ncdc.noaa.gov', user, pw)
#ftp.login()
ftp.cwd('/pub/data/noaa/')

#print ftp.dir()


# Sidi Ifni, Morocco
# 600600-99999
# 1950-03-10 to 2018-03-14
weather_station_code = "600600-99999"
#year = '1950'
#ext = '.gz'
#filename = weather_station_code + year + ext

#ftp.cwd(year)


def callback(data):
    print 'Done'

#file = open(filename, 'wb')
#ftp.retrbinary('RETR %s' % filename, file.write)
#file.close()

ftp.sendcmd("TYPE i")    # Switch to Binary mode

for year in range(1953, 2017+1):
    ftp.cwd("%s" % year)
    filename = "%s-%s.gz" % (weather_station_code, year)
    #fsize = ftp.size(filename)
    #if fsize:
    try:
        with open("dl/"+filename, "wb") as f:
            ftp.retrbinary("RETR %s" % filename, f.write)
    except Exception as e:
        print e

    ftp.cwd("..")

ftp.close()
