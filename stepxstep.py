import pygame
import pygame.midi
import time
import random

pygame.init()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 255)

WIDTH = 1380 # window dimension
HEIGHT = 768 # window dimension
windowSurface = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('stepXstep') # window caption

#initialize midi system
midi_instrument=46
pygame.midi.init()
print(pygame.midi.get_default_output_id()) # -1
player = pygame.midi.Output(2)
player.set_instrument(midi_instrument)

KeepGoing=True # event loop
Playing=False # playback
index=0
X=0 # current position
Y=0 # current position
WIDTH=32
HEIGHT=15
STARTX=75
STARTY=100
BUTTON_D=35
SPACE_D=BUTTON_D+5
Cscale=[72,71,69,67,65,64,62,60,59,57,55,53,52,50,48]
bpm=240
Loudness=50

Matrix = [[False for x in range(HEIGHT)] for y in range(WIDTH)] 

def do_note(note, duration, volume):
    player.note_on(note, volume)
    time.sleep(duration)
    player.note_off(note, volume)

def do_note_down(note, duration, volume):
    player.note_on(note, volume)

def do_note_up(note, duration, volume):
    player.note_off(note, volume)

def DrawScreen(screen):
    screen.fill(BLACK)    
    # initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
    myfont=pygame.font.SysFont("monospace", 45)
    # render text
    label=myfont.render("MIDI Code Experiments", 1, (255,255,0))
    screen.blit(label, (10, 10))
    buffer="Instument: "+str(midi_instrument)
    Instrument = myfont.render(buffer, 1, (255,255,0))
    screen.blit(Instrument, (10, 50))
    buffer="BPM: "+str(bpm)
    Rhythm=myfont.render(buffer, 1, (255,255,0))
    screen.blit(Rhythm, (400, 50))
    for i in range (0,WIDTH):
        for j in range (0,HEIGHT):
            if (Matrix[i][j]==False):
                pygame.draw.rect(screen,BLUE,(STARTX+(i*SPACE_D),STARTY+(j*SPACE_D),BUTTON_D,BUTTON_D), 0)
            else:
               pygame.draw.rect(screen,RED, (STARTX+(i*SPACE_D),STARTY+(j*SPACE_D),BUTTON_D,BUTTON_D), 0)
            
    pygame.draw.rect(screen,GREEN, (STARTX+(index*SPACE_D),STARTY,BUTTON_D,BUTTON_D+((HEIGHT-1)*SPACE_D)), 2) # playback index
    pygame.draw.rect(screen,YELLOW, (STARTX+(X*SPACE_D),STARTY+(Y*SPACE_D),BUTTON_D,BUTTON_D), 2) # current position
    
    pygame.display.flip()

def MouseClick(pos):
    print(pos)
    indexX=-1
    indexY=-1
    for i in range (0,WIDTH):
        for j in range (0,HEIGHT):
            if ((pos[0]>(STARTX+(i*SPACE_D))) and
                (pos[0]<(STARTX+((i+1)*SPACE_D))) and
                (pos[1]>(STARTY+(j*SPACE_D))) and
                (pos[1]<(STARTY+((j+1)*SPACE_D)))):
                indexX=i
                indexY=j
                Matrix[i][j]=not Matrix[i][j]
    
    
def Playback(index, duration, volume):
    print(index)
    for j in range (0,HEIGHT):
        if (Matrix[index][j]==True):
            player.note_on(Cscale[j], volume)
    time.sleep(duration)
    for j in range (0,HEIGHT):
        if (Matrix[index][j]==True):
            player.note_off(Cscale[j], volume)
    
#event loop
while (KeepGoing==True):

    if (Playing==True):
        Playback(index, (60.0/bpm), Loudness)
        index=(index+1)%WIDTH
        DrawScreen(windowSurface)
    else:
        DrawScreen(windowSurface)
        time.sleep(0.2)


        
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            print("Quit")
            KeepGoing=False
        elif event.type == pygame.MOUSEBUTTONUP:
            MouseClick(event.pos)
        elif event.type == pygame.KEYDOWN:
            print(event.key)
            if event.key == pygame.K_ESCAPE:
                print("Quit")
                KeepGoing=False
            elif event.key == pygame.K_LEFT:
                if (X>0):
                    X=X-1
            elif event.key == pygame.K_RIGHT:
                if (X<(WIDTH-1)):
                    X=X+1
            elif event.key == pygame.K_UP:
                if (Y>0):
                    Y=Y-1
            elif event.key == pygame.K_DOWN:
                if (Y<(HEIGHT-1)):
                    Y=Y+1
            elif event.key == pygame.K_RETURN:
                print(X,Y)
                Matrix[X][Y]=not (Matrix[X][Y]);
            elif event.key == pygame.K_SPACE:
                Playing=not Playing
            elif event.key == pygame.K_EQUALS:
                midi_instrument=(midi_instrument+1)%128
                player.set_instrument(midi_instrument)                
            elif event.key == pygame.K_MINUS:
                midi_instrument=(midi_instrument-1)%128
                player.set_instrument(midi_instrument)
            elif event.key == pygame.K_a:
                if (bpm>20):
                    bpm=bpm-10
            elif event.key == pygame.K_s:
                if (bpm<800):
                    bpm=bpm+10
            elif event.key == pygame.K_1:
                do_note_down(60, 1, Loudness) #C4
            elif event.key == pygame.K_2:
                do_note_down(62, 1, Loudness) #D
            elif event.key == pygame.K_3:
                do_note_down(64, 1, Loudness) #E
            elif event.key == pygame.K_4:
                do_note_down(65, 1, Loudness) #F
            elif event.key == pygame.K_5:
                do_note_down(67, 1, Loudness) #G
            elif event.key == pygame.K_6:
                do_note_down(69, 1, Loudness) #A
            elif event.key == pygame.K_7:
                do_note_down(71, 1, Loudness) #B
            elif event.key == pygame.K_8:
                do_note_down(72, 1, Loudness) #C5
            elif event.key == pygame.K_9:
                do_note_down(74, 1, Loudness) #D
            elif event.key == pygame.K_0:
                do_note_down(76, 1, Loudness) #E
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_1:
                do_note_up(60, 1, Loudness) #C4
            elif event.key == pygame.K_2:
                do_note_up(62, 1, Loudness) #D
            elif event.key == pygame.K_3:
                do_note_up(64, 1, Loudness) #E
            elif event.key == pygame.K_4:
                do_note_up(65, 1, Loudness) #F
            elif event.key == pygame.K_5:
                do_note_up(67, 1, Loudness) #G
            elif event.key == pygame.K_6:
                do_note_up(69, 1, Loudness) #A
            elif event.key == pygame.K_7:
                do_note_up(71, 1, Loudness) #B
            elif event.key == pygame.K_8:
                do_note_up(72, 1, Loudness) #C5
            elif event.key == pygame.K_9:
                do_note_up(74, 1, Loudness) #D
            elif event.key == pygame.K_0:
                do_note_up(76, 1, Loudness) #E
# clean up before exit
del player
pygame.midi.quit()
pygame.quit()



