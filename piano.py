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
ZERO = ord('0') if version_info[0] >= 3 else '0'

if len(argv) >= 2 and argv[1] == "--no-serial":
    ser = None
else:
    port = "com7" if len(argv)<2 else argv[1]
    print("Connecting to "+port)
    ser = serial.Serial(port, baudrate=115200, timeout=5)
    ser.readline() # skip a potential partial line

def drawKeys():
    for i in range(len(notes)):
        x = keyWidth * i
        pygame.draw.rect(screen, BLACK if playing[i] else WHITE, [x,0,keyWidth,height], 0)
        pygame.draw.rect(screen, WHITE if playing[i] else BLACK, [x,0,keyWidth,height], 2)
        size = font.size(noteNames[i])
        screen.blit(font.render(noteNames[i],1,
            (255,255,255) if playing[i] else (0,0,0)), (x+keyWidth/2-size[0]/2,height*3/4-size[1]/2))
    pygame.display.flip()   

print("MIDI setup")
pygame.midi.init()
midiOut = pygame.midi.Output(0)

print("Screen setup")
pygame.init()
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Piano")
font = pygame.font.Font(None,30)
drawKeys()

done = False

previousLine = [ZERO for i in range(len(notes))]

mouseNote = None

def noteOn(i):
    midiOut.note_on(notes[i], 127)
    playing[i] = True
    print(noteNames[i])
    
def noteOff(i):
    playing[i] = False
    midiOut.note_off(notes[i], 127)

try:
    while not done:
        changed = False
        if ser is None:
            line = previousLine
        else:
            line = ser.readline().strip()
        for i in range(min(len(notes),len(line))):
            if previousLine[i] != line[i]:
                if line[i] == ONE:
                    noteOn(i)
                else:
                    noteOff(i)
                changed = True
        previousLine = line
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if mouseNote is not None:
                    noteOff(mouseNote)
                mouseNote = event.pos[0] // keyWidth
                if mouseNote < len(notes):
                    noteOn(mouseNote)
                else:
                    mouseNote = None
                changed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if mouseNote is not None:
                    noteOff(mouseNote)
                    mouseNote = None
                changed = True
                    
        if changed:
            drawKeys()
                
                
except serial.SerialException:
    print("Disconnected!")

midiOut.close()
pygame.quit()
