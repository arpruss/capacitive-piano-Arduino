import pygame.midi
import time
import serial
from sys import argv

ser = serial.Serial("com7" if len(argv)<2 else argv[1], baudrate=115200, timeout=5)

notes = [60, 62, 64, 65, 67, 69, 71, 72 ];
noteNames = ["C", "D", "E", "F", "G", "A", "B", "C"];
playing = [False for i in range(len(notes))];

pygame.midi.init()

midiOut = pygame.midi.Output(0)

while True:
    line = ser.readline().strip()
    #print(line)
    for i in range(min(len(notes),len(line))):
        state = line[i] == ord('1')
        if state != playing[i]:
            if state:
                midiOut.note_on(notes[i], 127)
                playing[i] = True
                print(noteNames[i])
            else:
                playing[i] = False
                midiOut.note_off(notes[i], 127)

midiOut.close()
