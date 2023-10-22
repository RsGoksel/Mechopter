
<p align="center">
  <img src="https://github.com/RsGoksel/Mechopter/assets/80707238/10f648bb-0c61-411a-a24f-6b163fc8752a" width="500px"/>
</p>

![Reinforcement Learning](https://img.shields.io/badge/Reinforcement%20Learning-%23000000.svg?&style=for-the-badge)
![Python](https://img.shields.io/badge/Python-%230377B5.svg?&style=for-the-badge)
![Quadcopter](https://img.shields.io/badge/Quadcopter-%237159c1.svg?&style=for-the-badge)
![Pygame](https://img.shields.io/badge/Pygame-%23FFD43B.svg?&style=for-the-badge)
![PPO](https://img.shields.io/badge/PPO-%238BC34A.svg?&style=for-the-badge)
![A2C](https://img.shields.io/badge/A2C-%23FF7043.svg?&style=for-the-badge)
![DQN](https://img.shields.io/badge/DQN-%230000FF.svg?&style=for-the-badge)

# Mech-opter  🎮 🥳
This repository provides code exercise and solution for Reinforcement Learning. All code is written in Python and uses custom RL environment from OpenAI Gym. <br><br>
Goal was train the Reinforcement Learning Drone Agent mastering the flying and accurately hitting a target balloon. A2C was used primaly, PPO and DQN also can be used. Explanations and details are down below ↓ 

## Game Screen
<img src="https://github.com/RsGoksel/Mechopter/assets/80707238/9172b1d7-d33a-4327-a52b-e9b6800d0881" alt="Quad" width="500" />
________________________________________________________________________________________________________________

# Environment & Mechanisms

### _**Reward:**_
 
* -score | Proportional to the distance to the target
* Hitting the target is +score, & restart
* Flying out of the game screen is -score & restart

### _**Observation Space:**_ 

* Agent Y Coordinate
* Angle to Up
* Velocity
* Angular Velocity
* Angle to Target
* Angle Between Target and Velocity
* Distance to Target

###  _**Action Space:**_ 
Action space is discrete(5). It means there is certain 5 moves the Agent has to do. *__Do Nothing, Up, Down, Right, Left__*

________________________________________________________________________________________________________________

## Files 

* [test.py](https://github.com/RsGoksel/Train-PPO-Agent_PongGame/blob/main/test.py): Testing for the environment. You can display game screen.
* [train.py](https://github.com/RsGoksel/Train-PPO-Agent_PongGame/blob/main/train.py): Trains the Agent. You can change total_steps from Constants.py.
* [Agent.py](https://github.com/RsGoksel/Train-PPO-Agent_PongGame/blob/main/Agent.py): Drone class.
* [evaluate.py](https://github.com/RsGoksel/Train-PPO-Agent_PongGame/blob/main/evaluate.py): Evaluate the trained model. Elaborated usage is at down below.
* [env.py](https://github.com/RsGoksel/Train-PPO-Agent_PongGame/blob/main/Env.py)       :  Environment class. You can alter the game rules, Reward mechanism etc.
* [Constants.py](https://github.com/RsGoksel/Train-PPO-Agent_PongGame/blob/main/Constants.py) : Constant variables of the Game. Screen width, hyperparameters etc. 
________________________________________________________________________________________________________________

## Install required libraries: 
``` 
$ pip install -r requirements.txt
```

## Test the environment and check everything is OK:
``` 
$ python test.py
```

## Let's Train!  
Default step is 300k. You can alter it from Constants.py  
(Loading Libraries may take a while)
``` 
$ python train.py
```

## Evaluting the Agent
! After the training, your model will be saved in 'models' file. 
Evaluate your trained model with adding --model parameter to terminal,
Or use pretrained models Which in __*models*__ folder. 
There is a already pretrained model which named "Crayz_bill" and it is default model.
```
$ python evaluate.py
```
__*If you would like to evaluate your custom model:*__
```
$ python evaluate.py --model models/yourmodel
$ python evaluate.py --model models/200k
```

# After the Training 🦾
________________________________________________________________________________________________________________
