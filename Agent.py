import pygame
import Constants
import os

# Screen
WIDTH, HEIGHT =  Constants.WIDTH, Constants.HEIGHT


class Drone(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.reset()
        
        
    def reset(self):
        
        # Reset variables
        (self.angle, self.angle_speed, self.angular_acceleration) = (0, 0, 0)
        (self.x_position, self.x_speed, self.x_acceleration)      = (int(WIDTH/2) , 0, 0)
        (self.y_position, self.y_speed, self.y_acceleration)      = (int(HEIGHT/2), 0, 0)