
# Piper

Pi-based audio player geared toward providing uninterrupted audio ambience.


## Setup for local development and iteration
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
            "name": "background", // unique string
            "play_mode": "", // "sequential", "shuffled", "simultaneous"
            "loop": true,
                /*
                sequential & true - full playlist is repeated
                sequential & false - full playlist plays once
                -
                shuffled & true - full playlist loops, each loop is uniquely shuffled
                shuffled & false - full playlist is shuffled then plays once
                -
                simultaneous & true - all tracks play simultaneously, individual tracks loop
                simultaneous & false - all tracks play simultaneously, individual tracks play once
                */
            "intermission": 0,
                // in seconds.
                // Negative number: crossfade time
                // Individual number value: static gap time between tracks in this set
                // List of two numbers [ minValue, maxValue ] imposes a wait-to-start-next-track for n seconds. N is a random number between min and max.
            "audio_options": {
                "volume": 0.25, // 0 - 1
                "equalizers": [
                    {
                        "name": "lowshelf", // equalizer values for all tracks to inherit.
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
