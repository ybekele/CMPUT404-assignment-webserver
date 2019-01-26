CMPUT404-assignment-webserver
=============================

CMPUT404-assignment-webserver

See requirements.org (plain-text) for a description of the project.

Make a simple webserver.

Contributors / Licensing
========================

Generally everything is LICENSE'D under the Apache 2 license by Abram Hindle.

server.py contains contributions from:

* Abram Hindle
* Eddie Antonio Santos
* Jackson Z Chang
* Mandy Meindersma 

But the server.py example is derived from the python documentation
examples thus some of the code is Copyright © 2001-2013 Python
Software Foundation; All Rights Reserved under the PSF license (GPL
compatible) http://docs.python.org/2/library/socketserver.html

# https://github.com/python/cpython/blob/master/Lib/http/server.py#L147 (class BaseHTTPRequestHandler)
# - used this source mainly how to parse and handle outputs. Probably the source that I benefitted most from
# https://ruslanspivak.com/lsbaws-part1/ - this source helped in understanding what I'm sending as output
# https://www.tutorialspoint.com/http/http_message_examples.htm - Just for more understanding
# https://www.acmesystems.it/python_http - How to handle HTML & CSS files. By checking path endswith(mimetype), in our case .html or .class
#https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/301 - redirect if it doesn't end with /

