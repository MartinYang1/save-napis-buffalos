from game_ui import GameUI
from game_settings import Settings
import threading

add_library('minim')


def setup():
    global gameUI
    gameUI = GameUI(this, Minim(this))
    
    smooth()
    frameRate(Settings.FRAME_RATE)
    size(Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT, P2D)
    
    gameUI.setup()

    
def draw():
    gameUI.draw()

def stop():
    gameUI.stop()
    
def keyPressed():
    gameUI.keyPressed()

def keyReleased():
    gameUI.keyReleased()
