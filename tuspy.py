from optparse import OptionParser
import os
import sys
import StringIO
import time
import traceback

import requests
import pycurl

import config

#exponential backoff
initial_delay = 10 # 10 seconds
max_attempts = 3
def attempts():
    for i in range(max_attempts):
        yield i
        time.sleep(initial_delay ** i)

def die(msg, exit_code=0):
    print msg
    sys.exit(exit_code)

def get_endpt(filename):
    filesize = os.path.getsize(filename)
    c  = requests.post(config.CREATE_ENDPT, headers={"Upload-Length": filesize, "Tus-Resumable": "1.0.0"})
    if c.status_code != 201:
        die("create failure. reason: %s"  % c.reason)
    location = c.headers["Location"]
    print location
    return location

def get_offset(location):
    h = requests.head(location,  headers={"Tus-Resumable": "1.0.0"})
    offset = int(h.headers["Upload-Offset"])
    print "Offset: ", offset
    return offset 

def upload(location, filename, offset=0, upload_speed=None):
    c = None
    content_type = "application/offset+octet-stream"
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
        if offset > 0: 
            f.seek(offset)
        c.setopt(pycurl.READFUNCTION, f.read)
        filesize = os.path.getsize(filename)
        if upload_speed:
            c.setopt(pycurl.MAX_SEND_SPEED_LARGE, upload_speed)
        c.setopt(pycurl.INFILESIZE, filesize - offset)
        c.setopt(pycurl.HTTPHEADER, ["Expect:", "Content-Type: %s" % content_type, "Upload-Offset: %d" % offset, "Tus-Resumable: 1.0.0"])
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
parser.add_option("-u", "--upload_speed",
                  dest="upload_speed", default=None,
                  help="upload speed in bytes per second")

"""
parser.add_option("-t", "--content-type",
                  dest="content_type", default="binary/octet-stream",
                  help="content-type")
"""

(options, args) = parser.parse_args()


if not options.filename:
    parser.print_help()
    sys.exit(0)

upload_speed = None
try:
    if options.upload_speed:
        upload_speed = int(options.upload_speed)
except:
    parser.print_help()
    sys.exit(0)    

filename = options.filename

if not os.path.exists(filename):
    die("%s not found" % filename)


status = "upload failure"
offset = 0
filesize = os.path.getsize(filename)
location = get_endpt(filename)
for i in attempts():
    try:
        offset = get_offset(location)
        if offset == filesize:
            status = "upload success"
            break
        upload(location, filename, offset=offset, upload_speed=upload_speed)
        offset = get_offset(location)
        if offset == filesize:
            status = "upload success"
            break
    except:
        traceback.print_exc()
die(status)
