import sys
import time
import flappy_bird_gym as gym
from NeuralNetwork import NeuralNetwork
import matplotlib.pyplot as plt
import collections.abc
import numpy as np
#For an explanation of how the code works, check the ReadMe


genSize = 100
numGen = 200
birds = []
meanscores = []
medianscores = []

def initialise():
    for i in range(numGen+10):
        arr = [None]*genSize
        birds.append(arr[:])
        meanscores.append(arr[:])
        medianscores.append(arr[:])

    for i in range (genSize):
        birds[0][i] = NeuralNetwork()
def runGen(genNumber):
    for i in range (genSize):
        scorelst = [] # List of scores a particular bird gets
        for __ in range (10):
            env = gym.make("FlappyBird-v0") # Setup for flappy bird gym to run
            obs, _ = env.reset() # Setup for flappy bird gym to run
            score = 0
            while True:
                def chooseAction():
                    vec = birds[genNumber][i].feedForward(np.array(obs))
                    if vec[0] > vec[1]:
                        return 0
                    else: return 1

                if isinstance( obs, np.float64 ):
                    action = 0
                else:
                    action = chooseAction()                
                obs, reward, terminated, info = env.step(action)

                score += reward                
                
                if terminated:
                    global bestBirdScore
                    if info['score'] > bestBirdScore:
                        global bestBird
                        bestBird = birds[genNumber][i]
                        bestBirdScore = info['score']
                        print ('NEW HIGH SCORE IS', bestBirdScore )
                    scorelst.append(info['score'])
                    break
            env.close()
        scorelst.sort()
        meanscores [genNumber][i] = (sum(scorelst)/len(scorelst), i)
        medianscores[genNumber][i] = (scorelst[len(scorelst)//2], i)
    def createNewGen():
        '''Creates the next generation of birds using the top 3 birds according to their mean score and the top 3 birds according to their median score.'''
        cnt = 0
        v1 = meanscores[genNumber][:]
        v1.sort(reverse = True)
        v2 = medianscores[genNumber][:]
        v2.sort(reverse = True)
        v = v1[:3]
        v.extend(v2[:3]) 
        for i in range(5):
            birds[genNumber + 1][cnt] = NeuralNetwork()
            cnt += 1
        for i in range(len(v)):
            birds[genNumber + 1][cnt] = birds[genNumber][v[i][1]]
            cnt += 1
        while True:
            for i in range(len(v)):
                bird1 = birds[genNumber][v[i][1]]
                for j in range(len(v)):
                    bird2 = birds[genNumber][v[j][1]]
                    birds[genNumber + 1][cnt] = bird1.reproduce(bird2)
                    cnt += 1
                    if cnt >= genSize:
                        return
    createNewGen()

initialise()
bestBirdScore = 0
bestBird = birds[0][0]
for i in range(numGen):
    runGen(i)
    
print(bestBird.params)
 
