#!/usr/bin/python
import serial
import os
import sys

#ser=serial.Serial('COM4',baudrate=9600,timeout=0)
ser=serial.Serial('/dev/ttyUSB0',baudrate=9600,timeout=0)
#ser=serial.Serial('/dev/ttyACM0',baudrate=9600,timeout=0)

#$GPRMC,103246.096,V,,,,,0.00,0.00,101118,,,N*48
#$GPVTG,0.00,T,,M,0.00,N,0.00,K,N*32
#$GPGGA,103247.096,,,,,0,0,,,M,,M,,*44
#$GPGSA,A,1,,,,,,,,,,,,,,,*1E

raw_dt = "1"
gpvgt_dat=[]
gprmc_dat=[]	
gpgga_dat=[] 
gpgsa_dat=[]

gpvgt_match=0
gprmc_match=0
gpgga_match=0 
gpgsa_match=0 

apnd_data=0

while(1):
        while(ser.inWaiting()>0):
                #rec=ser.read()
		rec=ser.read()
		
		if(rec ==str('$')):
			apnd_data=1
		if(apnd_data==1):
			raw_dt = raw_dt + rec
			if(rec ==str(",")):				
				if(raw_dt == str("$GPRMC,")):
					gprmc_match=1
				if(gprmc_match==1):
					#print raw_dt,gprmc_match,gpvgt_match,apnd_data	
					gprmc_dat.append(raw_dt)
			
				if(raw_dt == str("$GPVTG,")):
					gpvgt_match=1
				if(gpvgt_match==1):
					gpvgt_dat.append(raw_dt)

				if(raw_dt == str("$GPGGA,")):
					gpgga_match=1
				if(gpgga_match==1):
					gpgga_dat.append(raw_dt)

				if(raw_dt == str("$GPGSA,")):
					gpgsa_match=1
				if(gpgsa_match==1):
					gpgsa_dat.append(raw_dt)

				raw_dt=""
								
		if(rec ==str('\n')):
			#print raw_dt,gprmc_match,gpvgt_match,apnd_data
                        try:
			 if(len(gprmc_dat)>8):
				#print"1- ",gprmc_dat
				print "gprmc"
				print"Status       ",gprmc_dat[2]
                                print"Latitude_1    ",gprmc_dat[3]
				print"Lati Dir_1    ",gprmc_dat[4]				
				print"Longitude_1   ",gprmc_dat[5]
				print"Long Dir_1    ",gprmc_dat[6]
				print"Date         ",gprmc_dat[9]
				print"Magn Vari    ",gprmc_dat[10],gprmc_dat[11]      
				print"-----------------------------------------------"

			 if(len(gpvgt_dat)>8):
				#print"2- ",gpvgt_dat
				print"gpvgt"
				#print"True Track   ",gpvgt_dat[1],gpvgt_dat[2]
				#print"Magn Track   ",gpvgt_dat[2],gpvgt_dat[3]
				print"Spd knots    ",gpvgt_dat[4],gpvgt_dat[5]
				print"Spd km/hr    ",gpvgt_dat[6],gpvgt_dat[7]
				print"-----------------------------------------------"

			 if(len(gpgga_dat)>8):
				print "gpgga"				
				#print"3- ",gpgga_dat
			        print"UTC         ",gpgga_dat[1]
 				print"Latitude_2    ",gpgga_dat[2]
				print"Lati Dir_2    ",gpgga_dat[3]				
				print"Longitude_2   ",gpgga_dat[4]
				print"Long Dir_2    ",gpgga_dat[5]
				print"GPS_Fix     ",gpgga_dat[6]
				print"No. of Sat  ",gpgga_dat[7]
				#print"Hori_Dilu   ",gpgga_dat[8]
				print"Altitude    ",gpgga_dat[9],gpgga_dat[10]
				#print"Ht_elepsoid ",gpgga_dat[11],gpgga_dat[12]
				print"-----------------------------------------------"				

			 #if(len(gpgsa_dat)>8):
				#print"4- ",gpgsa_dat
				#print "gpgsa"
				#print"-----------------------------------------------"

                        
                        except:
                                pass
			apnd_data=0			
			raw_dt=""
			apnd_data=0
			gpvgt_dat=[]
			gprmc_dat=[]
			gpgga_dat=[] 
			gpgsa_dat=[]	
			gpvgt_match=0
			gprmc_match=0
			gpgga_match=0 
			gpgsa_match=0
ser.close()
'''
##https://www.gpsinformation.org/dale/nmea.htm

 $GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47

Where:
     GGA          Global Positioning System Fix Data
     123519       Fix taken at 12:35:19 UTC
     4807.038,N   Latitude 48 deg 07.038' N
     01131.000,E  Longitude 11 deg 31.000' E
     1            Fix quality: 0 = invalid
                               1 = GPS fix (SPS)
                               2 = DGPS fix
                               3 = PPS fix
			       4 = Real Time Kinematic
			       5 = Float RTK
                               6 = estimated (dead reckoning) (2.3 feature)
			       7 = Manual input mode
			       8 = Simulation mode
     08           Number of satellites being tracked
     0.9          Horizontal dilution of position
     545.4,M      Altitude, Meters, above mean sea level
     46.9,M       Height of geoid (mean sea level) above WGS84
                      ellipsoid
     (empty field) time in seconds since last DGPS update
     (empty field) DGPS station ID number
     *47          the checksum data, always begins with *

  $GPGSA,A,3,04,05,,09,12,,,24,,,,,2.5,1.3,2.1*39

Where:
     GSA      Satellite status
     A        Auto selection of 2D or 3D fix (M = manual) 
     3        3D fix - values include: 1 = no fix
                                       2 = 2D fix
                                       3 = 3D fix
     04,05... PRNs of satellites used for fix (space for 12) 
     2.5      PDOP (dilution of precision) 
     1.3      Horizontal dilution of precision (HDOP) 
     2.1      Vertical dilution of precision (VDOP)
     *39      the checksum data, always begins 

RMC - NMEA has its own version of essential gps pvt (position, velocity, time) data. It is called RMC, The Recommended Minimum, which will look similar to:

$GPRMC,123519,A,4807.038,N,01131.000,E,022.4,084.4,230394,003.1,W*6A

Where:
     RMC          Recommended Minimum sentence C
     123519       Fix taken at 12:35:19 UTC
     A            Status A=active or V=Void.
     4807.038,N   Latitude 48 deg 07.038' N
     01131.000,E  Longitude 11 deg 31.000' E
     022.4        Speed over the ground in knots
     084.4        Track angle in degrees True
     230394       Date - 23rd of March 1994
     003.1,W      Magnetic Variation
     *6A          The checksum data, always begins with *

VTG - Velocity made good. The gps receiver may use the LC prefix instead of GP if it is emulating Loran output.

  $GPVTG,054.7,T,034.4,M,005.5,N,010.2,K*48

where:
        VTG          Track made good and ground speed
        054.7,T      True track made good (degrees)
        034.4,M      Magnetic track made good
        005.5,N      Ground speed, knots
        010.2,K      Ground speed, Kilometers per hour
        *48          Checksum
'''

