from core import Entity, GridDisplayManager
import pygame

# class representing point with potential mass
class PotentialUnit():
    def __init__(self, offset, Q):
        self.offset = offset # Offset from position to unit 
        self.Q = Q           # Potential mass


class PotentialEntity(Entity):
    def __init__(self):
        super().__init__()
        self.PU = []
    
class Ball(Entity):
    def __init__(self, pos, size=(0.2, 0.2), color=(255,255,255), ):
        super().__init__()
        self._color = color
        self._size  = size
        self.set_pos(pos)
        self.set_name("Ball")

    def display(self, canvas):
        x, y = GridDisplayManager.tf_g2d_pos(self._pos)
        w, h = GridDisplayManager.tf_g2d_size(self._size)
        pygame.draw.ellipse(canvas, self._color, (int(x-h/2), int(y-w/2), w, h))

class Allie(PotentialEntity):
    def __init__(self, pos, size=(0.5, 0.5), PU=[PotentialUnit((0,0), 0)], color=(0,0,255)):
        super().__init__()
        self._color = color
        self._size  = size
        self.set_pos(pos)
        self.set_name("Noname allie")
        self.PU = PU

    def display(self, canvas):
        x, y = GridDisplayManager.tf_g2d_pos(self._pos)
        w, h = GridDisplayManager.tf_g2d_size(self._size)
        pygame.draw.ellipse(canvas, self._color, (int(x-h/2), int(y-w/2), w, h))

class Opponent(PotentialEntity):
    def __init__(self, pos, size=(0.5, 0.5), PU=[PotentialUnit((0,0), -0.5)], color=(255,0,0)):
        super().__init__()
        self._color = color
        self._size  = size
        self.set_pos(pos)
        self.set_name("Noname opponent")
        self.PU = PU

    def display(self, canvas):
        x, y = GridDisplayManager.tf_g2d_pos(self._pos)
        w, h = GridDisplayManager.tf_g2d_size(self._size)
        pygame.draw.ellipse(canvas, self._color, (int(x-h/2), int(y-w/2), w, h))

class Target(PotentialEntity):
    def __init__(self, pos, size=(0.5, 0.5), PU=[PotentialUnit((0,0), 5)], color=(100,100,100)):
        super().__init__()
        self._color = color
        self._size  = size
        self.set_pos(pos)
        self.set_name("Target")
        self.PU = PU

    def display(self, canvas):
        x, y = GridDisplayManager.tf_g2d_pos(self._pos)
        w, h = GridDisplayManager.tf_g2d_size(self._size)
        pygame.draw.ellipse(canvas, self._color, (int(x-h/2), int(y-w/2), w, h))

class Arrow(Entity):
    def __init__(self, start_pos, end_pos, color = (255,0,0)):
        self._start_pos = start_pos
        self._end_pos   = end_pos
        self._color     = color

    def display(self, canvas):
        p1 = GridDisplayManager.tf_g2d_pos(self._start_pos)
        p2 = GridDisplayManager.tf_g2d_pos(self._end_pos)
        
        pygame.draw.line(canvas, self._color, p1, p2, 3)