#  coding: utf-8
import socketserver

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

# https://www.tutorialspoint.com/http/http_message_examples.htm
# Formatting help
# Client Request
# GET /hello.htm HTTP/1.1
# User-Agent: Mozilla/4.0 (compatible; MSIE5.01; Windows NT)
# Host: www.tutorialspoint.com
# Accept-Language: en-us
# Accept-Encoding: gzip, deflate
# Connection: Keep-Alive

# Server response
# HTTP/1.1 200 OK
# Date: Mon, 27 Jul 2009 12:28:53 GMT
# Server: Apache/2.2.14 (Win32)
# Last-Modified: Wed, 22 Jul 2009 19:15:56 GMT
# Content-Length: 88
# Content-Type: text/html
# Connection: Closed


class MyWebServer(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)

        # split the data request into an array of strings
        #http_method, http_path, http_version, http_host =
        parsed_request = self.parse_request(self.data)

        # Splits up the contents of the parse request by method, path and type 
        if parsed_request != None:
            http_method = parsed_request[0]
            http_path = parsed_request[1]
            http_type = parsed_request[2]


            # Handles if the request is not a GET request
            if http_method != "GET":
                self.send_error(http_type, 405)
                return

            # Handles if it is a GET request
            else:


        # Handles if there is an error in parse_request
        else:
            raise AttributeError
            return



        # Uncomment this line to get contents of request. [method, path, hostID]
        #Results were: [b'GET', b'/', b'HTTP/1.1', b'Host:', b'127.0.0.1:8080', b'User-Agent:', b'curl/7.54.0', b'Accept:', b'*/*']



        self.request.sendall(bytearray("OK",'utf-8'))

#https://github.com/python/cpython/blob/master/Lib/http/server.py#L147
    def parse_request(self, request):
        # # splits the request on
        # parsed_request = request.split()
        # return parsed_request
        parsed_request = request.split()

        if len(parsed_request) == 0:
            return False

        # if len(parsed_request) >= 3:
        #     print(parsed_request[2])
        #     try:
        #         print(parsed_request[2].Contains('HTTP/'))
        #         if not parsed_request[2].Contains('HTTP/'):
        #             raise ValueError
        #             return
        #     except:
        #         print("Error parsing HTTP request")
        #         return
        print(parsed_request)
        return parsed_request



    def send_error(self, version, error_code):
        # HTTP 1.1, 404

        if error_code == 405:
            output = (("%s %d %s\r\n" %
                    (version, error_code, "Method Not Allowed")).encode(
                        'latin-1', 'strict'))


        if error_code == 404:
            output = (("%s %d %s\r\n" %
                    (version, error_code, "Not Found")).encode(
                        'latin-1', 'strict'))

        self.request.sendall(output)



if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
