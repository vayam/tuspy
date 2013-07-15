# tuspy

[TUS Protocol 0.2.1](http://www.tus.io/protocols/resumable-upload.html) Client Implementation

## Installation
```
pip install requests
pip install pycurl
```

## Configuration
```
Modify CREATE_ENDPT = "http://master.tus.io/files/" in  config.py
```

## Run

```
Usage: tuspy.py [options]

Options:
  -h, --help            show this help message and exit
  -f FILENAME, --file=FILENAME
                        file to upload
  -u UPLOAD_SPEED, --upload_speed=UPLOAD_SPEED
                        upload speed in bytes per second
```

## Example
```
wget http://download.blender.org/peach/bigbuckbunny_movies/BigBuckBunny_640x360.m4v
python tuspy.py -f BigBuckBunny_640x360.m4v
```

## License
[Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0).
