from game_ui import GameUI
from game_settings import Settings
import threading

add_library('minim')


def setup():
    global gameUI
    gameUI = GameUI(this, Minim(this))
    gameUI.setup()

    size(Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT, P2D)

    
def draw():
    gameUI.draw()

def stop():
    gameUI.stop()
#def mousePressed():
    #print(mouseX, mouseY)
    #gameUI.mousePressed()
    
def keyPressed():
    gameUI.keyPressed()

def keyReleased():
    gameUI.keyReleased()
