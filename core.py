from turtle import screensize
import pygame
from threading import Thread
import time
import numpy as np

class GridDisplayManager:
    
    class Grid:
        Width  = None
        Height = None

    class Screen:
        Width  = None
        Height = None

    @staticmethod
    def init(gridsize, screensize):
        GridDisplayManager.Grid.Width    = gridsize[0]
        GridDisplayManager.Grid.Height   = gridsize[1]
        GridDisplayManager.Screen.Width  = screensize[0]
        GridDisplayManager.Screen.Height = screensize[1]

    @staticmethod
    def tf_g2d_x(coord):
        return int((float(coord) / GridDisplayManager.Grid.Width)  * GridDisplayManager.Screen.Width)

    @staticmethod
    def tf_g2d_y(coord):
        return int((float(coord) / GridDisplayManager.Grid.Height)  * GridDisplayManager.Screen.Height)

    # transforms grid coordinates into display coordinates
    @staticmethod
    def tf_g2d_pos(pos_in_grid):
        disp_x = GridDisplayManager.tf_g2d_x(pos_in_grid[0])
        disp_y = GridDisplayManager.Screen.Height - GridDisplayManager.tf_g2d_y(pos_in_grid[1])
        return (disp_x, disp_y)

    @staticmethod
    def tf_g2d_size(size_in_grid):
        disp_x = GridDisplayManager.tf_g2d_x(size_in_grid[0])
        disp_y = GridDisplayManager.tf_g2d_y(size_in_grid[1])
        return (disp_x, disp_y)

    @staticmethod
    def screensize():
        return GridDisplayManager.Screen.Width, GridDisplayManager.Screen.Height

    @staticmethod
    def gridsize():
        return GridDisplayManager.Grid.Width, GridDisplayManager.Grid.Height


class Entity():
    def __init__(self):
        self._name  = None
        self._state = None
        self._pos   = None

    def set_pos(self, pos):
        self._pos  = np.array(pos)
    def set_name(self,name):
        self._name = name

    def get_pos(self):
        return self._pos
    def get_name(self):
        return self._name

    def display(self, canvas):
        print("Error: displaying empty entity")


class Canvas():
    def __init__(self, background_color=(0, 255, 0)):
        self._active     = False
        self._bg_color   = background_color
        self._entities   = []

        pygame.init()
        self.start()
        
        self._screen = pygame.display.set_mode(GridDisplayManager.screensize())

    def _draw_grid_mesh(self):

        screen_w, screen_h = GridDisplayManager.screensize()
        grid_w, grid_h     = GridDisplayManager.gridsize()

        for x_grid in range(1, grid_w):
            x_disp = GridDisplayManager.tf_g2d_x(x_grid)
            pygame.draw.line(self._screen, (0,200,0), [x_disp, 0], [x_disp, screen_h], 1)

        for y_grid in range(1, grid_h):
            y_disp = GridDisplayManager.tf_g2d_y(y_grid)
            pygame.draw.line(self._screen, (0,200,0), [0, y_disp], [screen_w, y_disp], 1)

    def _display_tick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   
                self._active = False
       
        self._screen.fill(self._bg_color)

        self._draw_grid_mesh()

        for entity in self._entities:
            entity.display(self._screen)

        pygame.display.flip()

    def display_loop(self):
        print("Display loop started")
        while self._active:
            self._display_tick()

    def active(self):
        return self._active

    def start(self):
        self._active = True

    def stop(self):
        self._active = False
        pygame.quit()

    def update(self, entities):
        self._entities = entities


class Playground():
    def __init__(self, gridsize, screensize, entities):
        GridDisplayManager.init(gridsize, screensize)
        self._canvas   = Canvas()
        self.entities = entities 
        
        self._draw_thread = Thread(target=self._draw)
        self._play_thread = Thread(target=self.play)
        self._draw_thread.start()
        self._play_thread.start()

        self._canvas.display_loop()

    def get_playground_size(self):
        return GridDisplayManager.gridsize(), GridDisplayManager.screensize()

    def additional_draw(self):
        return []

    def play(self): pass

    def _draw(self):
        print("Starting playground...")
        time.sleep(1)
        while self._canvas.active():

            p_entities = self.entities["potential"].values()
            s_entities = self.entities["simple"].values()

            entities_to_draw = []

            for entity_group in p_entities:
                for entity in entity_group:
                    entities_to_draw.append(entity)

            for entity_group in s_entities:
                for entity in entity_group:
                    entities_to_draw.append(entity)

            additional_drawings = self.additional_draw()
            entities_to_draw.extend(additional_drawings)
            
            self._canvas.update(entities_to_draw)