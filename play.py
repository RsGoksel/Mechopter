import os
from math import sin, cos, pi, sqrt
from random import randrange

import pygame
from pygame.locals import *

import numpy as np
import gym
from gym import spaces

import Constants 
from Agent import Drone

WIDTH, HEIGHT = Constants.WIDTH, Constants.HEIGHT

TIME_LIMIT = Constants.TIME_LIMIT
BACKGROUND = Constants.BACKGROUND 

spriter = Constants.spriter #Image displayer

class droneEnv(gym.Env):
    def __init__(self):
        super(droneEnv, self).__init__()

        pygame.init()
        
            # VIDEO SETTINGS
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.FramePerSec = pygame.time.Clock()
    
        self.background = pygame.image.load(BACKGROUND)
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

            # Agent and Target SETTINGS
        self.Agent       = Drone()
        self.Agent_image = spriter("Drone")
        
        self.x_target = randrange(50, WIDTH - 50)
        self.y_target = randrange(75, HEIGHT - 75)
        self.target   = spriter("Baloon")

            # Font SETTINGS
        pygame.font.init()
        self.myfont = pygame.font.SysFont("Comic Sans MS", 20)
        
            # Physical CONSTANTS
        self.FPS         =  Constants.FPS
        self.gravity     = Constants.gravity
        self.thruster_amplitude = Constants.thruster_amplitude
        self.diff_amplitude     = Constants.diff_amplitude
        self.thruster_mean      = Constants.thruster_mean
        self.mass        = Constants.mass
        self.arm         = Constants.arm

            # GAME CONFIGURE
        self.target_counter = 0
        self.reward = 0
        self.time = 0
        self.pace = 0
        
            
    def reset(self):
        
        self.Agent.reset()
        
        self.x_target = randrange(50, WIDTH - 50)
        self.y_target = randrange(75, HEIGHT - 75)

        self.target_counter = 0
        self.reward = 0
        self.time = 0

        return 
    
    def move(self):
        
        self.render()
        self.reward = 0.0
        self.pace += 1
        self.pace %= 8
        
        self.time += 1 / 60

            # Initialize accelerations
        self.Agent.angular_acceleration = 0
        self.Agent.x_acceleration       = 0
        self.Agent.y_acceleration       = self.gravity

        thruster_left = self.thruster_mean
        thruster_right = self.thruster_mean

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            thruster_left += self.thruster_amplitude
            thruster_right += self.thruster_amplitude
            
        if pressed_keys[K_DOWN]:
            thruster_left -= self.thruster_amplitude
            thruster_right -= self.thruster_amplitude
            
        if pressed_keys[K_LEFT]:
            thruster_left -= self.diff_amplitude
        
        if pressed_keys[K_RIGHT]:
            thruster_right -= self.diff_amplitude

        
        # Calculating accelerations with Newton's laws of motions (F = M.A)(RIP Newton)
        self.Agent.x_acceleration += (
            -(thruster_left + thruster_right) * sin(self.Agent.angle * pi / 180) / self.mass
        )
        self.Agent.y_acceleration += (
            -(thruster_left + thruster_right) * cos(self.Agent.angle * pi / 180) / self.mass
        )

        self.Agent.angular_acceleration += self.arm * (thruster_right - thruster_left) / self.mass

        self.Agent.x_speed       += self.Agent.x_acceleration
        self.Agent.y_speed       += self.Agent.y_acceleration
        self.Agent.angle_speed   += self.Agent.angular_acceleration
        self.Agent.x_position    += self.Agent.x_speed
        self.Agent.y_position    += self.Agent.y_speed
        self.Agent.angle         += self.Agent.angle_speed

            # Euclidean distance between Agent and Target 
        dist = sqrt((self.Agent.x_position - self.x_target) ** 2 + (self.Agent.y_position - self.y_target) ** 2)

        if dist < 40:
            # Reward if agent closes to target
            self.x_target = randrange(50, WIDTH - 50)
            self.y_target = randrange(75, HEIGHT - 75)
            self.reward += 1

        # If times up
        if self.time > TIME_LIMIT:
            done = True
            return self.reward, done

        if self.Agent.x_position < -50 or self.Agent.x_position > WIDTH + 50 or self.Agent.y_position < -50 or self.Agent.y_position > HEIGHT + 50:
            self.reward -= 2
            done = True
            
            return self.reward, done

        return self.reward, 0


    def render(self):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                
        
        self.screen.blit(self.background, (0, 0))
        
        target_sprite = self.target[int(self.pace * 0.1) % len(self.target)]
        self.screen.blit(
            target_sprite,
            (
                self.x_target - int(target_sprite.get_width() / 2),
                self.y_target - int(target_sprite.get_height() / 2),
            ),
        )
        
        player_sprite = self.Agent_image[int(self.pace * 0.1) % len(self.Agent_image)]
        player_copy   = pygame.transform.rotate(player_sprite, self.Agent.angle)
        self.screen.blit(
            player_copy,
            (
                self.Agent.x_position - int(player_copy.get_width() / 2),
                self.Agent.y_position - int(player_copy.get_height() / 2),
            ),
        )

        textsurface = self.myfont.render(
            "Collected: " + str(self.target_counter), False, (0, 0, 0)
        )
        self.screen.blit(textsurface, (20, 20))
        textsurface3 = self.myfont.render(
            "Time: " + str(int(self.time)), False, (0, 0, 0)
        )
        self.screen.blit(textsurface3, (20, 50))

        pygame.display.update()
        self.FramePerSec.tick(120)

    def close(self):
        pass

    
env = droneEnv()

episode = 0


done = False
score = 0

for i in range(10):
    try:
        env.reset()
        done = False  # Initialize done here
        while not done:
            score, done = env.move()

        episode += 1
        print('Episode: {} Score: {}'.format(episode, score))
    except:
        pass
        
    
pygame.display.quit()
pygame.quit()