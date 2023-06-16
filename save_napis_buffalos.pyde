from game_ui import GameUI
from game_settings import Settings


add_library('minim')


def setup():
    global gameUI
    gameUI = GameUI(this)
    gameUI.setup()
    
    minim = Minim(this)
    game_song = minim.loadFile("game music.mp3")
    #game_song.loop()
    size(Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT, P2D)


def draw():
    gameUI.draw()
    
def mousePressed():
    gameUI.mousePressed()
    
def keyPressed():
    gameUI.keyPressed()

def keyReleased():
    gameUI.keyReleased()
