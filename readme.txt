Requires the marti2250 no-component capacitive touch library:
    https://github.com/martin2250/ADCTouch

Attach A0-A7 to pads, fruit, cans, etc. Turn on Arduino with sketch. Wait for the LED to turn off. Then run:
    python piano.py com-port
on a connected computer to get polyphonic sound. (Make sure you have pygame installed. If not, python -m pip install pygame)

