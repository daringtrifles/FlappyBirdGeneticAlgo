import numpy as np
class NeuralNetwork():
    ''' A fully connected neural network with 2 hidden layers that uses ReLU '''
    hiddenLayerSize = 5
    inputSize = 2
    nnsd = 1
    noiseSD = 0.1
    mutateProb = 0.3

    def __init__(self):
        '''Sets up weights and biases for each layer'''
        self.params = {}
        self.params['W1'] = np.random.normal(0, NeuralNetwork.nnsd, (NeuralNetwork.inputSize, NeuralNetwork.hiddenLayerSize)) 
        self.params['b1'] = np.random.normal(0,NeuralNetwork.nnsd, NeuralNetwork.hiddenLayerSize)
        self.params['W2'] = np.random.normal(0,NeuralNetwork.nnsd, (NeuralNetwork.hiddenLayerSize,NeuralNetwork.hiddenLayerSize))
        self. params['b2'] = np.random.normal(0,NeuralNetwork.nnsd, NeuralNetwork.hiddenLayerSize) 
        self.params['W3'] = np.random.normal(0,NeuralNetwork.nnsd, (NeuralNetwork.hiddenLayerSize,2))
        self. params['b3'] = np.random.normal(0,NeuralNetwork.nnsd, 2)
    def feedForward(self, input):
        '''Outputs a vector of size 2, with each element indicating whether to flap, or do nothing, respectively'''
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
            '''Adds noise to each vector and matrix. The noise follows a zero-mean normal distribution with standard deviation nnsd'''
            def addNoise(arr):
                noise = np.random.normal(0, NeuralNetwork.noiseSD, arr.shape)
                return noise + arr
            for key in child.params.keys():
                child.params[key] = addNoise(child.params[key])
            return child
        child = NeuralNetwork()
        def crossOver():
            def combine(a, b):
                '''This function essentially mimics meiosis. I would like to thank Apollo Heo for help implementing this method'''
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

        if (np.random.binomial(1,NeuralNetwork.mutateProb) == 1):
            return mutate(child)
        return child
