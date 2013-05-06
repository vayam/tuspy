# tuspy

TUS Protocol 0.2 Client Implementation
http://www.tus.io/protocols/resumable-upload.html

## Installation
```
pip install requests
pip install pycurl
```

## Configuration
```
Modify CREATE_ENDPT = "http://localhost:8080/files" in  config.py
```

## Run

```
Usage: tuspy.py [options]

Options:
  -h, --help            show this help message and exit
  -f FILENAME, --file=FILENAME
                        file to upload
  -t CONTENT_TYPE, --content-type=CONTENT_TYPE
                        content-type

```

## Example
```
python tuspy.py -f big_buck_bunny.mp4 -t video/mp4
```

## License
[Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0).
