#!/usr/bin/python
import time
import serial
import binascii
import sys
from shutil import copyfile
i=1

yh=''
yl=''

time_btw_chars=0.0006
#time_btw_sets=0.100##delay b/w packets

ser=serial.Serial('/dev/ttyUSB0',baudrate=38400,timeout=0)
#ser=serial.Serial('/dev/ttyAMA0',9600,timeout=1)

global multi_img
multi_img="/home/newuser/Intel_Demo_1/Camera_Demo/Single/multi_img.jpg"
#multi_img="/home/newuser/multi_img.jpg"

cmr_ok=0
p_count=1

def get_devreset():
    print "Resetting Device"
    msg=b"\x56\x00\x26\x00"
    TnR(msg)

def get_devversion():
    print "Get device version"
    msg=b"\x56\x00\x11\x00"
    TnR(msg)


def get_devpic():
    print "Capturing Image"
    msg=b"\x56\x00\x36\x01\x00"
    TnR(msg)

def get_devread():
    print "Reading Image length"
    msg=b"\x56\x00\x34\x01\x00"
    TnR(msg)

def get_devdata():
    print "Raw Image data"
    msg=b"\x56\x00\x32\x0C\x00\x0A\x00\x00\x00\x00\x00\x00"
    TnR(msg)

def TnR(msg):
    global yh,yl
    ser.flushInput()
    for j in range(0,len(msg)):
       ser.write(msg[j])
       ser.flush()
       #time.sleep(time_btw_chars)	
    print 'Tx= ',msg.encode('hex')
   
    time.sleep(5.50)
    lresp=ser.readline()
    #lresp=lresp.rstrip()
    print 'Rx= ',lresp.encode('hex')
    rdata=list((lresp))
    rdata=len(lresp)
    yh=lresp[rdata-2]
    yl=lresp[rdata-1]
    print yh.encode('hex'),yl.encode('hex')
    #size=(yh<<8) +yl
    #print int(size)

def SaveData(msg):
    global yh,yl
    global i                
    ser.flushInput()
    for j in range(0,len(msg)):
       ser.write(msg[j])
       ser.flush()
       #time.sleep(time_btw_chars)	
    print 'Tx= ',msg.encode('hex')
   
    i=0;
    f=open("/home/newuser/Intel_Demo_1/Camera_Demo/Single/rpimage.jpg", 'wb')
    time.sleep(0.5)
    while(ser.inWaiting()) :
     while(ser.inWaiting()) :
      	lresp=ser.read()
      	i=i+1
      	#print 'Rx= ',lresp.encode('hex')
	if(i>5) :
	  f.write(lresp)
     time.sleep(1)
    print i
    f.close()
    print("Snap_STOP")
    ser.close()
    return

def temp() :
    stime=time.time()
    while(1):
        while(ser.inWaiting()>0):
        	rec=ser.read()
		#print(rec,end="")
		#print rec.encode('hex')
		data=rec.encode('hex')	
		sys.stdout.write(data)
		writefile("RecData2.txt",data)
		i = i+1
                readfile("Reccounter.txt",i)
    return

def writefile(Fname,Fdata):
	f=open(Fname, 'a')
	f.write(str(Fdata))	
	f.close()
	return

def readfile(Fname,Fi):
	f=open(Fname, 'w')
	f.write(str(Fi))	
	f.close()
	return 
   
get_devreset()
get_devversion()
get_devpic()
get_devread()


if(yh) :
    print "Raw Image data"
    msg=b"\x56\x00\x32\x0C\x00\x0A\x00\x00\x00\x00\x00\x00" +yh +yl +"\x00\x0A"
    SaveData(msg)
    cmr_ok=1 	


