"""Control n servos on n arduinos over serial.

This is for a servo with angles from 20-165.
"""

import glob
import platform
import serial
from time import sleep
import sys

def servo_iter():
	l = []
	for i in range(0,200):
		l.append(40)
	for i in range(0,200):
		l.append(80)
	for pos in l:
		yield pos

if __name__ == "__main__":
	# find arduinos
	# note: currently this is Mac only
	arduinos = glob.glob('/dev/tty.usbmodem*')
	print arduinos

	if len(arduinos) == 0:
		print "No Arduinos found"
		sys.ext(1)

	ports = []
	for arduino in arduinos:
		try:
			# connect to serial port
			ports.append(serial.Serial(arduino, 9600))
		except:
			print "Failed to connect to Arduino"
			sys.exit(1)

	# need a short delay right after serial port is started for the Arduino to initialize
	sleep(2)

	# initialize generator
	pos = servo_iter()
	#pos = servo_iter2()

	try:
		while True:
			try:
				x = pos.next()
			except StopIteration:
				pos = servo_iter()
				#pos = servo_iter2()
				x = pos.next()
			print x
			
			# pad the servo value with zeros
			x = str(x).zfill(3)
			# for now we're sending the same value to both servos
			x = x + x

			# send data to the Arduinos
			for port in ports:
				port.write(x)

	# close the serial port on exit, or you will have to unplug the Arduino to connect again
	finally:
		for port in ports:
			port.close()