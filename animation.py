class Animator:
    """ A class to manaqge the animation for each specific sprite"""
    
    def __init__(self, **animations):
        """
        Initializes all the animations for the sprite
        :param **animations: a dictionary with the animation as 
        keys and values (frames, next_anim, frame_duration)
        """
        self._animations = animations
        self._curr_anim = None
        self._curr_anim_frames = None
        
        self._current_frame = None
        self._frame_duration = None
        self._next_anim = None
    
    def set_curr_anim(self, curr_anim):
        """
        Sets the animator to play the current desired animation from the first frame
        :param curr_anim: the current animation to play as a str
        :param frame_duration: the number of frames to display a frame for
        """
        self._next_anim = self._animations[curr_anim][1]
        self._curr_anim = curr_anim
        self._curr_anim_frames = iter(self._animations[self._curr_anim][0])
        
        self._curr_frame = next(self._curr_anim_frames)
        self._frame_duration = self._animations[curr_anim][-1]
        
    def _get_flipped_anim_x(self, sprite_x, sprite_w):
        """Returns the x coordinate of the flipped sprite as if the
           reflection line was through the midpoint of the sprite"""        
        return -(sprite_x + sprite_w)

    def play(self, sprite_x, sprite_y, sprite_w, sprite_h, direction_x):
        try:
            pushMatrix()
            scale(direction_x, 1)
            if direction_x == -1:
                sprite_x = self._get_flipped_anim_x(sprite_x, sprite_w)
            
            if frameCount % self._frame_duration == 0:
                try:
                    self._curr_frame = next(self._curr_anim_frames)
                except StopIteration:
                    if self._next_anim:
                        self.set_curr_anim(self._next_anim)
                        return
                    self._curr_anim_frames = iter(self._animations[self._curr_anim][0])
                    self._curr_frame = next(self._curr_anim_frames)
                image(self._curr_frame, sprite_x, sprite_y, sprite_w, sprite_h)
            else:
                image(self._curr_frame, sprite_x, sprite_y, sprite_w, sprite_h)
            popMatrix()
        except Exception:
            pass
        
    @property
    def curr_anim(self):
        return self._curr_anim
    
