from optparse import OptionParser
import os
import sys
import StringIO

import requests
import pycurl

import config



def die(msg, exit_code=0):
    print msg
    sys.exit(exit_code)

def upload(location, filename, content_type, offset=0):
    c = None
    try:
        c = pycurl.Curl()
        #c.setopt(pycurl.VERBOSE, 1)
        c.setopt(pycurl.URL, str(location))
        bout = StringIO.StringIO()
        hout = StringIO.StringIO()

        c.setopt(pycurl.HEADERFUNCTION, hout.write)
        c.setopt(pycurl.WRITEFUNCTION, bout.write)
        c.setopt(pycurl.UPLOAD, 1)
        c.setopt(pycurl.CUSTOMREQUEST, 'PATCH')

        f = open(filename, 'rb')
        f.seek(offset)
        c.setopt(pycurl.READFUNCTION, f.read)
        filesize = os.path.getsize(filename)
        c.setopt(pycurl.INFILESIZE, filesize)
        c.setopt(pycurl.HTTPHEADER, ["Expect:", "Content-Type: %s" % content_type, "Offset: %d" % offset])
        c.perform()

        response_code = c.getinfo(pycurl.RESPONSE_CODE)
        response_data = bout.getvalue()
        response_hdr = hout.getvalue()
        #print response_data
        #print response_hdr
        print "patch->", response_code
        return response_code == 200
    finally:
        if c: c.close()

parser = OptionParser()
parser.add_option("-f", "--file", dest="filename",
                  help="file to upload")
parser.add_option("-t", "--content-type",
                  dest="content_type", default="binary/octet-stream",
                  help="content-type")

(options, args) = parser.parse_args()


if not options.filename:
    parser.print_help()
    sys.exit(0)

filename = options.filename
content_type  = options.content_type


filesize = os.path.getsize(filename)
c  = requests.post(config.CREATE_ENDPT, headers={"Final-Length": filesize})
if c.status_code != 201:
    die("create failure. reason: %s"  % c.reason)

location = c.headers["Location"]

offset = 0
print location
upload(location, filename, content_type, offset)
h = requests.head(location)
#print h.headers
offset = int(h.headers["Offset"])
print "Offset: ", offset
if offset == os.path.getsize(filename):
    die("upload success")
die("upload failure")
