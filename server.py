#  coding: utf-8
import socketserver, os, sys

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


# ALL SOURCES :
# https://github.com/python/cpython/blob/master/Lib/http/server.py#L147 (class BaseHTTPRequestHandler)
# - used this source mainly how to parse and handle outputs. Probably the source that I benefitted most from
# https://ruslanspivak.com/lsbaws-part1/ - this source helped in understanding what I'm sending as output
# https://www.tutorialspoint.com/http/http_message_examples.htm - Just for more understanding
# https://www.acmesystems.it/python_http - How to handle HTML & CSS files. By checking path endswith(mimetype), in our case .html or .class
#https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/301 - redirect if it doesn't end with /
#
class MyWebServer(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        #print ("Got a request of: %s\n" % self.data)

        # split the data request into an array of strings
        #http_method, http_path, http_version, http_host =
        returned_request = self.parse_request(self.data)
        parsed_request = returned_request
        path = ""

        # Splits up the contents of the parse request by method, path and type
        if (parsed_request != None) and (type(parsed_request) != bool):
            #print(parsed_request)
            http_method = parsed_request[0].decode()
            http_path = parsed_request[1].decode()
            http_type = parsed_request[2].decode()

            # Handles if the request is not a GET request
            if http_method != "GET":
                self.send_code(http_type, 405, path)
                return

            # Handles if it is a GET request
            # https://stackoverflow.com/questions/39801718/how-to-run-a-http-server-which-serve-a-specific-path - John Carter
            else:
                directory = os.getcwd()
                # gets the path that the request is trying to go to
                path = directory + '/www' + http_path

                # makes sure that the path actually exists
                if os.path.exists(path):
                    if not (path.endswith('/')):
                        self.send_code(http_type, 301, path)


                    else:
                        self.send_code(http_type, 200, path)



                else:
                    self.send_code(http_type, 404, path)



        # Handles if there is an error in parse_request
        else:
            #print(parsed_request)
          #  print("Request could not be parsed properly")
            http_type = "HTTP/1.1"
            self.send_code(http_type, 404, path)
            return



        # Uncomment this line to get contents of request. [method, path, hostID]
        #Results were: [b'GET', b'/', b'HTTP/1.1', b'Host:', b'127.0.0.1:8080', b'User-Agent:', b'curl/7.54.0', b'Accept:', b'*/*']



        self.request.sendall(bytearray("OK",'utf-8'))

#https://github.com/python/cpython/blob/master/Lib/http/server.py#L147
    def parse_request(self, request):
        # # splits the request on
        # parsed_request = request.split()
        # return parsed_request
       # print('this is the request')
       # print(request)
        parsed_request = request.split()
      #  print('this is the split request')
       # print(parsed_request)

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
        #print(parsed_request)
        return parsed_request


    def redirect_301(self, version, code, path):
        path = path + '/'
        output = ((("%s %d Moved Permanently\r\n" %
                 (version, code))+ ("Location %s\n\n" % path)).encode(
                     'latin-1', 'strict'))

        self.request.sendall(output)
        self.send_code(version, code, path)
        return




    def send_code(self, version, code, path):
        # HTTP 1.1, 404

        # Handle 405
        if code == 405:
            output = (("%s %d %s\r\n" %
                    (version, code, "Method Not Allowed")).encode(
                        'latin-1', 'strict'))

        # Handle 404
        elif code == 404:
            output = (("%s %d %s\r\n" %
                    (version, code, "Not Found")).encode(
                        'latin-1', 'strict'))

        # Handle 200
        elif code == 200:
            # is the path a file ?
            if os.path.isfile(path):
                file = open(path)
                file_data = file.read()
                file.close()

            # mime types can only be .css or HTML according to specs
                if path.endswith(".css"):
                    #print("handle 200 right here ")
                    #print("trying to handle CSS")
                    byte_contents = bytes(file_data, 'utf-8')
                    content_length = sys.getsizeof(byte_contents)
                    #print("this is my byte size")
                    #print(content_length)
                    output = ((("%s %d OK\r\n" %
                            (version, code))+  "Content-Type: text/css\n\n" + file_data).encode(
                                'latin-1', 'strict'))
                    # output = ((("%s %d OK\r\n" %
                    #         (version, code))+  ("Content-Type: text/css\n\nContent-Length: %s\n\n" % content_length) + file_data).encode(
                    #             'latin-1', 'strict'))


                    print("this is the output")
                    print(output)

                elif path.endswith(".html"):
                    #print('handle 200 right here for html')
                #    print("trying to handle HTML")
                    output = ((("%s %d OK\r\n" %
                            (version, code))+  "Content-Type: text/html\n\n" + file_data).encode(
                                'latin-1', 'strict'))


                else:
                    # send 404 code if we can't recognize the file
                    output = (("%s %d %s\r\n" %
                            (version, 404, "Not Found")).encode(
                                'latin-1', 'strict'))

# bad practice in how i'm handling this , should probably the way program finds file vs. directory and have a seperate function to send codes
# will fix after

#source : https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/301
#301
# Header:
#HTTP/1.1 301 Moved Permanently
#Location: http://www.example.org/index.asp
            elif os.path.isdir(path):

                # if (not(path.endswith('/'))):
                #     output = ((("%s %d Moved Permanently\r\n" %
                #             (version, 301)) + ("Location: %s\n\n" % (path + '/'))).encode(
                #                 'latin-1', 'strict'))
                # else:
                path = path + ("/index.html")
                if os.path.isfile(path):
                    file = open(path)
                    file_data = file.read()
                    file.close()

                    output = ((("%s %d OK\r\n" %
                            (version, code))+  "Content-Type: text/html\n\n" + file_data).encode(
                                'latin-1', 'strict'))

                else:
                    output = (("%s %d %s\r\n" %
                            (version, 404, "Not Found")).encode(
                                'latin-1', 'strict'))




    self.request.sendall(output)
    return







if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
