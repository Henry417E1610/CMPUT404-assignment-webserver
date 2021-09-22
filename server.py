#  coding: utf-8 
import socketserver
import os

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
        
        if command[0] == 'GET':
            if "css" not in source and "index.html" not in source:
                if source[-1] == "/":
                    source=source+"index.html"
                else:
                    self.request.sendall(bytearray("HTTP/1.1 301 Moved Permanently\r\nLocation:" + source +'/' +"\r\n",'utf-8'))
                    return

            URLpath = "./www"+source
        else:
            self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed\r\n",'utf-8'))
            return

        #path_type=''
        # by now any non html or css sources have been filtered out
        if ".html" in source:
            path_type="text/html"
        elif ".css" in source:
            path_type="text/css"

        #if path_type!='':

        if os.path.exists(URLpath):
            file = open(URLpath,'r')
            data = file.read()
            self.request.sendall(bytearray('HTTP/1.1 200 OK\r\n'+"Content-Type:" + path_type +"\r\n"  +"\r\n\r\n"+data,'utf-8'))
            return
        else:
            self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n",'utf-8'))
            return


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
