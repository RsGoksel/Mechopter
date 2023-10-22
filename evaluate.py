import argparse
from env import droneEnv
import logging
from stable_baselines3 import A2C

# Initialize the argument parser
parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str, default='models/crayz_bill.zip', help='Path to the model zip file')
args = parser.parse_args()

try:
    env = droneEnv()
    # Load the model using the provided argument or the default value
    model = A2C.load(args.model, env=env)
except Exception as e:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    logger.error(e)
    quit()

import os
from stable_baselines3.common.evaluation import evaluate_policy

evaluate_policy(model, env, n_eval_episodes=10)
quit()
