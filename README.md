
# Piper

Pi-based audio player geared toward providing uninterrupted bespoke audio ambience.


## Setup
Run `./install`


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


### Connect Pi to Bluetooth device
```sh
   bluetoothctl
   power on
   agent on
   scan on
   # Note MAC address: Device F0:41:C8:3C:24:FC BT HIFI AUDIO
   pair XX:XX:XX:XX:XX:XX
   trust XX:XX:XX:XX:XX:XX
   connect XX:XX:XX:XX:XX:XX

```