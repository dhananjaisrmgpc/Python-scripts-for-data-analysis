#xx=0
#f2=open("myimageFRESH.txt","r")
#f3=open("FRESH.txt","w")
#rec=f2.read(32)
#print rec
#length=rec.split("\n")
#print length
#for xx in range(5):
#	data=rec.replace('0x','').replace(',','').replace("\n",'')
	#f3.write(data)
#	print data
#f2.close
#f3.close
import binascii
hexdata=0
debug=0
comb_data=[]

def split(c) :
   global debug
   a= (ord(c)&0xf0) >>4
   if(a<=0x09) :
        a=a+0x30
   else :
        a=a+0x37
   b= ord(c)&0xf
   if(b<=0x09) :
        b=b+0x30
   else :
        b=b+0x37
   if (debug==1): print "Split Hex: " + hex(a), hex(b)
   a=str(hex(a))
   a=a[2:]
   a=binascii.unhexlify(a)
   b=str(hex(b))
   b=b[2:]
   b=binascii.unhexlify(b)
   rval=[a,b]
   return(rval)

def split_data(data_t):
   rdata=[]
   for tr_no in range(0,len(data_t)):
        nr=split(data_t[tr_no])
        rdata= rdata + nr
   return rdata

def compute_lrc(msg) :
   global debug
   lrc=0
   mesg=combine_data(msg)
   for j in range(0, len(mesg)) :
      
      lrc = lrc+ mesg[j]
   lrc=(~lrc +1)&0xff
   lr=(hex(lrc)).upper()
   if(lr=='0X0') : lr=lr+'0'
   if (debug==1): print "LRC: " + hex(lrc)
   return lr[2:]

def combine( a, b) :
   global debug
   a=binascii.hexlify(a)
   a=int(a,16)
   if(a<0x40) :
        a=a-0x30
   else :
        a=a-0x37
   #print a
   b=binascii.hexlify(b)
   b=int(b,16)
   if(b<0x40) :
        b=b-0x30
   else :
        b=b-0x37
   #print b

   c= (a<<4) + b
   #if (debug==1): print "Combined Hex: " + hex(c)
   #if (debug==1): print "Combined Ascii: " + format(c, "c")
   return c


def combine_data(msg) :
#   global msg_len
   global debug
   msg_len=len(msg)
   comb_data=[]
   for li in range(2,msg_len+1,2) :
        cdata=combine(msg[li-1],msg[li])
        comb_data.append(cdata)
   if(debug==1) : print "Tx Message : ", comb_data 
   return comb_data 

import binascii
data=[]
w=10
x=0
msb=0
lsb=0
bin_msb=0
bin_lsb=0
f3=open("FRESH.txt", "r")
import binascii

f4=open("coolPic6.txt", 'w')
f5=open("coolPic6.jpg", 'wb')
data=f3.read()
#print data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10]
#bdata=bytearray(b'\xff\xd8\xff\xfe\x00')
bdata=bytearray()
b1data=[]
end_count=(len(data)-4)
while((w>9)and(w<=(end_count))):
#while((w>7)and(w<=20)):
	x=w+1
	#print data[w]
	msb=str(data[w])
	lsb=str(data[x])
	#print (msb,lsb)
	#intdata=combine(msb.upper(),lsb.upper())
	#print (msb,lsb,intdata,hex(intdata))
	#bdata.extend(intdata)	
	hexdata=(combine(msb.upper(),lsb.upper()))
	b1data.extend(hexdata)	
	#print (hexdata)	
	#bdata.append(intdata)	
	#print intdata
	
	#print hexdata
	#hexdata=str(hexdata).replace('0x','')
	#if(hexdata=='0'):
	#	hexdata='00'
	#f4.write((hexdata)+"\n")
	#f5.write((hexdata))	
	#print (hexdata) 
	w=x+1	
x=0
#f5.write(bdata)
print b1data
f3.close
f4.close
f5.close
