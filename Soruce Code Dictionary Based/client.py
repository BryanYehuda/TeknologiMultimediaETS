#!/usr/bin/env python

import random
import socket, select
from time import gmtime, strftime
from random import randint
import time
import os

#image = raw_input("enter the name of the image file: ")

HOST = '127.0.0.1'
PORT = 6662

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (HOST, PORT)
sock.connect(server_address)

try:
    os.system('python3 LZW.py')
    time.sleep(20)
    myfile = open('/home/daniel/Documents/cmpr/CompressedFiles/checkCompressed.lzw', 'rb')
    bytes = myfile.read()
    size = len(bytes)

    # send image size to server
    sock.sendall("SIZE %s" % size)
    answer = sock.recv(4096)

    print 'answer = %s' % answer

    # send image to server
    if answer == 'GOT SIZE':
        sock.sendall(bytes)

        # check what server send
        answer = sock.recv(4096)
        print 'answer = %s' % answer

        if answer == 'GOT IMAGE' :
            #time.sleep(20)
            sock.sendall("BYE BYE ")
            print 'File successfully send to server'
            file_size1 = float(os.path.getsize('/home/daniel/Documents/cmpr/CompressedFiles/checkCompressed.lzw'))
            file_size2 = float(os.path.getsize('check.tif'))
            ukuran = float(file_size2/file_size1)
            print "rasio kompresi : "+str(float(ukuran))

    myfile.close()

finally:
    sock.close()