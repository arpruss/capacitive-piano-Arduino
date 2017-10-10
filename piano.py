import pygame.midi
import pygame
import time
import serial
from sys import argv,version_info
from time import sleep

notes = [60, 62, 64, 65, 67, 69, 71, 72 ]
noteNames = ["C", "D", "E", "F", "G", "A", "B", "C"]
playing = [False for i in range(len(notes))]
width = 800
height = 600
keyWidth = width//len(notes)
WHITE = (255,255,255)
BLACK = (0,0,0)
ONE = ord('1') if version_info[0] >= 3 else '1'

ser = serial.Serial("com7" if len(argv)<2 else argv[1], baudrate=115200, timeout=5)

def drawKeys():
    for i in range(len(notes)):
        x = keyWidth * i
        pygame.draw.rect(screen, BLACK if playing[i] else WHITE, [x,0,keyWidth,height], 0)
        pygame.draw.rect(screen, WHITE if playing[i] else BLACK, [x,0,keyWidth,height], 2)
        size = font.size(noteNames[i])
        screen.blit(font.render(noteNames[i],1,
            (255,255,255) if playing[i] else (0,0,0)), (x+keyWidth/2-size[0]/2,height*3/4-size[1]/2))
    pygame.display.flip()   

pygame.init()
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Piano")
font = pygame.font.Font(None,30)
drawKeys()
sleep(10)

pygame.midi.init()

midiOut = pygame.midi.Output(0)

try:
    while True:
        line = ser.readline().strip()
        for i in range(min(len(notes),len(line))):
            state = line[i] == ONE
            if state != playing[i]:
                if state:
                    midiOut.note_on(notes[i], 127)
                    playing[i] = True
                    print(noteNames[i])
                else:
                    playing[i] = False
                    midiOut.note_off(notes[i], 127)
                drawKeys()
except serial.SerialException:
    print("Disconnected!")

midiOut.close()
pygame.quit()
