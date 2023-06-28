class Settings:
    FRAME_RATE = 60
    
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    
    game_font = None
    
    @classmethod
    def initialize_game_font(cls):
        cls.game_font = createFont("Roboto-Regular.ttf", 16, True)
    
