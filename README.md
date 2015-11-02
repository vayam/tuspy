# tuspy

[TUS Protocol 1.0.0](https://github.com/tus/tus-resumable-upload-protocol/blob/1.0/protocol.md) Client Implementation

## Installation
```
pip install requests
pip install pycurl
```

## Configuration
```
Modify CREATE_ENDPT = "http://localhost:1080/files/" in  config.py
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
