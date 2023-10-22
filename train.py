# Author: RsGoksel

print("Libraries Loading, please wait...")

import sys
import pygame
import traceback
import logging

import Constants

from stable_baselines3 import A2C #PPO, DQN also can be used 

from env import droneEnv
env = droneEnv()

tensorboard_log_path   = Constants.tensorboard_log
tensorboard_sub_folder = Constants.tensorboard_sub_folder

learning_rate   = Constants.learning_rate 
ent_coef        = Constants.ent_coef
gamma           = Constants.gamma 
gae_lambda      = Constants.gae_lambda
max_grad_norm   = Constants.max_grad_norm

total_timesteps = Constants.total_timesteps

try:
    # In addition to PPO, A2C and DQN are also viable options.
    model = A2C('MlpPolicy',
                env,
                learning_rate   = learning_rate,
                ent_coef        = ent_coef, 
                gamma           = gamma, 
                gae_lambda      = gae_lambda,
                max_grad_norm   = max_grad_norm,
                verbose         = 0, 
                tensorboard_log = tensorboard_log_path)
    
    model.learn(total_timesteps = total_timesteps, 
                callback        = None, 
                log_interval    = 1, 
                tb_log_name     = tensorboard_sub_folder, 
                reset_num_timesteps=True, 
                progress_bar=False)
    
    
    Model_Save_Path = Constants.Model_Save_Path
    model.save(Model_Save_Path)
    
    
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    logger.info(f'Model has trained and Saved in -> "{Model_Save_Path}" <- ')

    """
     Hyperparameters & Default values:
    
        policy, env, learning_rate=0.0003, n_steps=2048, batch_size=64, n_epochs=10, verbose=0, 
        seed=None, device='auto', _init_setup_model=True
        
        gamma=0.99, gae_lambda=0.95, clip_range=0.2, 
        clip_range_vf=None, normalize_advantage=True, ent_coef=0.0, vf_coef=0.5, 
        max_grad_norm=0.5, use_sde=False, sde_sample_freq=-1, 
        target_kl=None, stats_window_size=100, tensorboard_log=None, policy_kwargs=None, 
    
        Explanations:
        
        gamma = A higher gamma value (e.g., 0.99) means that the agent considers future rewards more heavily, 
            which can lead to a longer-term focus in its learning. Conversely, a lower gamma value (e.g., 0.9) 
            makes the agent prioritize immediate rewards (Aggresive). 
    
        gae_lambda = is the factor used for trade-off between bias and variance when estimating advantages with the 
            Generalized Advantage Estimator (GAE). GAE is used to estimate how much better or worse taking a specific 
            action is compared to following the current policy. A higher gae_lambda value (e.g., 0.95) reduces bias 
            but may increase variance, while a lower value reduces variance but may introduce bias into the advantage estimates.
    
        max_grad_norm = is the maximum allowed value for gradient clipping during the training process. 
            Gradient clipping is a technique used to prevent exploding gradients, which can lead to unstable training. 
            If the magnitude of the gradients exceeds this value, they are scaled down to ensure they do not become too large.
    
    """
    
    
except Exception as e:
    exc_type, exc_obj, tb = sys.exc_info()
    line_number = tb.tb_lineno
    print("Error! at ", line_number,"th. line")
    traceback.print_exc()
    pygame.quit()

    
                                                                # Author: RsGoksel
