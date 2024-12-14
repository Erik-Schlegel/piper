
# Piper

Pi-based audio player geared toward providing uninterrupted audio ambience.


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


## Configuration Options
```json
{
    "layer_sets": [
        {
            "name": "background", // unique, optional
            "play_mode": "string", // "simultaneous", "ordered", "shuffled"
            "loops": true, //boolean

            "intermission": -0.25, // in seconds. negative represents crossfade time, single value is static gap between tracks, [ minValue, maxValue ] is a random gap between plays
            "audio_options": {
                "volume": 0.25, // 0 - 1
                "equalizers": [
                    {
                        "name": "lowshelf", // equalizer values for all tracks to inherit. If track has an equalizer of the same name, the track's value overrides
                        "frequency": 100,
                        "gain": 13 // decibels
                    }
                ]
            },
            "tracks": [
                {}
            ]
        }
    ]
}
```
