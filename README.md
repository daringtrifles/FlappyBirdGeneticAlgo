# FlappyBirdGeneticAlgo

My goal for this project was to create a bird that could achieve a score of over 1000 using a genetic algorithm. The final bird achieved a median score of 1000 and a high score of over 7000, so I'm quite happy with the outcome.

# Training the Bird

Initially, I used a neural network with 1 hidden layer of 5 neurons, which was able to achieve a score of 300 in 20 generations. This success indicated that I was moving in the right direction. After some experimentation, I found that using 2 hidden layers worked best. I trained the birds again, and this time they were able to achieve scores above 1000.

However, I wanted to further improve the bird's performance. I tried training the bird with 10 neurons in each hidden layer, but it took too many generations to reach a satisfactory score. Instead, I decided to freeze the weights of the network with 5 neurons in each layer. Then, I reran the genetic algorithm with 10 neurons per hidden layer, but for the first generation, 5 of the neurons use the frozen weights, and the other neurons have their weights set to 0. This approach yielded excellent results and led to the resulting bird.

For each generation, which consisted of 100 birds, I ran each bird 10 times. I selected the top 3 birds with the highest mean scores and the top 3 birds with the highest median scores. I used these top-performing birds to repopulate 90 out of the 100 birds through crossover. Additionally, I introduced 10 randomly generated birds every generation to prevent getting stuck in local minima. During crossover, I also applied small mutations to the birds' neural network parameters, such as weights and biases.

# Areas for Improvement

The bird's consistency is still an area that needs improvement. In 10 runs, its best score can exceed 5000, while its worst score can be less than 100. To address this issue, I believe finding an alternative fitness metric to rank the bird's performance could be beneficial.


![](https://github.com/daringtrifles/FlappyBirdGeneticAlgo/blob/main/FlappyBird.gif)

GIF of the final bird playing the game (it doesn't die at 40, just that the display crashes afterwards :P)


