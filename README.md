# FlappyBirdGeneticAlgo

My goal for this project was to create a bird that could get a score over 1000 using a genetic algorithm. The final bird gets a median score of 1000 and has a high score of over 7000, so I'm quite happy with how this has turned out.

# How the bird was trained

I initially used a neural network with 1 hidden layer of 5 neurons, and this was able to get a score of 300 in 20 generations, which proved to me that I was heading in the right direction. After some testing, it seemed that 2 hidden layers worked best, so I stuck with it and retrained the birds. This was able to get scores of above 1000, but I wanted to see if I could make the bird even better. I tried training the bird with 10 neurons in each hidden layer, but this seemed to take too many generations before reaching a good score, so instead, I freezed the weights of the network with 5 neurons in each layer, and then reran the genetic algorithm with the first generation having the frozen weights, and all other weights were set to 0. This worked wonderfully, and ended meup with the resulting bird. The code for the second generation 

![](https://github.com/daringtrifles/FlappyBirdGeneticAlgo/blob/main/FlappyBird.gif)

GIF of the final bird playing the game (it doesn't die at 40, just that the display crashes afterwards :P)


