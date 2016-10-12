#!/usr/bin/python
import datetime
import serial

# http://stackoverflow.com/questions/23025021/how-would-i-add-the-timezone-to-a-datetime-datetime-object#23025048
ser = serial.Serial('/dev/ttyUSB0', 9600)

while(True):
	dataline = ser.readline().strip()
	last_delim = dataline.rfind('%')
	second_to_last_delim = dataline.rfind('%', 0, last_delim) + 1
	data = dataline[second_to_last_delim: last_delim].split(',')
	date = datetime.datetime.now()

	output = '{0} UTC - {1}'.format(date, ';'.join(data))

	print(output)
	with open('water_table.txt', 'a') as fid:
		fid.write(output + '\n')


ser.close()

