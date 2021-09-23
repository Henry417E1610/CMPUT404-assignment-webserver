#  coding: utf-8 
import socketserver
import os
import time

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        #print ("Got a request of: %s\n" % self.data)
        #self.request.sendall(bytearray("OK",'utf-8'))

        converted_data = self.data.decode("utf-8")
        request = converted_data.split('\r\n')
        command = request[0].split(' ')
        source = command[1]
        executing_date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        path_type = "text/html"
        
        if command[0] == 'GET':
            if "css" not in source and "index.html" not in source:
                if source[-1] == "/":
                    source += "index.html"
                else:
                    temp = "./www" + source + "/index.html"
                    #print(os.path.abspath(temp))
                    #print(self.read_fl(os.path.abspath(temp)))
                    self.request.sendall(bytearray("HTTP/1.1 301 Moved Permanently\r\nLocation:" + source + '/' + "\r\n" + "Content-Type:" + path_type + "\r\n"
                                                   + "Date: "+ executing_date + "\r\n" + "Connection: close\r\n\r\n",'utf-8'))
                    return

            URLpath = "./www" + source
        else:
            # included but not limited to POST PUT DELETE
            self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed\r\n" + "Date: " + executing_date + "\r\n\r\n",'utf-8'))
            return

        # by now any non html or css sources have been filtered out
        if ".css" in source:
            path_type = "text/css"

        #if path_type!='':

        if os.path.exists(URLpath):
            #print(URLpath)
            #data = self.read_fl(URLpath)
            fl = open(URLpath,'r')
            data = fl.read()
            
            self.request.sendall(bytearray('HTTP/1.1 200 OK\r\n' + "Content-Type:" + path_type + "\r\n" + "Date: " + executing_date + "\r\n"
                                           + "Content-Length: " + str(len(data)) + "\r\n" + "Connection: close\r\n\r\n" + data,'utf-8'))
        else:
            self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n" + "Content-Type:" + path_type + "\r\n" + "Date: " + executing_date + "\r\n"
                                           + "Connection: close\r\n\r\n",'utf-8'))

'''
    def read_fl(self,URLpath):
        fl = open(URLpath,'r')
        data = fl.read()
        fl.close()
        return data
'''

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
