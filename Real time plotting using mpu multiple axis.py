import numpy as np
import matplotlib.pyplot as plt
import time
seconds=0
lines_in_file=0
time_xaxis_count=0

global time_values
time_values=[]

global ax_axis_sensor
ax_axis_sensor=[]
global plot_ax_values 
plot_ax_values=[]

global ay_axis_sensor
ay_axis_sensor=[]
global plot_ay_values 
plot_ay_values=[]

global az_axis_sensor
az_axis_sensor=[]
global plot_az_values 
plot_az_values=[]

global gx_axis_sensor
gx_axis_sensor=[]
global plot_gx_values 
plot_gx_values=[]

global gy_axis_sensor
gy_axis_sensor=[]
global plot_gy_values 
plot_gy_values=[]

global gz_axis_sensor
gz_axis_sensor=[]
global plot_gz_values 
plot_gz_values=[]

def calculate_time():
	global seconds
	global lines_in_file	
	date_stamp=[]
	minute_stamp=[]
	seconds=0.0
	
	for data_of_file in hmc_file:
		lines_in_file=lines_in_file+1		
		if(lines_in_file==1):
			date_stamp=data_of_file
		
	lines_in_file=lines_in_file-5
	print(lines_in_file)	
	print date_stamp
	minute_stamp=date_stamp.split(':')
	seconds=int(float(minute_stamp[2]))
	seconds=seconds*1.0
	print "Seconds", seconds, type(seconds)
	time.sleep(0.5)
	print "xxxc"

def read_sensor_values():
	global lines_in_file
	sensor_data_arrray=[]
	global ax_axis_sensor
	global ay_axis_sensor
	global az_axis_sensor 
        print(lines_in_file)
        local_read_index=0
        m=0
	for data_of_file in hmc_file:
		local_read_index=local_read_index+1
		data_of_file=data_of_file.replace(',','')
		data_of_file=data_of_file.replace('ax','')
		data_of_file=data_of_file.replace('ay','')
		data_of_file=data_of_file.replace('az','')
		data_of_file=data_of_file.replace('=','')
		if((local_read_index>=4)and(local_read_index<=lines_in_file+3)):
			sensor_data_arrray=data_of_file.split(' ')	
			ax_axis_sensor.append(sensor_data_arrray[1])			
			ay_axis_sensor.append(sensor_data_arrray[2])
		 	az_axis_sensor.append(sensor_data_arrray[3])		
			#print "ax ",sensor_data_arrray[1]," ay ",sensor_data_arrray[2]," az ",sensor_data_arrray[3]        

def time_on_xaixs():
	global seconds
	global lines_in_file
	global ax_axis_sensor
	global ay_axis_sensor
	global az_axis_sensor
	global time_xaxis_count         
	global time_values	
	global plot_ax_values
	global plot_ay_values
	global plot_az_values
	
	time_index=0.0
	y_axis_index=0	
        write_in_yaxis=0

	for local_variable in range(0,lines_in_file):
		time_values.append(float(time_index))		
		if(str(time_index)==str(seconds)):
			write_in_yaxis=1
		if(write_in_yaxis!=1):
			plot_ax_values.append(0.0)
			plot_ay_values.append(0.0)
			plot_az_values.append(0.0)
			plot_file.write(str(time_values[time_xaxis_count])+','+"0"+'\n')
		
		if(write_in_yaxis==1):
			
			plot_ax_values.append(float(ax_axis_sensor[y_axis_index]))
			plot_ay_values.append(float(ay_axis_sensor[y_axis_index]))	
			plot_az_values.append(float(az_axis_sensor[y_axis_index]))
			plot_file.write(str(time_values[time_xaxis_count])+','+ax_axis_sensor[y_axis_index] +','+ay_axis_sensor[y_axis_index] +','+az_axis_sensor[y_axis_index]+'\n')
			
			if(y_axis_index<lines_in_file):
				y_axis_index=y_axis_index+1	
		time_index=(time_index)+0.020
		time_xaxis_count=time_xaxis_count+1
	print "time_smpls",time_xaxis_count
        
 
hmc_file=open("ax_multi.log", 'r')
plot_file=open("mpu_multiple_ax_axis.txt", 'w')
time.sleep(0.2)
calculate_time()
hmc_file.close()

hmc_file=open("ax_multi.log", 'r')
time.sleep(0.2)
read_sensor_values()
hmc_file.close()

time_on_xaixs()
plot_file.close()
print len(time_values),len(ax_axis_sensor), len(plot_ax_values)
#plt.axis([time_values[0], time_values[time_xaxis_count-1], -10, 400])#list of [xmin, xmax, ymin, ymax], axis viewpoint
#plt.plot(2, 5, 'g^', 4, 15, 'c|')#markers at particular point
#linewidth=2.0

plt.plot(time_values,plot_ax_values,color='r') #plt.plot(y,z,'or')
plt.grid()
plt.tight_layout()#Helps u to get the full screen layout view
plt.savefig("mpu_multiple_ax_axis_graph.png")
#plt.show()
plt.close()#To prevent the overlap of figures

plt.plot(time_values,plot_ay_values,color='b') #plt.plot(y,z,'or')
plt.grid()
plt.tight_layout()#Helps u to get the full screen layout view
plt.savefig("mpu_multiple_ay_axis_graph.png")
#plt.show()
plt.close()#To prevent the overlap of figures

plt.plot(time_values,plot_az_values,color='g') #plt.plot(y,z,'or')
plt.grid()
plt.tight_layout()#Helps u to get the full screen layout view
plt.savefig("mpu_multiple_az_axis_graph.png")
#plt.show()
plt.close()#To prevent the overlap of figures

