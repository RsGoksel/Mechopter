import pygame
from env import droneEnv
env = droneEnv()


print("\n\n")
print("Observation space:")
print(env.observation_space)
print("")
print("Action space:")
print(env.action_space)
print("")
print("Action space sample:")
print(env.action_space.sample(),"\n\n")


episode = 0
while episode < 10:
    state = env.reset()
    done = False
    score = 0
    
    while not done:
        
        #env.render() # Step method already involves rendering
        pygame.time.delay(5)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
         
        action = env.action_space.sample()
        n_state, reward, done, info = env.step(action)
        score += reward
    episode += 1
    print('Episode: {} Score:  {}'.format(episode , score))

pygame.display.quit()
pygame.quit()