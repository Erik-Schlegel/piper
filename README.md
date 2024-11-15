
# Piper

Pi-based audio player geared toward providing uninterrupted audio ambience. Exposes a webapp for live control.

## Setup
in a terminal, run `./install`


## Dev Notes


### Play single audio file using Sox; set volume and reverb
```sh
play test.mp3 vol 0.15 reverb 90
```


### Pip stuff

#### Adding a new pip requirement
```sh
source venv/bin/activate
pip install whatever...

# Replace requirements.txt. Include only the packages loaded in venv
pip freeze --local > requirements.txt
deactivate
```



## Seamless loop audio file
We prepare a single file which has a crossfade (with itself) at the beginning and the end

```sh
#start at 10, then 30 seconds from there
sox file.mp3 file_trimmed.mp3 trim 10 30
sox file_trimmed.mp3 file_trimmed.mp3 file_trimmed.mp3 file_concatenated.mp3
sox file_concatenated.mp3 file_spliced.mp3 splice 27,3 splice 57,3
sox file_spliced.mp3 file_final.mp3 trim 30 30
```