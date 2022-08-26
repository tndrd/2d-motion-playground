#from html import entities
#from turtle import screensize
from cmath import sin
from core  import Playground
from entities import Ball, Arrow, Allie, Target, Opponent
import time
from math import sqrt, isnan, sin, cos
import numpy as np

class PotentialAlgorythms:
    
    # Evaluates field potential in point
    # Formule: potential = sum(Qn/rn), where:
    # Qn is potential mass of some entity, and
    # rn is distance from desired point to some this entity
    @staticmethod
    def evaluate_potential(pos, p_entities):
        potential = 0
        
        for p_entity in p_entities:
            dr = pos - np.array(p_entity.get_pos())
            dx = dr[0]
            dy = dr[1]
            r  = sqrt(dx**2 + dy**2)
            
            potential += p_entity.PU[0].Q/r
        return potential


    # evaluetes field strength vector in point
    # Formule: E = -grad(potential)
    @staticmethod
    def evaluate_field_strength(pos, p_entities):
        pos = np.array(pos)
        
        grad_x = 0
        grad_y = 0

        for entity_group in p_entities:
            for p_entity in entity_group:
                dr = pos - np.array(p_entity.get_pos())
                dx = dr[0]
                dy = dr[1]
                r  = sqrt(dx**2 + dy**2)

                if r == 0.0:
                    continue

                grad_x += p_entity.PU[0].Q * (dx / r**3)
                grad_y += p_entity.PU[0].Q * (dy / r**3)
        return np.array([-grad_x, -grad_y])



class PotentialFunctionsPlayground(Playground):
    def __init__(self, gridsize, screensize, entities):
        super().__init__(gridsize, screensize, entities)

    def additional_draw(self):
        return self.get_potential_field()

    def get_potential_field(self):    
        p_entities = self.entities["potential"].values()
        arrows = []

        gridsize, _    = self.get_playground_size()
        grid_w, grid_h = gridsize
        for grid_y in range(grid_h):
            for grid_x in range(grid_w):
                grad = PotentialAlgorythms.evaluate_field_strength((grid_x, grid_y), p_entities)

                r  = sqrt(grad[0]**2 + grad[1]**2)
                if r < 0.0001:
                    continue
                
                grad = grad / r
                if isnan(grad[0]) or isnan(grad[1]):
                    continue

                start_pos = (grid_x, grid_y)
                arrow = Arrow(start_pos, start_pos + grad * 0.5)
                arrows.append(arrow)
        return arrows

    def ballstep(self, speed):
        pos = self.entities["simple"]["ball"][0].get_pos()
        
        grad = PotentialAlgorythms.evaluate_field_strength(pos, self.entities["potential"].values())

        r  = sqrt(grad[0]**2 + grad[1]**2)
        if r < 0.0001:
            return
        
        grad = grad / r
        if isnan(grad[0]) or isnan(grad[1]):
            return
        
        pos = pos + speed * grad
        self.entities["simple"]["ball"][0].set_pos(pos)


    def play(self):
        time.sleep(2)
        t = 0
        pos = self.entities["potential"]["opponents"][0].get_pos()
        while self._canvas.active():
            self.ballstep(0.005)
            dr = (1.5 * sin(0.01 * t), 0)
            
            self.entities["potential"]["opponents"][0].set_pos(pos+dr)

            t+=1
            time.sleep(0.001)

if __name__ == "__main__":
    aent = {}
    aent["potential"] = {}
    aent["simple"]    = {}

    aent["simple"]["ball"]   = [Ball((8,1))]
    aent["potential"]["target"] = [Target((8,15))]

    aent["potential"]["allies"]    = [Allie((8,2))]
    aent["potential"]["opponents"] = [Opponent((8.5, 10)), Opponent((4, 10))]

    playground = PotentialFunctionsPlayground((16, 16), (1000, 1000), aent)

    