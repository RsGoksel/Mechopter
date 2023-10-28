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

os.system('cls' if os.name == 'nt' else 'clear') # Cleaning library loading information texts
print("Fetching Libraries.. Please Wait..")

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
        self.reward = 0
        self.time   = 0
        self.pace   = 0
        self.time_limit = 20
        self.target_counter = 0
        
            # GYM CONFIGURE
        self.action_space      = gym.spaces.Discrete(5)
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(6,), dtype=np.float16)
        
        self.info = {}
        Constants.report(self)
        
        """
        5 actions: 
            Nothing, Up, Down, Right, Left
        
        8 observations: 
            angle_to_up, 
            velocity, 
            angle_velocity, 
            distance_to_target, 
            angle_to_target, 
            angle_target_and_velocity, 
            distance_to_target
        """
    def reset(self):
        
        self.Agent.reset()
        self.x_target = randrange(50, WIDTH - 50)
        self.y_target = randrange(75, HEIGHT - 75)

        self.target_counter = 0
        self.reward = 0
        self.time   = 0

        return self.get_obs()

    def get_obs(self) -> np.ndarray:
        
        """
        Calculates the observations

        Returns:
            np.ndarray: The normalized observations:
            + angle_to_up : angle between the drone and the up vector (to observe gravity)
            + velocity : velocity of the drone
            + angle_velocity : angle of the velocity vector
            + distance_to_target : distance to the target
            + angle_to_target : angle between the drone and the target
            + angle_target_and_velocity : angle between the to_target vector and the velocity vector
            + distance_to_target : distance to the target
        """
        angle_to_up     = self.Agent.angle / 180 * pi#* 565.5 # ne gerek var
        velocity        = sqrt(self.Agent.x_speed**2 + self.Agent.y_speed**2)
        angle_velocity  = self.Agent.angle_speed
        angle_to_target = np.arctan2(self.y_target - self.Agent.y_position, self.x_target - self.Agent.x_position)
        
        # Angle between the to_target vector and the velocity vector
        angle_target_and_velocity = np.arctan2(self.y_target - self.Agent.y_position, self.x_target - self.Agent.x_position) - np.arctan2(self.Agent.y_speed, self.Agent.x_speed)
        
        distance_to_target = sqrt((self.x_target - self.Agent.x_position) ** 2 + (self.y_target - self.Agent.y_position) ** 2) / 500
        
        return np.array(
            [
                angle_to_up,
                velocity,
                angle_velocity,
                distance_to_target,
                angle_to_target,
                angle_target_and_velocity,
            ]
        ).astype(np.float16)

    def step(self, action):
        
        self.render()
        self.reward = 0.0
        self.pace += 1
        self.pace %= 20
        
        action = int(action)
            
        # Act every x frames. Range can be altered. 
        for _ in range(1):
            self.time += 1 / 60

                # Initialize accelerations
            self.Agent.angular_acceleration = 0
            self.Agent.x_acceleration       = 0
            self.Agent.y_acceleration       = self.gravity
            
            thruster_left  = self.thruster_mean
            thruster_right = self.thruster_mean

            if action == 0:
                pass
            
            elif action == 1:
                thruster_left  += self.thruster_amplitude
                thruster_right += self.thruster_amplitude
                
            elif action == 2:
                thruster_left  -= self.thruster_amplitude
                thruster_right -= self.thruster_amplitude
                
            elif action == 3:
                thruster_left  += self.diff_amplitude
                thruster_right -= self.diff_amplitude
                
            elif action == 4:
                thruster_left  -= self.diff_amplitude
                thruster_right += self.diff_amplitude

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

                # Reward per step if survived
            self.reward += 1 / 60
            
                # Penalizing to the distance to target (0.00016 is for normalize)
            self.reward -= dist * 0.000166 # (100*60)

            if dist < 45:
                # Reward if agent closes to target
                self.x_target = randrange(50, WIDTH - 50)
                self.y_target = randrange(75, HEIGHT - 75)
                self.reward += 100
                self.target_counter += 1
        
            # If times up
            if self.time > self.time_limit:
                done = True
                return self.get_obs(), self.reward, done, self.info

            #dist > 1000: 
            if self.Agent.x_position < -50 or self.Agent.x_position > WIDTH + 50 or \
                self.Agent.y_position < -50 or self.Agent.y_position > HEIGHT + 50: 
                        
                self.reward -= 800
                done = True
                return self.get_obs(), self.reward, done, self.info

        return self.get_obs(), self.reward, False, self.info

    def render(self):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                del(self)
                quit()
                
        self.screen.blit(self.background, (0, 0))
        
        target_sprite = self.target[int(self.pace * 0.15) % len(self.target)]
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

        textsurface = self.myfont.render("Collected: " + str(self.target_counter), False, (0, 0, 0))
        textsurface3 = self.myfont.render("Time: " + str(int(self.time)), False, (0, 0, 0))
        self.screen.blit(textsurface, (20, 20))
        self.screen.blit(textsurface3, (20, 50))

        pygame.display.update()
        #self.FramePerSec.tick(self.FPS)

    def close(self):
        pass
