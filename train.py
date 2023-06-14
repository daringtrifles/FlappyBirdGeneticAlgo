import sys
import time
import flappy_bird_gym as gym
import matplotlib.pyplot as plt
import collections.abc
import numpy as np
#For an explanation of how the code works, check the ReadMe
hiddenLayerSize = 5
inputSize = 2
nnsd = 1
noiseSD = 0.1
mutateProb = 0.3
genSize = 100
numGen = 10000
bestBirdScore = 0
birds = []
meanscores = []
medianscores = []
class NeuralNetwork():
    ''' A fully connected neural network with 2 hidden layers that uses ReLU '''
    def __init__(self):
        self.params = {}
        self.params['W1'] = np.random.normal(0, nnsd, (inputSize, hiddenLayerSize)) 
        self.params['b1'] = np.random.normal(0,nnsd, hiddenLayerSize)
        self.params['W2'] = np.random.normal(0,nnsd, (hiddenLayerSize,hiddenLayerSize))
        self. params['b2'] = np.random.normal(0,nnsd, hiddenLayerSize) 
        self.params['W3'] = np.random.normal(0,nnsd, (hiddenLayerSize,2))
        self. params['b3'] = np.random.normal(0,nnsd, 2)
    def feedForward(self, input):
        def relu(vec):
            return np.maximum (0,vec)

        if not isinstance(input, np.ndarray):
            input = np.array(input)
        hiddenLayer1 = input @ self.params['W1'] + self.params['b1']
        hiddenLayer1 = relu(hiddenLayer1)
        hiddenLayer2 = hiddenLayer1 @ self.params['W2'] + self.params['b2']
        hiddenLayer2 = relu(hiddenLayer2)
        outputLayer = hiddenLayer2 @ self.params['W3'] + self.params['b3']
        return outputLayer

    def reproduce (self, other):
        def mutate(child):
            def addNoise(arr):
                noise = np.random.normal(0, noiseSD, arr.shape)
                return noise + arr
            for key in child.params.keys():
                child.params[key] = addNoise(child.params[key])
            return child
        child = NeuralNetwork()
        def crossOver():
            def combine(a, b):
                '''This function essentially mimics meiosis. I'd like to thank Apollo Heo for helping me with the implementation of this code'''
                if np.random.binomial(1,0.5) == 1:
                    return a/2 + b/2
                idx = np.random.randint(0, 2, (*a.shape,))
                parents = np.stack((a, b), axis=-1)
                if len(a.shape) == 1:
                    return parents[np.arange(a.shape[0]), idx]
                else:
                    s1, s2 = a.shape
                    return parents[
                        np.tile(np.arange(s1).reshape(s1, 1), (1, s2)).flatten(),
                        np.tile(np.arange(s2), (1, s1))[0],
                        idx.flatten()
                    ].reshape(s1, s2)
            neww1 = combine(self.params['W1'], other.params['W1'])
            newb1 = combine(self.params['b1'], other.params['b1'])
            neww2 = combine(self.params['W2'], other.params['W2'])
            newb2 = combine(self.params['b2'], other.params['b2'])
            neww3 = combine(self.params['W3'], other.params['W3'])
            newb3 = combine(self.params['b3'], other.params['b3'])
            return neww1, newb1, neww2, newb2, neww3, newb3
            
        
        child.params['W1'], child.params['b1'], child.params['W2'], child.params['b2'], child.params['W3'], child.params['b3'] = crossOver()

        if (np.random.binomial(1,mutateProb) == 1):
            return mutate(child)
        return child
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
        scorelst = []
        for __ in range (10):
            env = gym.make("FlappyBird-v0")
            obs, _ = env.reset()
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
                        bestBirdScore = info['score']
                        print ('SCORE CHANGE: NEW SCORE IS', bestBirdScore )
                    scorelst.append(info['score'])
                    break
            env.close()
        scorelst.sort()
        meanscores [genNumber][i] = (sum(scorelst)/len(scorelst), i)
        medianscores[genNumber][i] = (scorelst[len(scorelst)//2], i)
    def createNewGen():
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
bestScore = 0
bestBird = 0
for i in range(numGen):
    runGen(i)
    
print(bestBird.params)
 
